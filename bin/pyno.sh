#!/bin/bash

pyInoC=$(egrep '(CREATED|DELETED)' ~/IOT-USTH/test.txt)

function GET_CD()
{
    echo -e "$pyInoC\n"
}


