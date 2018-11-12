#!/bin/bash

THIS_DIR=`dirname $0`
ESP_DIR=$THIS_DIR/../externals/micropython/ports/esp8266

cd $ESP_DIR
make clean && make && make PORT=/dev/ttyUSB0 BAUD=460800 deploy
