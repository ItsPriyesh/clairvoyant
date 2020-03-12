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
from clairvoyant_data import *
import json

_API_ENDPOINT = "http://10.33.143.62:5000/model/predict"


def cms(Packet):
    payload = []
    payload.append("mtn")
    payload.append(Packet._node_id)
    payload.append(Packet._message_id)
    payload.append(Packet._hop_count)
    payload.append(Packet._retry_count)
    payload.extend(Packet._payload.to_array())


    return payload


def cml(Packet): 
    payload = []
    payload.append("ml")#packet type
    payload.append(Packet._node_id)
    payload.append(Packet._message_id)
    payload.append(Packet._hop_count)
    payload.append(Packet._retry_count)
    payload.extend(Packet._payload.to_array())


    return payload
  
def chb(Packet):
    payload = []
    payload.append("hb")#packet type
    payload.append(Packet._node_id)
    payload.append(Packet._message_id)
    payload.append(Packet._hop_count)
    payload.append(Packet._retry_count)    
    payload.extend(Packet._payload.to_array())


    return payload

def init(input_buff, output_buff):
    string = ""

    while(1):
        if (input_buff.empty() == False):
            packet = input_buff.get()
            print("Got Packet sending to laptop server")

            if (packet.get_type() == "ML_CLASS"):
                string = cml(packet)
                                
            elif (packet.get_type() == "HEART_BEAT"):
                string = chb(packet)


            elif (packet.get_type() == "MOTION_EVENT"):
                string = cms(packet)

            string = json.dumps(string,separators=(',', ':'))

            b = string  
            print(b)

            data = parse.urlencode({str(string): "test"}).encode('utf8')
            req =  request.Request("http://10.33.143.62:5001/", data=data) # this will make the method "POST"
            resp = request.urlopen(req)
            
          

# q = Queue()

# print("CREATING A ML CLASS PACKET")
# payload = MlPayload()
# payload._battery_lvl = 100.0
# payload._timestamp = round(time.time())
# payload._classification = "BOMB"
# payload._confidence = 100.0
# packet = PacketBuilder().set_type("ML_CLASS").set_node_id(clairvoyant.CURRENT_NODE).set_message_id().set_payload(payload).set_ttl().set_retry_count(10).set_hop_count(10)
# packet = packet.build()
# q.put(packet)
# convertpayload_transmit(q)

                

      
