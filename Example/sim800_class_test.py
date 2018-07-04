#!/usr/bin/python
import sim800_class
import time

sim = sim800_class.Sim800(0)

def phoneCall():
    print "Call Waiting"

def textMsg():
    print "Checking for messages"
    msgs = sim.checkformsg()
    if not msgs:
        return 0
    for msg in msgs:
        x = "*****Recieved message: ******************************\n\r"
        msgtime = time.localtime(msg[0])
        x += "Time: " + str(msgtime[3]) + ":" + str(msgtime[4]) + ":" + str(msgtime[5])
        x += " on the: " + str(msgtime[2]) + "/" + str(msgtime[1]) + "/" + str(msgtime[0]) + "\r\n"
        x += "From: " + msg[1] + "\r\n"
        x += "******msg*******\r\n"
        x += msg[2]
        x += "\r\n************************end**************************\r\n"
        print x
    sim.textmsg("777", "BAL")

sim.checksignal()
print "Signal is: " + str(sim.signal[0]) + " that is: " + str(sim.signal[1]) + "dB and condition " + str(sim.signal[2])

#sim.textmsg("+64210332570", "Helllllooo")
#sim.call("+64210332570")
sim.textmsg("777", "BAL")
while True:
    sim.idle(phoneCall, textMsg)
