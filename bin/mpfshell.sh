#!/bin/bash

PACKAGE=mpfshell
VIRTUAL_ENV_DIR=$HOME/.virtualenvs/$PACKAGE
VIRTUAL_ENV_ACTIVATE=$VIRTUAL_ENV_DIR/bin/activate

THIS_SCRIPT_DIR=`dirname $0`
MPF_SCRIPT_DIR=$THIS_SCRIPT_DIR/../externals/$PACKAGE

if [ ! -d $VIRTUAL_ENV_DIR -o ! -r $VIRTUAL_ENV_ACTIVATE ]
then
    echo "Directory $VIRTUAL_ENV_DIR is not found or $VIRTUAL_ENV_ACTIVATE can't be read."
    echo "Use virtualenvwrapper for creating it:"
    echo "  mkvirtualenv -p /usr/bin/python3 $PACKAGE"
    echo "And install needed packages:"
    echo "  pip install -r $MPF_SCRIPT_DIR/requirements.txt"
    exit 1
fi

# activate virtual environment
source $VIRTUAL_ENV_ACTIVATE

# and run it
$MPF_SCRIPT_DIR/$PACKAGE $*

