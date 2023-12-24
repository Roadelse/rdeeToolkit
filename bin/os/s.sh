#!/bin/bash

# echo ${PWD} > ~/.path

sFile=$pathSG_re

curP=${PWD}

if [[ $1 == "" ]]; then
    sFlag="main"
else
    sFlag=$1
fi

if [[ $sFlag == "list" ]]; then
    echo "cannot take 'list' as the save-flag!"
    exit 0
fi


declare -A fpDict  # flag-path dict

if [[ -e $sFile ]]; then
    strT=`cat $sFile`
    eval "fpDict=$strT"
    fpDict[$sFlag]=$curP
else
    fpDict[$sFlag]=$curP
fi

sps_str='('         # saved paths
for i in ${!fpDict[@]}
do
    sps_str+="[$i]=${fpDict[$i]} "
done
sps_str+=')'

echo "$sps_str" > $sFile
