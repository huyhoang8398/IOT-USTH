#!/bin/bash
str1="Images JPG:"
str2="Images PNG:"
str3="Free storage:"

#Linux command line 
avaiMem=$(df -h /tmp | tail -1 | awk '{print $4}')
notiF=$(find /Users/huyhoang8398/Desktop/scann -mtime -1 -ls)
infoPng=$(find /Users/huyhoang8398/Pictures | grep .png | wc -l)
infoJpg=$(find /Users/huyhoang8398/Pictures | grep .jpg | wc -l)

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
date > /Users/huyhoang8398/test.txt

#printf "`echo $str1` `find /Users/huyhoang8398/Pictures | grep .jpg | wc -l`\n" >> /Users/huyhoang8398/test.txt
#printf "`echo $str2` `find /Users/huyhoang8398/Pictures | grep .png | wc -l`\n" >> /Users/huyhoang8398/test.txt

# Echo output to textfile without overwrite date time 
echo $(GET_JPG) >> /Users/huyhoang8398/test.txt
echo $(GET_PNG) >> /Users/huyhoang8398/test.txt
echo $(GET_MEM) >> /Users/huyhoang8398/test.txt
echo $(GET_WR) >> /Users/huyhoang8398/test.txt
echo $(GET_WRITED) >> /Users/huyhoang8398/test.txt
echo $(GET_DELETED) >> /Users/huyhoang8398/test.txt


