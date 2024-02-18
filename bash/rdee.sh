#!/bin/bash


fPath=$(cd $(dirname "${BASH_SOURCE[0]}") && readlink -f .)

source $fPath/_components/_basic.sh
source $fPath/_components/_io.sh
source $fPath/_components/_os.sh
source $fPath/_components/_time.sh
source $fPath/_components/_array.sh
source $fPath/_components/_string.sh

export RDEE_LOADED=1