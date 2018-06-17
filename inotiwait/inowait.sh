#!bin/bash
inotifywait -e delete,create -m -r --exclude ./(tmp\|swp\|swx\|) --timefmt '%F-%T' --format '%:e | %f | %T' /home/huyhoang8398/scann -o /home/huyhoang8398/test.txt

