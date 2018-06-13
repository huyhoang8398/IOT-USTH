# IOT USTH

## Team 

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
* Linux ≥ 2.6.13
* Python ≥ 2.4 (including Python 3.x)
* Bash
* Gammu
* An USB Huawei Dcom or GSM module 800l

## Hardware 
Python 2.7 code to interface a cheap 2G SIM800L to a cheap Raspberry Pi 3

| <a href=""><img src="https://github.com/huyhoang8398/IOT-USTH/blob/master/images/ban_raspberry_pi_3-850x784.jpg" width="200" /></a> | <a href=""><img src="https://github.com/huyhoang8398/IOT-USTH/blob/master/images/SIM800L.jpg" width="200" /></a> |
|-|-|

## Connections

- Hook up the SIM800 to the Pi Zero with a few wires:

| <img src="https://github.com/huyhoang8398/IOT-USTH/blob/master/images/SIM800L.sides.jpg" width="450" /> |  <img src="https://github.com/huyhoang8398/IOT-USTH/blob/master/images/Raspberry-Pi-GPIO.2.png" width="800" />  |
|-|-|

| SIM800 Pin | Pi Zero Pin |
| --- | --- |
| 5V | Pin 2 - 5V |
| GND | Pin 6 - GND |
| VDD | Pin 4 - 5V |
| TX | Pin 10 - GPIO15 - RX |
| RX | Pin 8 - GPIO14 - TX |
| GND | Pin 14 - GND |
| RST | Pin - |
|-|-|

- Insert your SIM card into the SIM800

## Install Gammu (python-gammu and gammu-smsd can be skipped - depending on requirements)
Check python is installed on your computer 
```bash
python --version
python3 --version
```
Use command
```bash
sudo apt-get update & apt-get upgrade 

sudo apt-get install gammu
sudo apt-get install python-gammu
sudo apt-get install gammu-smsd
sudo apt-get install libgammu-dev
```

## Find port USB device connected to 
Connect your DCOM to your Raspberry Pi then:
```bash
dmesg | grep tty
```
[7.578478] usb 1-1.2: GSM modem (1-port) converter now attached to ttyUSB0<br />
[7.697942] usb 1-1.2: GSM modem (1-port) converter now attached to ttyUSB1

## Config gammu
```bash
gammu-config
```
set port /dev/ttyUSB0
```bash
sudo gammu-config
```
set port /dev/ttyUSB0
## Check connected
```bash
sudo gammu --identify
```
Device               : /dev/ttyUSB0<br />
Manufacturer         : Huawei<br />
Model                : E220 (E220)<br />
Firmware             : 11.117.03.01.156<br />
IMEI                 : 3XX19301XXXXXX3<br />
SIM IMSI             : 2XXXX923271XXX1

## Test with a text message
```bash
echo "some message" | gammu --sendsms TEXT 07921XXXXXX
```

## Run this app
```bash
git clone https://github.com/huyhoang8398/IOT-USTH
cd IOT-USTH
cd GSM
python GSM.py
```

## Pyinotify 
### Install
#### Get the current stable version from PyPI and install it with pip

To install pip follow http://www.pip-installer.org/en/latest/installing.html
```bash
sudo pip install pyinotify
```

### Watch a directory
Install pyinotify and run this command from a shell:
```bash
    $ python -m pyinotify -v /my-dir-to-watch
```

### Run this script from Pi
```bash
git clone https://github.com/huyhoang8398/IOT-USTH
cd IOT-USTH
cd pyinotify
python inotify.py >> /home/pi/scann/test.txt
```
Test the result 
```bash
cd /home/pi/scann
touch test.jpg
vi test.txt
```
## Auto run at start up with crontab
```bash
sudo apt-get install crontab
```
To config crontab use:
```bash
crontab -e
```

## Added script files
```bash
cd bin
chmod +x info.sh
./info.sh
```
## Upgrade 15/06/2018
```bash
sudo apt-get install inotifytools
inotifywait -e modify,delete,create -m -r --timefmt '%F-%T' --format '%:e | %f | %T' <watch-dir> -o <output-file>
```
