#!/bin/bash
str1="Images JPG:"
str2="Images PNG:"
str3="Free storage:"
myAvai=$(df -h /tmp | tail -1 | awk '{print $4}')
date > /Users/huyhoang8398/test.txt
printf "`echo $str1` `find /Users/huyhoang8398/Pictures | grep .jpg | wc -l`\n" >> /Users/huyhoang8398/test.txt
printf "`echo $str2` `find /Users/huyhoang8398/Pictures | grep .png | wc -l`\n" >> /Users/huyhoang8398/test.txt
echo "$str3 $myAvai" >> /Users/huyhoang8398/test.txt

