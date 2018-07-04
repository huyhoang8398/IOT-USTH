import serial
import time

port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=5.0)
port.write("AT\n\r")
time.sleep(.1)
x = port.read(port.inWaiting())
print (x)
if x[-4:-2]=="OK":
    print ("Good all working well :)")
