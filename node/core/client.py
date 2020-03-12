from urllib import request, parse
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
from uart_process import *

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


  
    

			data = parse.urlencode({"test": string}).encode()
			req =  request.Request("http://localhost:5001/", data=data) # this will make the method "POST"
			resp = request.urlopen(req)
            
          

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

                

      