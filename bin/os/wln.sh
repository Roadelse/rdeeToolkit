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
# v20240322     @2024-03-22 16:22:16
#   ● Extend support for both shortcut link and symbol link
#   ● add help
# v0.2 	  @2023-09-15 10:24:20  add support for flexible destination specification, includin all relative/absolute path/dir/filename for win and wsl-win
# v0.1    @2023-08-16 16:17:01  for ideal conditions
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



pws=`which pwsh.exe`

if [[ -z "$pws" ]]; then
	echo "Error! Cannot find pwsh.exe"
	exit 1
fi

shortcut=0
show_help=0
utest=0
while getopts "shu" arg
do
    case $arg in 
        s)
            shortcut=1
            shift;;
		h)
			show_help=1
			shift;;
        u)
            utest=1
            shift;;
        *)
            echo Error
            return 200
    esac
done   

if [[ $show_help == 1 ]]; then
	echo -e "
wln, a bash scipt aiming to create windows link in WSL, supporting both shortcut link and symbol link
All the paths are flexible for both windows-path & wsl-path

[Usage]
    wln [option] <src> <dst>

[arguments]
    ● src: source file/directory path of windows file system, including both windows path & WSL path
    ● dst: similar with src

[optional]
    ● -h
        show help information
    ● -s
        use shortcut link, use symbol link by default
"
    exit 0
fi

if [[ $utest == 0 ]]; then

target=$1
location=$2

target_wsl=`win2wsl $target`
target_bname=`basename $target_wsl`
target_win=`wsl2win $target`

location_win=`wsl2win $location`
location_wsl=`win2wsl $location`

# echo location_wsl=$location_wsl

if [[ -d $location_wsl ]]; then
	destination=${location_win}\\${target_bname}.lnk
else
	destination=${location_win}
fi

echo "target : $target_win"
echo "destination : $destination"

if [[ $shortcut ]]; then
    powershell.exe -c "fast_link.ps1 -s ${target_win} ${destination}"
else
    powershell.exe -c "fast_link.ps1 ${target_win} ${destination}"
fi

else
    #@ unittest
    # mkdir .utest-wln && cd $_
    # wln 




fi