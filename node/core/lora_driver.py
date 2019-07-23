import os
import serial
import time

class LoraString:
    tx_string = ""
    ack_list = []
    
#software reset 
def software_reset(uart_q):

    input = "AT+RESET\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+RESET", "+READY"]

    uart_q.put(string)
        
#set to transmit and receive mode
def set_work_mode(uart_q): 
    input = "AT+MODE=0\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)

   #expecting +OK
            
#set UART Baud rate
def set_uart_baud(uart_q):
    input = "AT+IPR=115200\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)
    #expecting +OK

#set RF parameter (all default parameters)
def set_rf_params(uart_q):
    input = "AT+PARAMETER=12,7,1,4\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)
    #expecting +OK

#set rf frequency
def set_rf_frequency(uart_q):
    input = "AT+BAND=915000000\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)
    #expecting +OK
            
#set AT address (1 to 65535)
def set_at_address(uart_q):
    if ((count < 1) or (count > 65535)):
        return False
    
    input = "AT+ADDRESS=" + str(addr) + "\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)
    #expecting +OK


#def set Network ID
def set_network_id(uart_q):
    
    input = "AT+NETWORKID=" + str(id) + "\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)

    #expecting +OK

#set AES128 password of the network
def set_network_pass(uart_q):
    input = "AT+CPIN=50AE32A0FCF3BD155E280013DFAB5CAB\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)
    #expecting +OK


#set the rf ouput power
def set_rf_output_pwr(uart_q):
    input = "AT+CRFOP=15\r\n"

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)

    #expecting +OK

def lora_init(uart_q):
    software_reset(uart_q)
    set_work_mode(uart_q)
    set_uart_baud(uart_q)
    set_rf_params(uart_q)
    set_rf_frequency(uart_q)
    set_at_address(uart_q)
    set_network_id(uart_q)
    set_network_pass(uart_q)
    set_rf_output_pwr(uart_q)

#transmit data
# @transmit_all is false when sending to a specific address, else true
# @address is specific address you want to send to, can be null if transmit all is used
# @datastring is string you want to send has to be less than 240 char in string format
def lora_transmit(uart_q, transmit_all, address, datastring):
    if (len(datastring) > 240):
        return False

    if (transmit_all == True):
        input = "AT+SEND=0," +str(len(datastring)) + "," + datastring

    else:
        input = "AT+SEND=" + str(address) + "," + str(len(datastring)) + "," + datastring

    string = LoraString()
    string.tx_string = input
    string.ack_list = ["+OK"]

    uart_q.put(string)


