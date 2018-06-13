#!/bin/bash
cronJob=$(ps aux | grep inowait.sh | grep -v "grep" | awk '{print $2}')
kill -9 $cronJob
