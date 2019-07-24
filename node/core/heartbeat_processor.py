import time
import multiprocessing
import clairvoyant

from clairvoyant_data import PacketBuilder
from clairvoyant_data import Packet
from clairvoyant_data import HeartbeatPayload

_DEFAULT_HEARTBEAT_FREQ = 900 #15 Minutes
_DEFAULT_HEARTBEAT_FREQ = 30 #15 Minutes

def init(input_buff, output_buff):
    print("Initializing Heartbeat Process...")

    while(1):

        payload = HeartbeatPayload()
        payload._battery_lvl = 100.0
        payload._timestamp = round(time.time())
        builder = PacketBuilder()
        builder.set_type("HEART_BEAT")
        builder.set_node_id(clairvoyant.CURRENT_NODE)
        builder.set_message_id()
        builder.set_payload(payload)
        builder.set_ttl()
        builder.set_retry_count()
        builder.set_hop_count()

        print("=== CREATING HEART BEAT PACKET ===")
        output_buff.put(builder.build())

        time.sleep(_DEFAULT_HEARTBEAT_FREQ)