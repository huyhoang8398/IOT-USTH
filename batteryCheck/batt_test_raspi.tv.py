#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
# explained here...
# http://raspi.tv/2013/controlled-shutdown-duration-test-of-pi-model-a-with-2-cell-lipo
# DO NOT use this script without a Voltage divider or other means of 
# reducing battery voltage to the ADC. This is exaplained on the above blog page
import time
import os
import subprocess
import smtplib
import string
import RPi.GPIO as GPIO
from time import gmtime, strftime

GPIO.setmode(GPIO.BCM)

################################################################################
######################### Program Variables you MUST SET #######################
# email variables
fromaddr = 'your_gmail_account@gmail.com'  
toaddr  = 'destination email address'  
# Googlemail login details
username = 'your googlemail/gmail username'  
password = 'your googlemail/gmail password' 

########## Program variables you might want to tweak ###########################
# voltage divider connected to channel 0 of mcp3002
adcs = [0] # 0 battery voltage divider
reps = 10 # how many times to take each measurement for averaging
cutoff = 7.5 # cutoff voltage for the battery
previous_voltage = cutoff + 1 # initial value
time_between_readings = 60 # seconds between clusters of readings

# Define Pins/Ports
SPICLK = 8             # FOUR SPI ports on the ADC 
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

####### You shouldn't need to change anything below here #######################
################################################################################

# read SPI data from MCP3002 chip, 2 possible adc's (0 & 1)
# this uses a bitbang method rather than Pi hardware spi
# modified code based on an adafruit example for mcp3008
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 1) or (adcnum < 0)):
        return -1
    if (adcnum == 0):
        commandout = 0x6
    else:
        commandout = 0x7

    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout <<= 5    # we only need to send 3 bits here
    for i in range(3):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:   
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout /= 2       # first bit is 'null' so drop it
    return adcout

# this function creates and logs to a file called battery_log.txt
# you can change the name if you want, but you'll have to change line 98 as well
def write_log(logline):
    logfile = open('battery_log.txt', 'a')
    logfile.write(logline + '\n')
    logfile.close()

# you can edit the text for the email to suit your requirements
def send_email():
    BODY = string.join((
        "From: %s" % fromaddr,
        "To: %s" % toaddr,
        "Subject: Shutting down the model A now",
        "",
        "Your battery voltage was just measured at or below threshold.",
        "If it happens twice in a row, we shut down.",
        ), "\r\n")
      
    # send the email  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, toaddr, BODY)  
    server.quit()

#Set up ports
GPIO.setup(SPIMOSI, GPIO.OUT)       # set up the SPI interface pins
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# create log file
item = 'Battery log data'
logfile = open('battery_log.txt', 'w')
logfile.write(item + '\n')
logfile.close()

try:
    while True:
        for adcnum in adcs:
            # read the analog pin
            adctot = 0
            for i in range(reps):
                read_adc = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
                adctot += read_adc
                time.sleep(0.05)
            read_adc = adctot / reps / 1.0
            print read_adc

            # convert analog reading to Volts = ADC * ( 3.33 / 1024 )
            # 3.33 tweak according to the 3v3 measurement on the Pi
            volts = read_adc * ( 3.33 / 1024.0) * 2.837
            voltstring = str(volts)[0:5]
            print "Battery Voltage: %.2f" % volts
            # now we need to log the time and voltage in the log file
            logline = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            logline += ', '
            logline += voltstring
            print "adding %s to log file" % logline

            write_log(logline)
            # put safeguards in here so that it takes 2 or 3 successive readings
            if volts <= cutoff:
                # get it to send you an email at this point before full cutoff
                try:
                    send_email()
                    print "email sent"
                except:
                    print "email failed"
                if previous_voltage <= cutoff:
                    logline = 'Shutting down due to low V at '
                    logline += str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                    write_log(logline)
                    # initiate shutdown process
                    print "OK. Syncing file system, then we're shutting down."
                    command = os.system("sync")
                    command = 0
                    if command == 0:
                        print "we're shutting down now"
                        command = "/usr/bin/sudo /sbin/shutdown -h now"
                        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                        output = process.communicate()[0]
                        print output     
            previous_voltage = volts               
        time.sleep(time_between_readings)

except KeyboardInterrupt:             # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()
    time.sleep(5)
GPIO.cleanup()
