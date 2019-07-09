import serial
import time

print ("Starting uart stream between RPI Cosole and UART port")


ser = serial.Serial('/dev/serial0', baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )


while (1):
	try:
		#input string from console
		console_in = input("$ ") #

		#append \r\n characters
		console_in = console_in + "\r\n"
		ser.write(console_in.encode())

		while(1):
			if (ser.inWaiting() > 0):
				data = ser.readline()
				print (data)
				break;

	except KeyboardInterrupt:
		print ("Exiting Program")
		ser.close()
		break;


