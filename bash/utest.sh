#!/bin/bash



# WorkFlow
#   2023-12-12    init, <T::is_array>, <T::aq_hasVal>



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Pre-processing
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ------------ check run mode
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
	echo -e "\033[31m execute the script rather than source it! \033[0m"
	return 0
fi

# ------------ help
# help_mode=0
# while getopts "h" arg
# do
#     case $arg in
#         h)
#             help_mode=1;;
#     esac
# done
if [[ "$1" == "-h" ]]; then
	echo \
'Usage: ./utest.sh [-h] [test1 test2 test3 ... ...]

For rdee.bash module, run all tests if no test names specified, or run the selected tests

options:
   -h    print the help messgae
'
	exit 0
fi



# ------------ reset working directory
fPath=$(cd $(dirname "${BASH_SOURCE[0]}") && readlink -f .)
cd $fPath

# ------------ import rdee & prepare global variables
source rdee.sh

errCount=0

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Detailed tests
# A test function should always start with "test_", then it
# can be detected automatically when running all tests
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
function test_is_array(){
	# This test aims to test is_array from _basic.sh

	echo -n "test_is_array: "

	local A=(1 2 3)
	local -A B
	B[a]=1 ; B[b]=2
	local -n C=B 
	is_array A > /dev/null && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }
	is_array B > /dev/null && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }
	is_array C > /dev/null && { echo -ne "\033[31m Error \033[0m"; let errCount++; } || echo -ne "\033[33m ok \033[0m"
	is_array D > /dev/null && { echo -ne "\033[31m Error \033[0m"; let errCount++; } || echo -ne "\033[32m ok \033[0m"

}

function test_aq_hasVal(){
	echo -n "test_aq_hasVal: "

	# ============= direct mode with the number of arguments > 2
	[[ `aq_hasVal 1 2 3 4 2` == 1 ]] && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }
	[[ `aq_hasVal 1 2 3 4 5` == 0 ]] && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }

	# ============= indirect mode with the number of arguments == 2, except for $1 == $2
	A=(1 2 3 4 hello)
	[[ `aq_hasVal 5 5` == 1 ]] && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }
	aq_hasVal A hello > /dev/null && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }
	[[ `aq_hasVal A nani` == 0 ]] && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }
	[[ `aq_hasVal B hello` == 0 ]] && echo -ne "\033[32m ok \033[0m" || { echo -ne "\033[31m Error \033[0m"; let errCount++; }
}




# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# main
# [-] Usage
#     ./utest.sh
#     ./utest.sh aq_hasVal        (without test_ prefix!)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if [[ $# == 0 ]]; then  #>- run all tests
	allFuncs=(`compgen -A function | grep -P '^test_'`)  #>- can use `declare -F | cut -d\  -f 3 | grep -P '^test_'` to get all functions starting with test_, alternatively
	for f in ${allFuncs[@]}; do
		$f
		echo
	done
else  #>- run given tests
	for f in "$@"; do
		test_$f
		echo
	done
fi
echo

# ------------ Summary
if [[ $errCount -gt 0 ]]; then
	echo -e "\033[31m All tests fails in $errCount times \033[0m"
else
	echo -e "\033[32m All tests passed \033[0m"
fi
