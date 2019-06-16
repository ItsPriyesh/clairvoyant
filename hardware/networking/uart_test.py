import serial

print "Starting uart stream between RPI Cosole and UART port"


ser = serial.Serial('/dev/ttyAMA0', baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )

time.sleep(1)

while:
	try:
		#input string from conolse
		console_in = input("$ ") #

		#append \r\n characters
		ser.write("console_in")

		print(console_in)
	   
	    while True:
	        if ser.inWaiting() > 0:
	            data = ser.read()
	            print data
	        
	except KeyboardInterrupt:
	    print "Exiting Program"

	except:
	    print "Error Occurs, Exiting Program"

	finally:
	    ser.close()
