#!/bin/bash

# this script aims to build working environment from roadelse tools & libs
# by rdee in zjlab-11B-303 @2023-04-19 10:29:24
# @2023-08-10  update to support copy folder from given directories rather than from git clone
# @2023-11-15  re-build to fully embrace the Module management system



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pre-defined temporary functions
function errhandler(){
    msg="$1"
    echo -e '\033[31m'${msg}'\033[0m'
    exit 10  # from 10 on
}



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> resolve arguments
gitDir=`realpath ../recRoot/GitRepos`
while getopts "g:" arg
do
    case $arg in 
        g)
            gitDir=$OPTARG;;
    esac
done



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> key control variables


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> resolving necessary variables
echo "Resolving necessary variables ... ..."
# ...................... root dir
fPath=$(cd $(dirname "${BASH_SOURCE[0]}") && readlink -f .)
currDir=$fPath
cd $currDir
echo '>>>' currDir is $currDir
if [[ `basename ${currDir}` != 'tools' ]]; then
    echo "the config.sh should be located in .../tools, or modify the code manually"
    exit 2
fi

# ...................... machine info
mach_name="`whoami`@`uname -n`"
[[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && isWSL=1 || isWSL=0
if [[ $isWSL == 1 ]]; then
    win_uname=$(cmd.exe /C "echo %USERNAME%" 2>/dev/null | tr -d '\r')
fi



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> file/dir operations
rm -rf projs bin include lib modulefiles

echo "file/dir operating ... ..."
mkdir -p projs && cd $_
for p in NCL_RDEE PY_RDEE LinuxTools_rdee
do
    if [[ -e $gitDir/$p ]]; then
        ln -s $gitDir/$p .
    else
        errhandler "$p not found, please check the gitDir: ${gitDir}"
    fi
done

mkdir -p minor && cd $_
for p in workFlowRec rdSync quickSpace
do
    if [[ -e $gitDir/$p ]]; then
        ln -s $gitDir/$p .
    else
        errhandler "$p not found, please check the gitDir: ${gitDir}"
    fi
done
cd ../..

mkdir -p bin lib include
cd bin
ln -sf ../projs/NCL_RDEE/bin/* .
ln -sf ../projs/LinuxTools_rdee/bin/*/* .
ln -sf ../projs/PY_RDEE/bin/* .
ln -sf ../projs/minor/rdSync/rdsync .
ln -sf ../projs/minor/rdSync/rob .
ln -sf ../projs/minor/workFlowRec/wf .
ln -sf ../projs/minor/quickSpace/bin/* .
pyfs=(`ls *py 2>/dev/null`)
[[ -n "${pyfs}" ]] && rename 's/.py//' *.py

cd ../lib
ln -sf ../projs/LinuxTools_rdee/lib/* .
ln -sf ../projs/minor/quickSpace/lib/* .

cd ../include
cd ..



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> create modulefile
echo "creating modulefile"
# ...................... prepare variables
reHome=`dirname $fPath`
reRec=$reHome/recRoot
reGit=$reRec/GitRepos
reSoft=$reHome/softwares
reMANA=$reSoft/mana
reModel=$reHome/models
reTool=$reHome/tools
reTemp=$reHome/temp
reTest=$reHome/test


# ...................... write
echo '*************** setting modulefiles ***************'
mkdir -p modulefiles

cat << EOF > modulefiles/rdee
#%Module 1.0

# >>>>>>>>>>>>>>>>>>>>>>>>>>> environment variables
# ............ basic directories & file paths
setenv reHome ${reHome}
setenv reRec ${reRec}
setenv reGit ${reGit}
setenv reSoft ${reSoft}
setenv reMANA ${reMANA}
setenv reModel ${reModel}
setenv reTool ${reTool}
setenv reTemp ${reTemp}
setenv reTest ${reTest}

setenv pathSG_re ${reHome}/.path.rdee.sg


# ............ others
setenv pipSrc https://pypi.tuna.tsinghua.edu.cn/simple


# ............ for applications 
# --- bin & lib
prepend-path PATH ${currDir}/bin
prepend-path PATH ${currDir}/lib

# --- NCL
setenv NCL_RDEE_DIR ${currDir}/NCL_RDEE
setenv NCL_RDEE_LIB ${currDir}/NCL_RDEE/lib
setenv NCL_RDEE ${currDir}/NCL_RDEE/lib/rdee.ncl

# --- Python
prepend-path PYTHONPATH ${currDir}/PY_RDEE

# --- workFlowRec
set-alias wfa {source wf}


# >>>>>>>>>>>>>>>>>>>>>>>>>>> Alias
set-alias rp realpath

set-alias ll {ls -alF}
set-alias ls {ls --color=auto}
set-alias la {ls -A}

set-alias pso {ps -o ruser=userForLongName -e -o pid,ppid,c,stime,tty,time,cmd}
set-alias psu {ps -u `whoami` -o pid,tty,time,cmd}
set-alias grep {grep --color=auto}
set-alias du1 {du --max-depth=1 -h}
set-alias dv {dirs -v}
set-alias topu {top -u `whoami`}
set-alias g {source g2s}
set-alias cdd {source cdDir}
set-alias gf {gfortran}

set-alias cd0 {cd `readlink -f .`}

set-alias cdR {cd $reRec}
set-alias cdG {cd $reRec/GitRepos}

set-alias web {echo "plz copy : export http_proxy=127.0.0.1:port; export https_proxy=127.0.0.1:port"}
set-alias unweb {unset https_proxy; unset http_proxy}



# >>>>>>>>>>>>>>>>>>>>>>>>>>> System operations
system "source ${reGit}/rdeeToolkit/bash/rdee.sh"
system "source ${reTool}/config.bash"

EOF

if [[ $isWSL == 1 ]]; then
    cat << EOF >> modulefiles/rdee
# >>>>>>>>>>>>>>>>>>>>>>>>>>> WSL additions
setenv OneDrive /mnt/c/Users/${win_uname}/OneDrive
setenv Desktop /mnt/c/Users/${win_uname}/Desktop
setenv BaiduSync /mnt/d/BaiduSyncdisk
setenv recRoot /mnt/d/recRoot
set-alias rob {source ${currDir}/bin/rob}
set-alias winc {cmd.exe /c}
set-alias cdw {source cdw_}
set-alias sublime {/mnt/d/XAPP/SublimeText/sublime_text.exe}
set-alias vscode {/mnt/d/XAPP/VSCode/code.exe}
set-alias pdf {/mnt/d/DAPP/SumatraPDF/SumatraPDF.exe}
set-alias md {/mnt/d/XAPP/VSCode/Code.exe}
set-alias ii {/mnt/c/Windows/explorer.exe}
set-alias cdO {cd \$OneDrive}
set-alias cdD {cd \$Desktop}
set-alias cdB {cd \$BaiduSync}
EOF
fi
