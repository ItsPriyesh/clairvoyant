import requests
import clairvoyant_data
import clairvoyant
import os
import time
import traceback
import json

from clairvoyant_data import PacketBuilder
from clairvoyant_data import PacketBuilder

_API_ENDPOINT = "http://10.33.143.62:5000/model/predict"

def init(input_q, output_q):
    print("Initializing Machine Learning Process...")

    files = []

    while (1):
        
        #check for new files
        if (input_q.empty() == False):
            files.append(str(input_q.get()) + ".wav")
            
        if (len(files) > 0):
            print("file " + str(files[0]))
            file_path = os.path.join('output','processed_audio',files[0])

            ibm_packet = ibm_model(files[0], file_path)

            if (ibm_packet != "NOISE"):
                output_q.put(ibm_packet)

            os.remove(file_path)
            del files[0]

def ibm_model(file_name, file_path):
    
    files = {'audio' : (file_name, open(file_path, 'rb'), 'audio/wav')} 

    response = requests.post(url = _API_ENDPOINT, files=files)
    if(not response.ok):
        print("An Error occurred while loading the prediction model..")
        print(response.content)
        
    response_bytes = response.content
    response_decoded = response_bytes.decode('utf8').replace("'", '"')
    parsed_res = json.loads(response_decoded)

    built_packet = ''
        
    prediction = parsed_res['prediction']
    normalized_ratio = parsed_res['normalized_ratio']
    if normalized_ratio < 0.3:
      return "NOISE"

    # If we have classified as noise..
    # Ignore and don't send a packet through the mesh network.
    if str(prediction) == 'noise':
        return "NOISE"

    timestamp = round(time.time())
    ml_payload = clairvoyant_data.MlPayload()
    ml_payload._battery_lvl = 100.0
    ml_payload._timestamp = timestamp
    ml_payload._classification = prediction
    ml_payload._confidence = normalized_ratio
    ml_packet = PacketBuilder().set_type("ML_CLASS").set_node_id(clairvoyant.CURRENT_NODE).set_message_id().set_payload(ml_payload).set_ttl().set_retry_count().set_hop_count()
    built_packet = ml_packet.build()

    return built_packet
