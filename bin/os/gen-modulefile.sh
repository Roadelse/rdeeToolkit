#!/bin/bash

target_dir=$1  # target directory
bname=`basename $target_dir`
ENAME=$2  # key environment variable name

if [[ -z $target_dir || ! -e $target_dir ]]; then
	echo -e '\033[31m''Must provide an existed directory as target!''\033[0m'
	exit 1
fi


cat > $bname << EOF
#%Module 1.0

setenv $ENAME $target_dir

EOF

if [[ -e $target_dir/bin ]]; then

	cat >> $bname << EOF
prepend-path PATH $target_dir/bin

EOF
fi

if [[ -e $target_dir/lib ]]; then

	cat >> $bname << EOF
prepend-path LD_LIBRARY_PATH $target_dir/lib
prepend-path LIBRARY_PATH $target_dir/lib

EOF
fi

