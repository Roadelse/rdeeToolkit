#!/bin/bash

mks=`find ${PWD} -iname Makefile`
for mk in ${mks[@]}
do 
    echo $mk
    cd `dirname $mk`
    make clean
done
