#!/bin/bash
# LibreOffice performance script
#
# ATTENTION: Before running the script, you need to run libreoffice one time
# to close the everyday-tips.



export SRC_BIN_DIR=$(dirname $(dirname $(readlink -e $(whereis -B /usr/bin -b libreoffice))))
export SRC_CODE_DIR=/home/infinity/Desktop/core
export SCRIPT_PATH=$(pwd)

export PYTHONPATH=$SRC_BIN_DIR/program:$SRC_CODE_DIR/unotest/source/python
export URE_BOOTSTRAP=file://$SRC_BIN_DIR/program/fundamentalrc
export SAL_USE_VCLPLUGIN=gen
export TDOC=$SCRIPT_PATH/resource
export TestUserDir=file:///tmp
export LC_ALL=C

#rm -rf /tmp/libreoffice/4
rm -f test_result.txt

python3 "$SRC_CODE_DIR/uitest/test_main.py" --soffice=path:"$SRC_BIN_DIR/program/soffice"  --userdir=file:///tmp/libreoffice/4 --file=$SCRIPT_PATH/script/uitest.py

killall soffice.bin
