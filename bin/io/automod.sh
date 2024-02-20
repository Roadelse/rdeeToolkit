#!/bin/bash

#@ <Introduction>
# This script aims to collect modulefiles automatically
#@ </Introduction>

wdir=${PWD}

if [[ `basename $wdir` != "modulefiles" ]]; then
    echo "This script should be run in a directory named \033[33m modulefiles \033[0m"
    exit 1
fi

for d in "$@"; do
    dname=`basename $d`  #@ exp dname -> directory name
    
done