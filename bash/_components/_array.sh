#!/bin/bash

# Internal script, should never be used alone. Always use rdee.sh.

# This script holds functions for bash array.
# *********************************************************
# WorkFlow

# 2023-12-12   Initialization, <aq_hasVal # init & utest>


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
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Querying, with prefix of aq_
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
function aq_hasVal()
{
    local target=${@:$#}
    # echo $#, $target
    if [[ $# -gt 2 ]]; then
        for e in ${@:1:$#-1}; do
            # echo $target, $e
            if [[ "$e" == "$target" ]]; then
                echo 1
                return
            fi
        done
    elif [[ $# -lt 2 ]]; then
        echo "aq_hasVal must accept at least 2 arguments! Error"
        exit 1
    else
        [[ "$1" == "$2" ]] && { echo 1; return 0; } #>- aq_hasVal 1 1, true

        is_array $1 > /dev/null || { echo 0; return 101; }  #>- $1 is not a valid array variable name, false

        local -n arr=$1  # aq_hasVal A 1
        for e in "${arr[@]}"; do
            [[ "$e" == "$target" ]] && { echo 1; return 0; }  #>- find target element in expanded array, true
        done
    fi

    # --- cannot find target element, false
    echo 0
    return 101
}
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<