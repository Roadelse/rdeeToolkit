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


echo_red(){
    echo -e "\033[31m"$*"\033[0m"
}


echo_yellow(){
    echo -e "\033[33m"$*"\033[0m"
}


echo_blue(){
    echo -e "\033[34m"$*"\033[0m"
}

echo_cyan(){
    echo -e "\033[36m"$*"\033[0m"
}

logT(){
    now_=`date +'%Y/%m/%d %H:%M:%S'`
    echo "$now_   $*"
}
logT_red(){
    now_=`date +'%Y/%m/%d %H:%M:%S'`
    echo -e "$now_   \033[31m"$*"\033[0m"
}
logT_yellow(){
    now_=`date +'%Y/%m/%d %H:%M:%S'`
    echo -e "$now_   \033[33m"$*"\033[0m"
}
logT_blue(){
    now_=`date +'%Y/%m/%d %H:%M:%S'`
    echo -e "$now_   \033[34m"$*"\033[0m"
}
logT_cyan(){
    now_=`date +'%Y/%m/%d %H:%M:%S'`
    echo -e "$now_   \033[36m"$*"\033[0m"
}
