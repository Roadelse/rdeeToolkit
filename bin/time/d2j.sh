#!/bin/bash


if [[ $1 =~ ^[0-9]{8}$ ]]; then
    echo `date -d $1 +%Y%j`
else
    echo "unknown date : $1"
    echo "should look like YYYYMMDD, such as 20190101"
    exit 1
fi