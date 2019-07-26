import traceback
import multiprocessing
import time
import random
import clairvoyant
import traceback

from multiprocessing import Queue
from uart_processor import uart_process
from clairvoyant_rpc import ClairvoyantRPCService
from clairvoyant_data import Packet
from clairvoyant_data import PacketBuilder
from collections import deque

"""
The communication processor is responsible for any message communication.
Any data that is passed through the input_buff will be passed through the appropriate network 
communication protocol
Note: If there is a valid WiFi connection, the data will be passed to the server 
instead of the LoRa Module.
Note: Application layer retry logic will be handled by the comm_processor
Note: If the FORCE_GATEWAY is set true, then LoRa will be bypassed.
Note: The current version of the comm_processor does not handle routing and is simply broadcast_all
Note: This comm_processor is not thread-safe.

The messeages that must be handled can be broken into two main criteria
    Case 1: Messages that need to be sent to servers.
        - Events that are detected by the machine learning model.
        - Heart beat/ status information about nodes
    Case 2: Messages that need to be sent to a node.
        - Ack messages.

Expected Packet
{
    t: [HEART_BEAT, ML_CLASS, ACK],
    node_id: 
    message_id: 1,
    payload: { /* follow rpc standard */},
    ttl: 10000s
}

Note: Refer to clairvoyant_data Packet or the latest version.
Note: All data that are not Packet objects are dropped.

"""




"""
Retry Service is responsible for handling application layer retry logic
for messages that are from the current node.

Note: retry_map has the following format.
{
    [unique message id] : {
            ack: [true/false]
            ttr: [timestamp]
            retry: [count]
    }
}
"""
class RetryService:

    _MAX_RETRY_COUNT = 5

    def __init__(self):
        self._retry_blocking_q = deque()
        self._retry_map = {}
        print("Starting retry service")

    def _calculate_backoff_time(self):
        return time.time() + random.randint(8,13)

    def has_messages(self):
        while len(self._retry_blocking_q) > 0:
            data = self._retry_blocking_q[0]
            # Check if there is any metadata assosciated with message.
            if data.get_message_id() in self._retry_map:
                retry_metadata = self._retry_map[data.get_message_id()]
                # If the message has been acked, discard it.
                if retry_metadata['ack'] == True:
                    self._retry_blocking_q.popleft()
                    del self._retry_map[data.get_message_id()]
                    continue
                else:
                    # Message has not been acked yet
                    # Check if current time is greater than estimated backoff time.
                    if time.time() > retry_metadata['ttr']:
                        # If retry count is greater than MAX_RETRY_COUNT, drop packet
                        if retry_metadata['retry'] > RetryService._MAX_RETRY_COUNT:
                            self._retry_blocking_q.popleft()
                            del self._retry_map[data.get_message_id()]
                            continue
                        else:
                            # If retry count is smaller than MAX_RETRY_COUNT, message is ready.
                            return True
                    else:
                        return False
            else:
                # If there is no metadata, message is ready.
                return True
        return False


    """
    Raise out of range error if no data in the retry service.
    Note: get() will return the data element at the head of the queue regardless of retry config.
    Note: get() will automaticall update internal ttr and retry count metadat for the data element
          at the head of the queue.
    """
    def get(self):
        data = self._retry_blocking_q[0]

        # Check if the data has a metadata in the map
        if data.get_message_id() in self._retry_map:
            # If there is already metadata in the map, update its metadata.
            retry_metadata = self._retry_map[data.get_message_id()]
            retry_metadata['retry'] = retry_metadata['retry'] + 1
            retry_metadata['ttr'] = self._calculate_backoff_time()
            data.increment_retry_count();
            return data
        else:
            # Add metadata to retry_map and return
            metadata = {'ack':False,'ttr': self._calculate_backoff_time(), 'retry':0}
            self._retry_map[data.get_message_id()] = metadata
            return data


    def add_message_to_blocking_queue(self, data):
        if ((data is None or not isinstance(data, Packet)) 
            or (data.get_type() not in Packet.VALID_EVENT_TYPES)):
            raise ValueError("Invalid data argument {}".format(data))
        self._retry_blocking_q.append(data)

    def ack(self, ack):
        if (ack is None or not isinstance(ack, Packet) 
            or ack.get_type() not in Packet.VALID_ACK_TYPES):
            raise ValueError("Invalid data argument {}".format(ack))

        if (ack.get_message_id() in self._retry_map):
            self._retry_map[ack.get_message_id()]['ack'] = True



def init(input_buff, output_buff):
    print("Initializing Communication Process...")

    # Launch uart subprocess
    # Initialize uart_tx queue
    uart_tx_buff = Queue()

    # Any recieving messages from the lora module should be put back into the 
    # input_buffer for the comm_processor to handle.
    uart_rx_buff = input_buff

    # Start uart processttggt
    uart_proc = multiprocessing.Process(target=uart_process, args=(uart_tx_buff, uart_rx_buff),)
    uart_proc.start()

    # Initalize rpc service for communicating with clairvoyant server
    rpc_service = ClairvoyantRPCService()
    retry_service = RetryService()

    while(1):
        data = None
        if (retry_service.has_messages()):
            data = retry_service.get()
        elif not input_buff.empty():
            data = input_buff.get()
            # If it is a piece of data that we don't know what to do with. simply drop it
            if not isinstance(data, Packet):
                continue;
                
            data.increment_hop_count()

            if data.get_node_id() == clairvoyant.CURRENT_NODE:
                if data.get_type() in Packet.VALID_EVENT_TYPES:
                    try:
                        retry_service.add_message_to_blocking_queue(data)
                    except Exception as e:
                        traceback.print_exc()
                    continue
                elif data.get_type() in Packet.VALID_ACK_TYPES:
                    try:
                        retry_service.ack(data)
                    except Exception as e:
                        traceback.print_exc()
                    continue
        else:
            continue

        print("processing...")
        print(data)

        # Data packets that are ready to be sent.
        #TODO(Sathoshi): implement cache for TTL
        if data.get_type() == "ACK":
            uart_tx_buff.put(data)
        elif data.get_type() == "ML_CLASS":
            try:
                #TODO(Sathoshi): Handle server ack
                ack_packet = rpc_service.create_data_point(data)
                input_buff.put(ack_packet)
            except Exception as e:
                traceback.print_exc
                if (not clairvoyant.FORCE_GATEWAY):
                    uart_tx_buff.put(data)
        elif data.get_type() == "HEART_BEAT":
            try:
                #TODO(Sathoshi): Handle server ack
                ack_packet = rpc_service.heart_beat(data)
                input_buff.put(ack_packet)
            except Exception as e:
                traceback.print_exc
                if (not clairvoyant.FORCE_GATEWAY):
                    uart_tx_buff.put(data)


