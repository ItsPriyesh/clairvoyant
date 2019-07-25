import serial
from multiprocessing import Queue
from clairvoyant_data import *
from lora_driver import *
import clairvoyant
import time
import binascii
import time
import ast

signature = 151410
encryption_key = 21093
    

#key: any n digit number, ex (1238135), more numbers more secure.
#string: "hello"
def akash_encrypt(string):

    global encryption_key

    key = str(encryption_key)
    list_key = ""
    out = ""


    #make key long enough for list
    while ( len(list_key) < len(string)):
        list_key += key
    
    for i in range(len(string)):

        ##human readable is 32 to 126
        string_ascii = ord(string[i])
        key_digit = int(list_key[i])

        if (string_ascii - key_digit <32):
            #ex ascii = 32, digit = 1 -> 31 , 32-31 = 1, 1-1 = 0, str_ascii = 126
            string_ascii = 126 - (32 - (string_ascii - key_digit) - 1)
        else:
            string_ascii-=key_digit
        
        out += str(chr(string_ascii))

    out = out[::-1]

    return out

def akash_decrypt(string):
    global encryption_key

    key = str(encryption_key)
    list_key = ""
    out = ""

    string = string[::-1]

    #make key long enough for list
    while ( len(list_key) < len(string)):
        list_key += key
    
    
    for i in range(len(string)):

        ##human readable is 32 to 126
        string_ascii = ord(string[i])
        key_digit = int(list_key[i])

        if (string_ascii + key_digit >126):
            #ex ascii = 126, digit = 1 -> 127 , 127 - 126 = 1, 1-1 = 0, str_ascii = 32
            string_ascii = 32 + ((string_ascii + key_digit) - 126 - 1)
        else:
            string_ascii+=key_digit
        
        out += str(chr(string_ascii))

    return out
    


                
def parse_rx_msg(string):
    global signature

    crc = string[:8]
    payload = string[8:]

    #check crc and make sure its not corrupted
    computed_crc32 = binascii.crc32(payload.encode())    
    computed_crc32 = "{:08x}".format(computed_crc32)

    if (computed_crc32 != crc):
        return False

    #decrypt message
    payload = akash_decrypt(payload)

    
    #decode list
    try:
        payload = ast.literal_eval(payload)
    except SyntaxError:
        return False

    #check signature filed
    if (payload[-1] != signature): #invalid packet
        return False
    #remove signature field
    payload = payload[:-1]
    #print(payload)
    #return payload list
    return payload

def construct_packet_from_list(payload):
    packet = PacketBuilder()

    if (payload[0] == "ml"):
        mlpayload = MlPayload()

        packet.set_type("ML_CLASS")
        packet.set_node_id( payload[1])
        packet.set_message_id( payload[2])
        packet.set_hop_count( payload[3])
        packet.set_retry_count( payload[4])
        packet.set_payload( mlpayload.from_array(payload[5:]))
        
    elif (payload[0] == "hb"):
        hbpayload = HeartbeatPayload()
        
        packet.set_type( "HEART_BEAT")
        packet.set_node_id( payload[1])
        packet.set_message_id( payload[2])
        packet.set_hop_count( payload[3])
        packet.set_retry_count( payload[4])
        packet.set_payload( hbpayload.from_array(payload[5:]))

    elif (payload[0] == "ack"):
        packet.set_type( "ACK")
        packet.set_node_id( payload[1])
        packet.set_message_id( payload[2])
        packet.set_hop_count( payload[3])
        packet.set_retry_count( payload[4])
        packet.set_payload(AckPayload())

    else:
        return False
    
    packet.set_ttl()
    packet = packet.build()
    
    return packet


#input json, return string
def parse_tx_msg(packet):
    global signature

    packet.append(signature)

    packet = str(packet)


    packet = akash_encrypt(packet)
    #packet_s = akash_decrypt(packet_s)
    
    #compute a crc of packet
    crc = binascii.crc32(packet.encode())

    crc = "{:08x}".format(crc)

    #append CRC to beginning
    packet = crc + packet
    
    return packet



def construct_lora_ml_string(Packet): 
    payload = []
    payload.append("ml")#packet type
    payload.append(Packet._node_id)
    payload.append(Packet._message_id)
    payload.append(Packet._hop_count)
    payload.append(Packet._retry_count)
    payload.extend(Packet._payload.to_array())

    string = parse_tx_msg(payload)

    return string
  
