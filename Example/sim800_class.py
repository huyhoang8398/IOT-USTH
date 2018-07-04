import serial
import time
signalTable = [[2,-109,"Marginal"],[3,-107,"Marginal"],[4,-105,"Marginal"],[5,-103,"Marginal"],[6,-101,"Marginal"],[7,-99,"Marginal"],[8,-97,"Marginal"],[9,-95,"Marginal"],[10,-93,"OK"],[11,-91,"OK"],[12,-89,"OK"],[13,-87,"OK"],[14,-85,"OK"],[15,-83,"Good"],[16,-81,"Good"],[17,-79,"Good"],[18,-77,"Good"],[19,-75,"Good"],[20,-73,"Excellent"],[21,-71,"Excellent"],[22,-69,"Excellent"],[23,-67,"Excellent"],[24,-65,"Excellent"],[25,-63,"Excellent"],[26,-61,"Excellent"],[27,-59,"Excellent"],[28,-57,"Excellent"],[29,-55,"Excellent"],[30,-53,"Excellent"]]

class Sim800:
    def __init__(self, debug = 0):
        try:
            self.buf = ""
            self.debug = debug
            self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=5.0) #USB0 or AMA0
            self.port.write("AT\n\r")
            time.sleep(.1)
            x = self.port.read(self.port.inWaiting())
            if x[-4:-2]!="OK":
                raise Exception("NO OK!")
            print ("Sim800 Successfully Detected!")
            self.setup()
        except Exception as e:
            print ("Critical Error Sim800 not detected!")
            print ("No 'OK' code found at end of message or no message or other error!")
            print ("******message********")
            print (x)
            print ("********end**********")
            print "Error: " + str(e)
            quit()

    def swfc ( self, tosend, tofind, wait = 15 ):
        "string Send and Wait For Characters from sim800"
        self.port.write(tosend)
        endtime = time.time() + wait
        keylength = len (tofind)
        x = ""
    
        while (time.time() < endtime):
            if self.port.inWaiting():
                x += self.port.read()
            if len(x) >= keylength:
                 if x[(0-keylength):] == tofind:
                     if self.debug : print "Found key: ", tofind, " in: ", x
                     self.rec = x
                     return 1
        raise Exception("No: '" + tofind + "' found in '" + x + "' for command '" + tosend + "'" )
        return 0 #else

    def command( self, torun ):
        if torun != "AT":
            self.command("AT")

        torun += "\r\n"
        if self.swfc (torun, "OK"):
            if self.debug: print "Command: '%s' completed succesfully" % (torun[:-2])
            return 1
        else:
            if self.debug: print "Command: '%s' failed" % (torun[:-2])
            return 0

    def setup(self):
        try:
            self.command ("AT+CSQ;E0;+CMGD=1,2;+CMGF=1;+CMEE=2;+CPIN?;+DDET=1;+CMIC=0,3")
            #signal, echo off, delete sent and read, txt text mode, errors on
            #+cpin? - check pin, tone detect on, mic gain +4.5dB
            print "Setup of Sim800 Completed Successfully"
        except Exception as e: 
            print str(e)
            quit()

    def checkformsg(self, store = "REC UNREAD"):
        try: 
            self.command("AT+CMGL=" + '"' + store + '"' + ",0")
            #print self.rec
            self.rec = self.rec.lstrip()
            self.tempmsgs = self.rec.split("\r\n\r\n")
            if self.debug: print self.tempmsgs
            self.tempmsgs = self.tempmsgs[:-1]
            self.recmsgs = [] #+CMGL: 15,"REC READ","+6478270001","","16/10/07,13:07:26+52" example
            for msg in self.tempmsgs:
                msg = msg.split("\r\n")
                msg[0] = msg[0].split(",")
                msg[0][5] = msg[0][5].split("+")
                #print msg
                
                msgtime = time.strptime(msg[0][4][1:] + "," + msg[0][5][0], "%y/%m/%d,%H:%M:%S")
                msgtime = time.mktime(msgtime)
                self.recmsgs.append([msgtime, msg[0][2][1:-1], msg[1]])
            self.command("AT+CMGD=1,2")
            return self.recmsgs
        except Exception as e:
            print "****ERROR recmsgs" + str(e) + " END****"
            time.sleep(5)
            print "**Attemping Re-read**"
            return self.checkformsg("REC READ")
        
    def idle(self, phoneCall, textRecieved):
        if self.port.inWaiting():
            self.buf = self.port.readline()
            self.buf = self.buf.strip()
            if self.debug: print self.buf
            if self.buf[0:5] == "+CMTI":
                  textRecieved()
            elif self.buf[0:4] == "RING":
                  phoneCall()

    def call(self, number):
        self.command("ATD" + number + ";")

    def hangup(self):
        self.command("ATH")

    def textmsg(self, number, message):
        try:
            self.command("AT")
            self.swfc("AT+CMGS=\"" + number + "\"\r", ">")
            self.swfc(message + "\x1A", "OK", 30)
        except Exception as e:
            print "****ERROR sending " + str(e) + " END****"
            print "**Recovering**"
            try:
                self.swfc("\x1A" + "\r\nAT\r\n", "OK", 30)
                self.command("AT")
                self.textmsg(number, message)
            except Exception as e:
                print "****ERROR sendingmsgs" + str(e) + " END****"


    def checksignal(self):
        self.command("AT+CSQ")
        signal = self.rec.strip("\r\n").split("\r\n")
        signal[0] = signal[0].split(" ")
        signal[0][1] = signal[0][1].split(",")
        sig = int(signal[0][1][0])
        if self.debug: print signal
        for lookup in signalTable:
            if lookup[0] == sig:
                self.signal = lookup
        if self.debug: print self.signal
        return self.signal
