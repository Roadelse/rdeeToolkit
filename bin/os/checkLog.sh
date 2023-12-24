#!/bin/bash

warning=0
while getopts "w" arg
do
    case $arg in
        w)
            warning=1;;
    esac
done


if [[ $warning == 0 ]]; then
    grep -Pi '(error|wrong|fail|fault)' $*
else
    grep -Pi '(error|wrong|fail|fault|warning)' $*
fi
