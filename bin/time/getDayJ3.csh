#!/bin/csh

set date = `2j $1`

@ dayj = $date % 1000

if ( $dayj < 10 ) then
    echo 00$dayj
else if ( $dayj < 100 ) then
    echo 0$dayj
else
    echo $dayj
endif
