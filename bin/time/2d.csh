#!/bin/csh 

if ($%1 == 8) echo $1
if ($%1 == 7) then
set julianD = $1
#echo $julianD
@ year = $julianD / 1000
@ day = $julianD % 1000 - 1
set yyyyjjj = `date -d "${year}0101 + $day days" +%Y%m%d`
echo $yyyyjjj
endif
