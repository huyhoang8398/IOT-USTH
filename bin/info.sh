#!/bin/bash
str1="Images JPG:"
str2="Images PNG:"
str3="Free storage:"

#Linux command line 
avaiMem=$(df -h /tmp | tail -1 | awk '{print $4}')
notiF=$(find /home/pi/scann -mtime -1 -ls)
infoPng=$(find /home/pi/scann | grep .png | wc -l)
infoJpg=$(find /home/pi/scann | grep .jpg | wc -l)

#Read data from pyinotify log file. 
pyInoC=$(fgrep 'REMOVING' ~/IOT-USTH/test.txt)
pyInoD=$(fgrep 'DELETED' ~/IOT-USTH/test.txt)

function GET_MEM()
{
    echo -e "$str3 $avaiMem\n";  
}

function GET_WR()
{
    echo -e "$notiF\n";
}

function GET_PNG()
{
    echo -e "$str2 $infoPng\n";
}

function GET_JPG()
{
    echo -e "$str1 $infoJpg\n";
}

function GET_WRITED()
{
    echo -e "$pyInoC\n";
}

function GET_DELETED()
{
    echo -e "$pyInoD\n";
}

# Write date, time > overwrite all files data
date > /home/pi/log1.txt

#printf "`echo $str1` `find /Users/huyhoang8398/Pictures | grep .jpg | wc -l`\n" >> /Users/huyhoang8398/test.txt
#printf "`echo $str2` `find /Users/huyhoang8398/Pictures | grep .png | wc -l`\n" >> /Users/huyhoang8398/test.txt

# Echo output to textfile without overwrite date time 
echo $(GET_JPG) >> /home/pi/log1.txt
echo $(GET_PNG) >> /home/pi/log1.txt
echo $(GET_MEM) >> /home/pi/log1.txt
echo $(GET_WR) >> /home/pi/log1.txt
echo $(GET_WRITED) >> /home/pi/log1.txt
echo $(GET_DELETED) >> /home/pi/log1.txt