def construct_lora_heartbeat_string(Packet):
    payload = []
    payload.append("hb")#packet type
    payload.append(Packet._node_id)
    payload.append(Packet._message_id)
    payload.append(Packet._hop_count)
    payload.append(Packet._retry_count)    
    payload.extend(Packet._payload.to_array())

    string = parse_tx_msg(payload)

    return string


def construct_lora_ack_string(Packet):
    payload = []
    payload.append("ack")
    payload.append(Packet._node_id)
    payload.append(Packet._message_id)
    payload.append(Packet._hop_count)
    payload.append(Packet._retry_count)

    string = parse_tx_msg(payload)

    return string



    

def uart_process(packet_tx_q, packet_rx_q):

    #init uart_q consists of tx strings and ack strings  (+Reset, +OK, +READY)
    uart_q = Queue()
    
    #initialize uart
    ser = serial.Serial('com5', baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS
                        )

    #Current Transmitted/Ack String
    curr_uart = None

    #Timestamp used for retrying, when an ack wasnt received
    curr_ack_ts = None

    lora_init(uart_q,clairvoyant.LORA_NODE_ID,clairvoyant.LORA_NETWORK_ID)

    while(1):

#process rx strings
        if (ser.inWaiting() > 0):

            rx_data = ser.readline()
            rx_data = str(rx_data,'utf-8',errors='ignore')
            rx_data = rx_data[:-2] #remove /r/n

            #check for error
            if (rx_data[:4] == "+ERR"):
                print("LoRa Error detected: " + str(rx_data))
                ##ADD reset module prob... will have to test and see types of errors

            #check for receive message
            elif (rx_data[:4] == "+RCV"):
                print("LoRa Message Received: " + str(rx_data))
                comm_index = ([pos for pos, char in enumerate(rx_data) if char == ','])
                rx_data = rx_data[comm_index[1] + 1: comm_index[-2]]
                ##process receive messages
                payload = parse_rx_msg(rx_data)
                packet = False
                
                if (payload != False):
                    packet = construct_packet_from_list(payload)
                    #print("valid payload uart")
                if (packet != False):
                    #print("valid packet uart")
                    #print("Received Packet: " + str(packet))
                    packet_rx_q.put(packet)
                
                
            #ack message
            elif (curr_uart != None):
                #print("Ack " + str(rx_data))
                #check if received msg is first element in ack list for that command

                ack_check = False
                
                for ack in curr_uart.ack_list:
                    if (rx_data.find(ack) != -1):
                        ack_check = True
                    else:
                        ack_check = False

                if (ack_check == True):
                    curr_ack_ts = None
                    curr_uart = None
                    curr_ack_index = 0
                    #print("Ack Received")

            
####process tx strings
        #check if not waiting on ack
        if (uart_q.empty() == False):
            if (curr_uart == None):

                curr_uart = uart_q.get()
                curr_ack_index = 0
                curr_ack_ts = time.time()

                ser.write(curr_uart.tx_string.encode())
                print("LoRa Send: " + str(curr_uart.tx_string.encode()))

            #check if ack timed out
            elif (time.time() - curr_ack_ts >= 5): #5 sec has passed since string has been sent
                #resend transmit, reset ack index, and ts
                curr_ack_index = 0
                curr_ack_ts = time.time()
                    
                ser.write(curr_uart.tx_string.encode())
                print("LoRa Send Retry: " + str(curr_uart.tx_string.encode()))
        
####process tx packets from com_process             
        if (packet_tx_q.empty() == False):
            packet = packet_tx_q.get()

            if (packet.get_type() == "ML_CLASS"):
                string = construct_lora_ml_string(packet)
                lora_transmit(uart_q, True, None, string)
                
            elif (packet.get_type() == "HEART_BEAT"):
                string = construct_lora_heartbeat_string(packet)
                lora_transmit(uart_q, True, None, string)

            elif (packet.get_type() == "ACK"):
                string = construct_lora_ack_string(packet)
                lora_transmit(uart_q, True, None, string)

                
                



def test_uart_process():
    a = Queue()
    b = Queue()

    print("CREATING A ML CLASS PACKET")
    payload = MlPayload()
    payload._battery_lvl = 100.0
    payload._timestamp = round(time.time())
    payload._classification = "BOMB"
    payload._confidence = 100.0
    packet = PacketBuilder().set_type("ML_CLASS").set_node_id(clairvoyant.CURRENT_NODE).set_message_id().set_payload(payload).set_ttl().set_retry_count(10).set_hop_count(10)
    packet = packet.build()
    a.put(packet)
    uart_process(a,b)

    # print("adding ml packet to output buff");
#test_uart_process()
