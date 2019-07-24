import time

from multiprocessing import queue
from clairvoyant_data import PacketBuilder

_DEFAULT_HEARTBEAT_FREQ = 900 #15 Minutes

def init(input_buff, output_buff):
    print("Initializing Heartbeat Process...")

    while(1):
    	#TODO(Sathoshi): Add node id and accurate battery level
    	payload = {'id':'1', 'timestamp': round(time.time()), 'battery_level':100.0}
    	hb_packet = PacketBuilder()
    	hb_packet.set_type("HEART_BEAT")
    	hb_packet.set_node_id("curr")
    	hb_packet.set_message_id()
    	hb_packet.set_payload(payload)
    	hb_packet.set_ttl()

    	output_buff.put(hb_packet)

    	time.sleep(_DEFAULT_HEARTBEAT_FREQ)