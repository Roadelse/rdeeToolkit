#!/bin/bash

myLoc=`readlink -f ${BASH_SOURCE[0]}`
myDir=`dirname $myLoc`

source $myDir/../include/sizeSum.sh


humanMode=0
while getopts "h" arg
do
    case $arg in 
        h)
            humanMode=1;;
    esac
done

# echo humanMode=$humanMode

if [[ $humanMode == 1 ]]; then
    # echo ${*:1}
    totalSize=`ls -l ${*:2} | awk 'BEGIN{sum=0}{sum += $5;}END{print sum}'`
    # echo totalSize=$totalSize
    sizeHuman=`byte2Human $totalSize`
    echo $sizeHuman
else
    totalSize=`ls -l $* | awk 'BEGIN{sum=0}{sum += $5;}END{print sum}'`
    echo $totalSize
fi