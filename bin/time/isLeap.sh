#!/bin/bash

year=$1

if [ `expr $year % 400` -eq 0 ]; then
    echo 1
elif [ `expr $year % 100` -eq 0 ]; then
    echo 1
elif [ `expr $year % 4` -eq 0 ]; then
    echo 1
else
    echo 0
fi