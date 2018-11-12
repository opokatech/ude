#!/bin/bash

F=$1

if [ "x$F" == "x" ]
then
    echo "Usage: $0 <all|apps|ude|specific_file>"
    exit 1
elif [ "x$1" == "xall" ]
then
    echo "Uploading all"
    mpfshell.sh -c "mput app_.*\.py; put hwconfig.py; put main.py; put boot.py" -n -o ttyUSB0
    mpfshell.sh -c "md ude; cd ude; lcd ude; mput .*\.py" -n -o ttyUSB0

    THINGSPEAK=thingspeak.cfg
    WIFI=wifi.json

    for cfg in $THINGSPEAK $WIFI
    do
        if [ -f $cfg ]
        then
            echo "Uploading $cfg"
            mpfshell.sh -c "put $cfg" -n -o ttyUSB0
        fi
    done
elif [ "x$1" == "xapps" ]
then
    echo "Uploading apps"
    mpfshell.sh -c "mput app_.*\.py; put hwconfig.py; put main.py; put boot.py" -n -o ttyUSB0
elif [ "x$1" == "xude" ]
then
    echo "Uploading ude"
    mpfshell.sh -c "md ude; cd ude; lcd ude; mput .*\.py" -n -o ttyUSB0
else
    echo "Uploading $F"
    mpfshell.sh -c "put $F" -n -o ttyUSB0
fi

