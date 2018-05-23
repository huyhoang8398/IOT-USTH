#IOT USTH

##Team 

Members:
* Do Duy Huy Hoang
* Nguyen Dinh Mau

## Project
* Control raspberry Pi via smartphone
* Student internship: Set up a Raspberry Pi to send SMS notifications
* Features:
	- Number images record
	- Free storage capacity of SD card
	- Number images record
	- Power of the battery
	- ...(More to come!)

## Dependencies
* Python
* Bash
* Gammu

## Install Gammu (python-gammu and gammu-smsd can be skipped - depending on requirements)
Check python is installed on your computer 
```bash
python --version
python3 --version
```
Use command
```bash
sudo apt-get install gammu 
sudo apt-get update & apt-get upgrade 
apt-get install python-gammu
apt-get install gammu-smsd
```

# Find port USB device connected to 
```bash
dmesg | grep tty
```
[    7.578478] usb 1-1.2: GSM modem (1-port) converter now attached to ttyUSB0
[    7.697942] usb 1-1.2: GSM modem (1-port) converter now attached to ttyUSB1

# Config gammu
```bash
gammu-config
```
# Check connected
```bash
gammu --identify
```
Device               : /dev/ttyUSB0
Manufacturer         : Huawei
Model                : E220 (E220)
Firmware             : 11.117.03.01.156
IMEI                 : 3XX19301XXXXXX3
SIM IMSI             : 2XXXX923271XXX1

# Test with a text message
```bash
echo "some message" | gammu --sendsms TEXT 07921XXXXXX
```

#Run this app
```bash
git clone https://github.com/huyhoang8398/IOT-USTH
cd IOT-USTH
python internship.py
```# IOT-USTH
Intership, Python 
