#!/bin/csh

set Date = `2d $1`
set nextD = `date -d "$Date +1 days" +%Y%m%d`
echo $nextD
