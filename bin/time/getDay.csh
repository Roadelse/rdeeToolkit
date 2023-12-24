#!/bin/csh

set date = `2d $1`
@ day = $date % 100

echo $day
