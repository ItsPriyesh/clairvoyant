import time

import multiprocessing
from clairvoyant_data import PacketBuilder
from clairvoyant_data import Packet

_DEFAULT_HEARTBEAT_FREQ = 900 #15 Minutes

def init(input_buff, output_buff):
    print("Initializing Heartbeat Process...")

    while(1):
        print("CREATING A HEART BEAT PACKETS")

        payload = HeartbeatPayload()
        payload._battery_lvl = 100.0
        payload._timestamp = round(time.time())
        packet = PacketBuilder()
        packet.set_type("HEART_BEAT")
        packet.set_node_id(clairvoyant.CURRENT_NODE)
        packet.set_message_id()
        packet.set_payload(payload)
        packet.set_ttl()
        packet.set_retry_count()
        packet.set_hop_count()

        print("adding heartbeat packet to output buff");
        output_buff.put(packet)

        time.sleep(_DEFAULT_HEARTBEAT_FREQ)