import pyaudio
import multiprocessing
import serial
import time
import os
from multiprocessing import queue
from uart_processor import uart_process


def lora_comm_processor():
    #transmit queue
    tx_q = queue.Queue()
    #rx event queue, i.e where event notifs are
    rx_event_q = queue.Queue()
    #rx cmd queue i.e where +OK, +Reset, +Ready, etc from Lora module come
    rx_cmd_q = queue.Queue()

    #start uart process
    uart_task = multiprocessing.Process(target=uart_process, args=(tx_q,rx_event_q,rx_cmd_q,))
    uart_task.start()

    
    #init LoRa module
    software_reset(tx_q)
    set_work_mode(tx_q)
    set_uart_baud(tx_q)
    set_rf_params(tx_q)
    set_rf_frequency(tx_q)
    set_at_address(tx_q)
    set_network_id(tx_q)
    set_network_pass(tx_q)

    while(1):
        #insert state machine here..






#There are 2 types of packets (Event Packet from Node, or MESH PATH ack packets during mesh path finding
#Packet Structure for Event Packets
#B1 = enum(event  packet, mesh path_1 packet, mesh path_2 packet event ack packet, mesh path ack packet)
#B2 = Hop #
#B3 = Battery Life ( 0 to 100), nodes with constant pwr have 100
#B4 = Number of Triplets
#B(5 to 5+ 3*75 - 1) = 75 Triplets ( #sec since event, event type enum(Movement, Human Voice, Vehicles, Gunshots, Explosions), confidence level ( to 100)).
#B(230 to B236) = Signature (c51410)
#B(237 to 240) = CRC32


#Mesh Path ACK Packet Structure
#B1 = enum(event  packet, mesh path_1 packet, mesh path_2 packet event ack packet, mesh path ack packet)
#B2 = Battery Life
#B(3 - 229) = NULL
#B(230 to 236) = Signature (c51410)
#B(237 to 240) = CRC32


#Gateway sends 3 types of Packets

#Mesh Path packet and Event ack packet
#Event ack packet structure
#B1 = enum(event  packet, mesh path_1 packet, mesh path_2 packet event ack packet, mesh path ack packet)
#B2 = ID of recepient
#B(3 - 229) = NULL
#B(230 to 236) = Signature (c51410)
#B(237 to 240) = CRC32


#Mesh Path_1 Packet structure
#B1 = enum(event  packet, mesh path_1 packet, mesh path_2 packet event ack packet, mesh path ack packet)
#B(2 - 229) = NULL
#B(230 to 236) = Signature (c51410)
#B(237 to 240) = CRC32


#Mesh Path_2 Packet structure
#B1 = enum(event  packet, mesh path_1 packet, mesh path_2 packet event ack packet, mesh path ack packet)
#B2 = 'G'
#B3 = '.'
#B(4 to N) = ID of each node that hasn't been detected yet by the gateway
#B(N+1) = '.'
#B(N+2 to 229) = NULL
#B(230 to 236) = Signature (c51410)
#B(237 to 240) = CRC32

        

}
