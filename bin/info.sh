#!/bin/bash
str1="Images JPG:"
str2="Images PNG:"
date > /Users/huyhoang8398/test.txt
printf "`echo $str1` `find /Users/huyhoang8398/Pictures | grep .jpg | wc -l`\n" >> /Users/huyhoang8398/test.txt
printf "`echo $str2` `find /Users/huyhoang8398/Pictures | grep .png | wc -l`" >> /Users/huyhoang8398/test.txt
