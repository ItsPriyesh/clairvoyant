import requests
import clairvoyant_data
import clairvoyant
import traceback
import json
import multiprocessing

from multiprocessing import Queue

_API_ENDPOINT = "http://localhost:5000/model/gateway"
_HEADERS = {'content-type': 'application/json'}

def init(input_buff, output_buff):
    print("Initializing Client Process...")
    while(1):

        # If the input buffer has data, poll and convert it into a JSON object
        # while maintaining the original packet structure.
        if (input_buff.empty() == False):
            packet = input_buff.get()

            payload = {'x-packet': packet.to_dict()}
            payload_json = json.dumps(payload)

            response = requests.post(url = _API_ENDPOINT, data = payload_json, headers = _HEADERS);
            print(response.content)