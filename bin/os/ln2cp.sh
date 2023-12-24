#!/bin/bash

realFile=`readlink -f $1`
rm $1
cp -r $realFile $1

