import SimpleHTTPServer
import SocketServer
from uart_processor import *


PORT = 5001

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)
      print(post_body)

      parse_rx_msg(post_body["test"])
      self.send_response(200, message=None) 


# Launch uart subprocess
# Initialize uart_tx queue
tx_q = Queue()

# Any recieving messages from the lora module should be put back into the 
# input_buffer for the comm_processor to handle.
rx_q = Queue()

# Start uart processttggt
proc = multiprocessing.Process(target=comm_processor.init, args=(tx_q, rx_q),)
proc.start()
Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()