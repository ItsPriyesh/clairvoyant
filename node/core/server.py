from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from uart_processor import *
import multiprocessing
from urllib.parse import unquote
import ast
import comm_processor
import json	

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))
        # print(unquote(post_data))
        packetStr = unquote(str(post_data, 'utf-8', errors='ignore'))[:-5]
        res = (json.loads(packetStr))

        packet = construct_packet_from_list(res)

        print(packet)


        # print(parse_rx_msg(post_data))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')



# Launch uart subprocess
# Initialize uart_tx queue
tx_q = Queue()

# Any recieving messages from the lora module should be put back into the 
# input_buffer for the comm_processor to handle.
rx_q = Queue()

# Start uart processttggt
# proc = multiprocessing.Process(target=comm_processor.init, args=(tx_q, rx_q),)
# proc.start()

run(port=5001)