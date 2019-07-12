import os
import serial
from uart_process import serial

#software reset 
def software_reset(tx_q):
    input = "AT+RESET\r\n"
    tx_q.add(input)

    #expecting +RESET
    #expecting +READY

#set to transmit and receive mode
def set_work_mode(tx_q): 
    input = "AT+MODE=0\r\n"
    tx_q.add(input)

   #expecting +OK
            
#set UART Baud rate
def set_uart_baud(tx_q):
    input = "AT+IPR=115200\r\n"
    tx_q.add(input)

    #expecting +OK

#set RF parameter (all default parameters)
def set_rf_params(tx_q):
    input = "AT+PARAMETER=12,7,1,4\r\n"
    tx_q.add(input)

    #expecting +OK

#set rf frequency
def set_rf_frequency(tx_q):
    input = "AT+BAND=915000000\r\n"
    tx_q.add(input)

    #expecting +OK
            
#set AT address (1 to 65535)
def set_at_address(tx_q, addr):
    if ((count < 1) or (count > 65535)):
        return False
    
    input = "AT+ADDRESS=" + str(addr) + "\r\n"
    tx_q.add(input)

    #expecting +OK


#def set Network ID
def set_network_id(tx_q, id):
    
    input = "AT+NETWORKID=" + str(id) + "\r\n"
    tx_q.add(input)

    #expecting +OK

#set AES128 password of the network
def set_network_pass(tx_q):
    input = "AT+CPIN=50AE32A0FCF3BD155E280013DFAB5CAB\r\n"

    tx_q.add(input)

    #expecting +OK


#set the rf ouput power
def set_rf_output_pwr(tx_q):
    input = "AT+CRFOP=15\r\n"

    tx_q.add(input)

    #expecting +OK

#transmit data
# @transmit_all is false when sending to a specific address, else true
# @address is specific address you want to send to
# @datastring is string you want to send has to be less than 240 char in string format
def transmit(tx_q, transmit_all, address, datastring):

    if (len(datastring) > 240):
        return False

    if (transmit_all == True):
        input = "AT+SEND=0," +str(len(datastring)) + "," + datastring

    else:
        input = "AT+SEND=" + str(address) + "," + str(len(datastring)) + "," + datastring
    tx_q.add(input)


