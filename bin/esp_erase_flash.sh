#!/bin/bash

cmd="esptool.py --port /dev/ttyUSB0 erase_flash"

if [ x"$1" != x"erase" ]
then
    echo "Usage: $0 <erase>"
    echo "Executes command: $cmd"
    exit 1
fi

$cmd

