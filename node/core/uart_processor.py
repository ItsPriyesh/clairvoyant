import serial
from multiprocessing import Queue
from clairvoyant_data import PacketBuilder, Packet
import lora_driver
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
    computed_crc32 = str(hex(computed_crc32))[2:]

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
    
    #return payload list
    return payload

def construct_packet_from_list(payload):
    packet = PacketBuilder()

    if (payload[0] == "ml"):
        mlpayload = MlPayload()

        packet.set_type(packet,"ML_CLASS")
        packet.set_node_id(packet, payload[1])
        packet.set_message_id(packet, payload[2])
        packet.set_hop_count(packet, payload[3])
        packet.set_retry_count(packet, payload[4])
        packet.set_payload(packet, mlpayload.to_array(payload[5:]))
        
    elif (payload[0] == "hb"):
        hbpayload = HeartbeatPayload()
        
        packet.set_type(packet, "HEART_BEAT")
        packet.set_node_id(packet, payload[1])
        packet.set_message_id(packet, payload[2])
        packet.set_hop_count(packet, payload[3])
        packet.set_retry_count(packet, payload[4])
        packet.set_payload(packet, hbpayload.to_array(payload[5:]))

    elif (payload[0[ == "ACK"):
        packet.set_type(packet, "ACK")
        packet.set_node_id(packet, payload[1])
        packet.set_message_id(packet, payload[2])
        packet.set_payload(packet, None)

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

    crc = str(hex(crc))[2:]

    #append CRC to beginning
    packet = crc + packet

    return packet



def construct_lora_ml_string(Packet): 
    payload = []
    payload.append("ml")#packet type
    payload.append(Packet.node_id)
    payload.append(Packet.message_id)
    payload.append(Packet.hopcount)
    payload.append(Packet.retry)
    payload.extend(Packet.payload.to_array())

    string = parse_tx_msg(payload)

    return string
  
def construct_lora_heartbeat_string(Packet):
    payload = []
    payload.append("hb")#packet type
    payload.append(Packet.node_id)
    payload.append(Packet.message_id)
    payload.append(Packet.hopcount)
    payload.append(Packet.retry)    
    payload.extend(Packet.payload.to_array())

    string = parse_tx_msg(payload)

    return string


def construct_lora_ack_string(Packet):
    payload = []
    payload.append("ack")
    payload.append(Packet.node_id)
    payload.append(Packet.message_id)

    string = parse_tx_msg(payload)

    return string


def lora_init(ser):
    #software reset
    software_reset(ser)


    

def uart_process(packet_tx_q, packet_rx_q):

    #init uart_q consists of tx strings and ack strings  (+Reset, +OK, +READY)
    uart_q = Queue()
    
    #initialize uart
    ser = serial.Serial('/dev/serial0', baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS
                        )

    #Current Transmitted/Ack String
    curr_uart = None
    #Current Ack Index
    curr_ack_index = 0
    #Timestamp used for retrying, when an ack wasnt received
    curr_ack_ts = None
    

    while(1):

#process rx strings
        if (ser.inWaiting() > 0):

            rx_data = ser.readline()

            #check for error
            if (rx_data[:4] == "+ERR"):
                print("Error detected: " + data)
                ##ADD reset module prob... will have to test and see types of errors

            #check for receive message
            elif (rx_data[:4] == "+RCV"):
                print("Message Received: " + data)
                ##process receive messages
                payload = parse_rx_msg(rx_data[4:-2]) #remove\r\n , need to check if they are there ADD
                packet = construct_packet_from_list(payload)
                packet_rx_q.put(packet)
                
                
            #ack message
            elif (curr_uart != None):
                #check if received msg is first element in ack list for that command
                if (data[:len(curr_uart.ack_list[curr_ack_index])] == curr_uart.ack_list[curr_ack_index]):

                    #check if more acks to process
                    if (len(curr_uart.ack_list) == curr_ack_index+1):
                        curr_ack_ts = None
                        curr_uart = None
                        curr_ack_index = 0
                    #waiting on more acks from same tx msg
                    else:
                        #reset ack ts
                        curr_ack_ts = time.time()
                        curr_ack_index += 1

            
####process tx strings
        #check if not waiting on ack
        if (curr_uart == None) and (uart_q.empty() == False):

            curr_uart = uart_q.get()
            curr_ack_index = 0
            curr_ack_ts = time.time()

            ser.write(curr_uart.tx_string.encode())
        #check if ack timed out
        elif (time.time() - curr_ack_ts >= 5): #5 sec has passed since string has been sent
                #resend transmit, reset ack index, and ts
                curr_ack_index = 0
                curr_ack_ts = time.time()
                
                ser.write(curr_uart.tx_string.encode())
        
####process tx packets from com_process             
        if (packet_tx_q.empty() == False):
            packet = packet_tx_q.get()

            if (packet.get_type() == "ML_CLASS"):
                string = construct_lora_ml_string(packet)
                lora_transmit(uart_q, False, Packet.node_id, string)
                
            elif (packet.get_type() = "HEART_BEAT"):
                string = construct_lora_heartbeat_string(packet)
                lora_transmit(uart_q, False, Packet.node_id, string)

            elif (packet.get_type() == "ACK"):
                string = construct_lora_ack_string(packet)
                lora_transmit(uart_q, False, Packet.node_id, string)

                
                




