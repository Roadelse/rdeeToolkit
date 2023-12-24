#!/bin/csh

set date = `2d $1`
@ day = $date % 100
if ($day < 10) then
  echo 0$day
else
  echo $day
endif
