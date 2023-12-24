#!/bin/bash

#filesWC=$*
#files=(`ls $filesWC`)

#for f in ${files[@]}

for f in $*
do
#    echo $f
    shasum $f
done
