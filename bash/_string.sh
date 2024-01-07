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
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


sf_startswith(){
    if [[ "$#" != "2" ]]; then
        echo "Error! Functino Startswith must accept 2 arguments"
        echo "Usage: "
        echo "    Startswith hello hel"
        exit 101
    fi

    if [[ "$1" =~ ^"$2" ]]; then  #>- use double-quotes to support handling spaces in strings
        echo 1
        return 0
    else
        echo 0
        return 1
    fi
}


sf_endswith(){
    if [[ "$#" != "2" ]]; then
        echo "Error! Functino Startswith must accept 2 arguments"
        echo "Usage: "
        echo "    Startswith hello hel"
        exit 101
    fi

    if [[ "$1" =~ "$2"$ ]]; then  #>- use double-quotes to support handling spaces in strings
        echo 1
        return 0
    else
        echo 0
        return 1
    fi
}