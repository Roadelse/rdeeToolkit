#!/bin/bash

sFile=$pathSG_re

if [[ $1 == "" ]]; then
    sFlag="main"
else
    sFlag=$1
fi

declare -A fpDict  # flag-path dict

if [[ ! -e $sFile ]]; then
    echo "Error! s first, then go to s (g2s)"
    return 1
fi

strT=`cat $sFile`
eval "fpDict=$strT"



if [[ $sFlag == "list" ]]; then
    for i in ${!fpDict[@]}
    do
        echo "${i} : ${fpDict[$i]}"
    done
else
    tarP=${fpDict[$sFlag]}

    if [[ $tarP == "" ]]; then
        echo "Error! s <sFlag> first, then go to s (g2s <sFlag>)"
        return 2
    fi

    cd $tarP
fi
