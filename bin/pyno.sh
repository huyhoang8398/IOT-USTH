#!/bin/bash

pyInoC=$(egrep '(REMOVING|DELETED)' ~/IOT-USTH/test.txt)

function GET_CD()
{
    echo -e "$pyInoC\n"
}
echo $(GET_CD)

