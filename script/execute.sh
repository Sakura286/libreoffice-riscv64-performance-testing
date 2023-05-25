#!/bin/bash
# LibreOffice performance script
#
# ATTENTION: Before running the script, you need to close 
# the everyday-tips and enable macros.
# 
# To enable macros, do Tools -> Options -> LibreOffice -> Security
# -> Macro Security -> Security Level -> Low

# Modify this to souce code of LibreOffice
export SRCDIR=/home/infinity/Desktop/core

export PYTHONPATH=$SRCDIR/instdir/program
export PYTHONPATH=$PYTHONPATH:$SRCDIR/unotest/source/python
export URE_BOOTSTRAP=file://$SRCDIR/instdir/program/fundamentalrc
export SAL_USE_VCLPLUGIN=gen
export TDOC=/home/infinity/Desktop/libreoffice-riscv64-performance-testing/resource
export TestUserDir=file:///tmp
export LC_ALL=C

rm -rf /tmp/libreoffice/4
rm -f test_result.txt

python3 "$SRCDIR/uitest/test_main.py" --soffice=path:"$SRCDIR/instdir/program/soffice"  --userdir=file:///tmp/libreoffice/4 --file=/home/infinity/Desktop/libreoffice-riscv64-performance-testing/script/uitest.py

killall soffice.bin