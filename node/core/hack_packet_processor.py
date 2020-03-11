from uart_processor import construct_packet_from_list
import os


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

                

        
    
