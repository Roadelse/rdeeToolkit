#!/bin/bash

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# This script aims to emulate the "ln" command in linux, 
# but for windows shortcuts, via calling powershell.exe in wsl
# Therefore, it can only be used in wsl
# ---------------------------
# a simple version little security check
# support both wsl and win path style
# Usage: 
#    wln [windows-path(D:\...) | wsl-win-path(/mnt/d/...)] [windows-path | wsl-win-path ]
#    for the 2nd parameter (destination), it can point to both directory or link-path
#    if the destination exists, it will use the basename from target
# e.g.
#     wln ../demo.py .   		# get ./demo.py.lnk
# 	  wln D:\demo.py a   		# get ./a.lnk
# 	  wln ../demo.py b.lnk  	# get ./b.lnk
# 	  wln ../demo.py /mnd/d/c 	# get /mnd/d/c/b.lnk, given ...c is an existed directory
# ---------------------------
# v0.2 	  @2023-09-15 10:24:20  add support for flexible destination specification, includin all relative/absolute path/dir/filename for win and wsl-win
# v0.1    @2023-08-16 16:17:01  for ideal conditions
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# Need to do:
#   + add help
#   + add support for specifing link path, now only support a location, and name is fixed



pws=`which powershell.exe`

if [[ -z "$pws" ]]; then
	echo "Error! Cannot find powershell.exe"
	exit 1
fi

target=$1
location=$2

target_wsl=`win2wsl $target`
target_bname=`basename $target_wsl`
target_win=`wsl2win $target`

location_win=`wsl2win $location`
location_wsl=`win2wsl $location`

# echo location_wsl=$location_wsl

if [[ -e $location_wsl ]]; then
	destination=${location_win}\\${target_bname}.lnk
else
	if [[ ! "$location" =~ .*\.lnk$ ]]; then
		# echo "Error! windows shortcut link must ends with '.lnk'!"
		# exit 1
		destination=${location_win}".lnk"
	else
		destination=${location_win}
	fi
fi

echo "target : $target_win"
echo "destination : $destination"

powershell.exe -c "fast_link.ps1 ${target_win} ${destination}"
