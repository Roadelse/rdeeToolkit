#!/bin/bash



# *********************************************************
# This bash script aims to add 'x' authority for selected
# files starting with '#!'
# The operation will be executed on the actual file, e.g., 
# it will go through the symbol link 
# ----------------------
# Usage:
#     addX file1 file2 file3 ... ...
#     addX dir1 file2 dir3 ... ...
# ----------------------
# Change log:
#    @2023-08-10 20:39:56  init
# *********************************************************


for fd in ${@}  # fd : file or directory
do
	if [[ -f $fd ]]; then
		if [[ `head -n 1 $fd` =~ ^'#!' ]]; then
			chmod +x `realpath $fd`
		fi
	elif [[ -d $fd ]]; then
		find $fd -type f | xargs addX
	fi
done
