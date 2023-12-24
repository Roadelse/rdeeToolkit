#!/bin/csh

set date = `2d $1`
@ month = $date / 100 % 100

echo $month

