#!/bin/bash
date > /Users/huyhoang8398/test.txt
printf "`echo Images JPG:` `find /Users/huyhoang8398/Pictures | grep .jpg | wc -l`\n" >> /Users/huyhoang8398/test.txt
printf "`echo Images PNG:` `find /Users/huyhoang8398/Pictures | grep .png | wc -l`" >> /Users/huyhoang8398/test.txt
