import serial
from multiprocessing import queue
import time



class rx_msg:
    address = 0
    length = 0
    data = ""
    ts = 0

class event_msg:


                  

def parse_rx_msg(data):

    rx_obj = rx_msg()
    rx_msg.ts = time.time()
    
    data = data[5:]
    split_data = data.split(",")

    rx_obj.address = int(split_data[0])
    rx_obj.length = int(split_data[1])
    rx_obj.data = (split_data[2]).encode() #convert ascii to int array


    #first check length is 240
    if (rx_obj.length != 240):
        return False

    #Compute CRC32 and make sure its not corrupted
    crc32 = (rx_obj.data)[-4:]
        #add CRC computation
    
    if (computed_crc32 != crc32):
        return False

    #check signature

    

def uart_process(tx_q, rx_event_q, rx_cmd_q):

    #initialize uart
    ser = serial.Serial('/dev/serial0', baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS
                        )
    


    while(1):
        #process transmit
        if (tx_q.empty() == False):
            ser.write((tx_q.get()).encode())
        

        #process receive
        if (ser.inWairing() > 0):
            data = ser.readline()


            #check for error
            if (data[:4] == "+ERR"):
                print("Error detected: " + data)

            #check for receive message
            else if (data[:4] == "+RCV"):
                print("Message Received: " + data)
                
