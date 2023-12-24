#!/bin/bash


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# This script aims to convert a wsl-windows path to actual windows path
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
path_wsl=$1


if [[ $path_wsl =~ ^[A-Z]:\\.* ]]; then
	echo $path_wsl
	exit 0
fi

path_wsl_rp=`realpath $path_wsl`
if [[ ! $path_wsl_rp =~ ^/mnt/[a-z]/.* ]]; then
	echo "Erorr! the wsl2win only works for windows path in wsl, i.e., like /mnt/[a-z]/..."
	exit 1
fi
disk=`echo $path_wsl_rp | cut -d/ -f3`
path_wsl_right=${path_wsl_rp:7}

rst=${disk^^}':\'${path_wsl_right////\\}

echo $rst