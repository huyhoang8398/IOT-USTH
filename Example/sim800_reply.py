#!/usr/bin/python
import serial
import time
password = ["2", "4", "6", "8"]
port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=5.0)
port.write("AT\n\r")
time.sleep(.1)
x = port.read(port.inWaiting())

if x[-4:-2]!="OK":
    print ("Critical Error Sim800 not detected!")
    print ("No 'OK' code found at end of message or no message")
    print ("******message********")
    print (x)
    print ("********end**********")
    quit()

print ("Sim800 Successfully Detected!")

#begin actual code....
def swfc ( tosend, tofind, wait = 2 ):
    "string Send and Wait For Characters from sim800"
    port.write(tosend)
    endtime = time.time() + wait
    keylength = len (tofind)
    x = ""

    while (time.time() < endtime):
         if port.inWaiting():
             x += port.read()
         if len(x) >= keylength:
             if x[(0-keylength):] == tofind:
                 #print "Found key"
                 return 1
    print "Did not find: ", tofind, " in :", x
    return 0 #else

def command( torun ):
    torun += "\r\n"
    if swfc (torun, "OK"):
        print "Command: '%s' completed succesfully" % (torun[:-2])
        return 1
    else: 
        print "Command: '%s' failed" % (torun[:-2])
        return 0

def decodePassword():
    got=1
    for p in password:
        if (swfc('', "+DTMF: " , 15)):
            time.sleep(.1)
            c = port.read()
            print c
            if c != p:
                got = 0
        else:
            got = 0
    return got
 

# void setup() {
if \
command ("AT") and \
command ("AT+CSQ") and \
command ("AT+CMEE=1") and \
command ("AT+CPIN?") and \
command ("ATS0=1") and \
command ("AT+DDET=1") and \
command ("AT+CMIC=0,3") :
    print "" 
    print "Setup of Sim800 Completed Successfully"
else: quit()

#}
#void loop() {
while True:
    if swfc("AT+CPAS\r\n", "+CPAS: ") and port.read() == "4":
        print "Call Connected"
        print decodePassword()
        command ("ATH")
    time.sleep(.1)

