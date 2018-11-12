#!/bin/bash

# Wraps pyboard.py providing it with another default device. User can overwrite if he wants
# by adding own --device...

THIS_SCRIPT_DIR=`dirname $0`
TOOLS_DIR=$THIS_SCRIPT_DIR/../externals/micropython/tools

$TOOLS_DIR/pyboard.py --device=/dev/ttyUSB0 $*

