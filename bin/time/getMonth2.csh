#!/bin/csh

set date = `2d $1`
@ month = $date / 100 % 100

if ($month < 10) then
  echo 0$month
else
  echo $month
endif
