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

#@ <function.get_fds_in_arr>
#@ This function save target directory names in a variable: _rstArray.By now it only saved the directories in working directory, can be extended to any-level and any-required-item in future
#@ Please note it always save result in _rstArray
get_fds_in_rstArray(){
    if [[ -z "$1" ]]; then
        target_path='.'
    else
        target_path="$1"
    fi

    IFS=$'\n' read -r -d '' -a _rstArray < <(find "$target_path" -mindepth 1 -maxdepth 1 -type d -printf '%P\n' && printf '\0')
}
