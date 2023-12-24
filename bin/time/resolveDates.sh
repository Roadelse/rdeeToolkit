#!/bin/bash


datesDef=$1

ymdps=(${datesDef//,/ })   # yyyymmdd parts

res=()

for ymdp in ${ymdps[@]}
do
    if [[ ${ymdp//-/ } == ${ymdp} ]]; then
        res+=($ymdp)
    else  # ymd range
        ymdp_arr=(${ymdp//-/ })
        ymdp_start=${ymdp_arr[0]}
        ymdp_end=${ymdp_arr[1]}
        ymdp_poi=$ymdp_start
        while [[ $ymdp_poi -le $ymdp_end ]]; do
            res+=($ymdp_poi)
            ymdp_poi=`date -d "$ymdp_poi + 1 days" +%Y%m%d`
        done
    fi

done

echo ${res[@]}