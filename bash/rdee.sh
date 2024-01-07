#!/bin/bash


fPath=$(cd $(dirname "${BASH_SOURCE[0]}") && readlink -f .)

source $fPath/_basic.sh
source $fPath/_io.sh
source $fPath/_time.sh
source $fPath/_array.sh
source $fPath/_string.sh
