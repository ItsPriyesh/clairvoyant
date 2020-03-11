import requests
import clairvoyant_data
import clairvoyant
import os
import time
import traceback
import json
import multiprocessing
from multiprocessing import Queue
from clairvoyant_data import PacketBuilder
from clairvoyant_data import PacketBuilder

_API_ENDPOINT = "http://localhost:5000/model/predict"


def convertpayload_transmit(payload_q):

    while(1):
        if (packet_tx_q.empty() == False):
            packet = packet_tx_q.get()

            if (packet.get_type() == "ML_CLASS"):
                string = construct_lora_ml_string(packet)
                                
            elif (packet.get_type() == "HEART_BEAT"):
                string = construct_lora_heartbeat_string(packet)

            elif (packet.get_type() == "ACK"):
                string = construct_lora_ack_string(packet)

            elif (packet.get_type() == "MOTION_EVENT"):
                string = construct_lora_motion_string(packet)

            raw_file_path = os.path.join('output','text','packet.txt')


            file = open(raw_file_path,"w")
            file.write(string)
            file.close()

            files = {'text' : (file_name, open(file_path, 'rb'), 'text/txt')} 

            response = requests.post(url = _API_ENDPOINT, files=files)
            if(not response.ok):
                print("An Error occurred while loading the prediction model..")
                print(response.content)
        
            response_bytes = response.content
            response_decoded = response_bytes.decode('utf8').replace("'", '"')
            parsed_res = json.loads(response_decoded)

q = Queue()

print("CREATING A ML CLASS PACKET")
payload = MlPayload()
payload._battery_lvl = 100.0
payload._timestamp = round(time.time())
payload._classification = "BOMB"
payload._confidence = 100.0
packet = PacketBuilder().set_type("ML_CLASS").set_node_id(clairvoyant.CURRENT_NODE).set_message_id().set_payload(payload).set_ttl().set_retry_count(10).set_hop_count(10)
packet = packet.build()
q.put(packet)
convertpayload_transmit(q)

                

        
    
