import requests
import clairvoyant_data
import clairvoyant
import os
import time
import traceback
import json

from clairvoyant_data import PacketBuilder
from clairvoyant_data import PacketBuilder

_API_ENDPOINT = "http://192.168.1.149:5000/model/predict"


if __name__ == '__main__':
# def init(ml_q, ml_init_q):
    print("Initializing Machine Learning Process...")
    
    files = []

    # while (1):

        #check for new files
        # if (ml_q.empty() == False):
            # files.append(str(ml_q.get()) + ".wav")


    	# if (len(files) > 0):
    files.append("1.wav")
    file_path = os.path.join('output','processed_audio',files[0])
    files = {'audio' : (files[0], open(file_path, 'rb'), 'audio/wav')} 

    response = requests.post(url = _API_ENDPOINT, files=files)
    if(not response.ok):
        print("An Error occurred while loading the prediction model..")
        print(response.content)
        
    parsed_res = json.loads(response.content)
    print(parsed_res)