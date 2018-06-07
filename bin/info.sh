#!/bin/bash
str1="Images JPG:"
str2="Images PNG:"
str3="Free storage:"
myAvai=$(df -h /tmp | tail -1 | awk '{print $4}')
myIfy=$(find /Users/huyhoang8398/Desktop/scann -mtime -1 -ls)

function GET_OUTPUT()
{
    echo -e "$str3 $myAvai\n";  
}
function OUTPUT_IFY()
{
    echo -e "$myIfy\n";
}

date > /Users/huyhoang8398/test.txt
printf "`echo $str1` `find /Users/huyhoang8398/Pictures | grep .jpg | wc -l`\n" >> /Users/huyhoang8398/test.txt
printf "`echo $str2` `find /Users/huyhoang8398/Pictures | grep .png | wc -l`\n" >> /Users/huyhoang8398/test.txt
echo $(GET_OUTPUT) >> /Users/huyhoang8398/test.txt
echo $(OUTPUT_IFY) >> /Users/huyhoang8398/test.txt



