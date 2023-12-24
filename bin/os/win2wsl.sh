#!/bin/bash


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# This script aims to convert a windows path to wsl path
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
path_win="$1"

if [[ ! $path_win =~ ^[A-Z]:\\.* ]]; then
	echo `realpath $path_win`
	exit 0
fi

disk=${path_win:0:1}
path_win_right=${path_win:3}


rst=/mnt/${disk,,}/${path_win_right//\\//}

echo $rst

