#!/bin/bash

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Pre-check
# 1. ensuring this script should only be sourced by another
#    script rather than in CLI
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "The script is being executed, Please source the rdee.sh!"
    exit 0
elif [[ `basename ${BASH_SOURCE[1]}` != "rdee.sh" ]]; then
    echo "The script can only be sourced from rdee.sh, exit"
    return 0
fi
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


now(){
    now_=`date +%Y%m%d-%H%M`
    echo $now_
}

