#!/bin/bash
http://4share.vn/f/487c7d7b7c7f797c/

pyInoC=$(egrep '(REMOVING|DELETED)' ~/IOT-USTH/test.txt)

function GET_CD()
{
    echo -e "$pyInoC\n"
}
echo $(GET_CD)

