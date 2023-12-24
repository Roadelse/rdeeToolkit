#!/bin/csh

set date = `2j $1`

@ dayj = $date % 1000

echo $dayj
