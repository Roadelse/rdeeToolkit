#!/bin/csh

set date = $1

set len = $%date
#echo $len
if ($len == 7) @ year = $date / 1000
if ($len == 8) @ year = $date / 10000

echo $year
