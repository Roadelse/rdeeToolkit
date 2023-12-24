#!/bin/csh

set Date = `2d $1`
set prevD = `date -d "$Date -1 days" +%Y%m%d`
echo $prevD
