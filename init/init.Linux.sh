#!/bin/bash

###########################################################
# This scripts aims to build the necessary environment    #
# for using the <rdeeToolkit> properly in Linux.          #
# To be specific, supported functionality includes:       #
#    ● gather correponding binary to target dir           #
#    ● generate init script                               #
#    ● generate modulefile                                #
# --------------------------------------------------------#
# by Roadelse                                             #
#                                                         #
# 2024-01-08    created                                   #
###########################################################

myDir=$(cd $(dirname "${BASH_SOURCE[0]}") && readlink -f .)

# <L1> resolve argument
# ...
# ...
# ...
binary_dir=${PWD}/bin
load_script=${PWD}/load.rdeeToolkit.sh
modulefile=${PWD}/rdeeToolkit
profile=
while getopts "b:s:m:p:" arg; do
    case $arg in
    b)
        binary_dir=$OPTARG;;
    s)
        load_script=$OPTARG;;
    m)
        modulefile=$OPTARG;;
    p)
        profile=$OPTARG;;
    esac
done

# [Hiden] use Tmod for compatiability
# if [[ ! $modulefile =~ "."lua$ ]]; then
#     $modulefile=${modulefile}.lua
# fi


cat << EOF > $load_script
#!/bin/bash

EOF

cat << EOF > $modulefile
#%Module 1.0

EOF


# <L1> handle binary (executable)
mkdir -p $binary_dir/temp && cd $_
find $myDir/../bin -type f \( ! -perm /u=x \) -exec chmod +x {} \;
find $myDir/../bin -type f -exec ln -sf {} . \;
for f in `ls`; do
    if [[ $f =~ ".sh"$ ]]; then
        mv $f ${f%.sh}
    elif [[ $f =~ ".csh" ]]; then
        mv $f ${f%.csh}
    elif [[ $f =~ ".py" ]]; then
        mv $f ${f%.py}
    elif [[ $f =~ ".ps1" ]]; then
        mv $f ${f%.ps1}
    else
        rm $f
        echo -e '\033[33m'"Unknown extension: $f"'\033[0m'
    fi
done
cd ..
mv -f temp/* .
rmdir temp

cat << EOF >> $load_script
# >>>>>>>>>>>>>>>>> rdee executable
export PATH=${binary_dir}:\$PATH
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee executable
prepend-path PATH ${binary_dir}
EOF
cd $myDir


# <L1> python
# maybe check python version??
pylib_path=`realpath ${PWD}/../python`
cat << EOF >> $load_script
# >>>>>>>>>>>>>>>>> rdee python library
export PYTHONPATH=${pylib_path}:\$PYTHONPATH
export pipsrc1=https://pypi.tuna.tsinghua.edu.cn/simple
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee python library
prepend-path PYTHONPATH ${pylib_path}
setenv pipsrc1 https://pypi.tuna.tsinghua.edu.cn/simple
EOF


# <L1> bash
shlib_path=`realpath ${PWD}/../bash`
# >>>>>>>>>>>>>>>>> rdee python library
export PATH=${shlib_path}:$PATH
cat << EOF >> $load_script
# >>>>>>>>>>>>>>>>> rdee bash library
export PATH=${shlib_path}:\$PATH
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee bash library
prepend-path PATH ${shlib_path}
EOF


# <L1> powershell
pwsh_module_path=`realpath ${PWD}/../powershell`
cat << EOF >> $load_script
# >>>>>>>>>>>>>>>>> rdee powershell library
export PSModulePath=${pwsh_module_path}:\$PSModulePath
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee powershell library
prepend-path PSModulePath ${pwsh_module_path}
EOF



# <L1> alias
cat << EOF >> $load_script

# >>>>>>>>>>>>>>>>> system basic & shortcut for builti-in commands
alias ..='cd ..'
alias ...='cd ../..'

alias rp='realpath'
alias ls='ls --color=auto'
alias ll='ls -alFh'
alias la='ls -A'

alias pso='ps -o ruser=userForLongName -e -o pid,ppid,c,stime,tty,time,cmd'
alias psu='ps -u `whoami` -o pid,tty,time,cmd'
alias du1='du --max-depth=1 -h'
alias dv='dirsv -v'
alias topu='top -u `whoami`'
alias g='source g2s'
alias cdd='source cdDir'
alias gf='gfortran'
alias cd0='cd `readlink -f .`'


alias web='echo "plz copy : export http_proxy=127.0.0.1:port; export https_proxy=127.0.0.1:port"'
alias unweb='unset https_proxy; unset http_proxy'

# >>>>>>>>>>>>>>>>> project based
export reSG_dat=${binary_dir}/.reSG.dat

# >>>>>>>>>>>>>>>>> final
alias iR='source $shlib_path/rdee.sh'

EOF

cat << EOF >> $modulefile

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


set-alias web {echo "plz copy : export http_proxy=127.0.0.1:port; export https_proxy=127.0.0.1:port"}
set-alias unweb {unset https_proxy; unset http_proxy}

# >>>>>>>>>>>>>>>>> project based
setenv reSG_dat ${binary_dir}/.reSG.dat

# >>>>>>>>>>>>>>>>> final
set-alias iR {source $shlib_path/rdee.sh}

EOF


# <L1> handle content written to bash profiles
if [[ -z $profile ]]; then
    read -p "target bash profile path to be added or just [Enter]: " profile
    if [[ -z $profile ]]; then
        exit 0
    fi
fi

    cat << EOF >> `eval echo $profile`


# >>>>>>>>>>>>>>>>>>>>>>>>>>> [rdeeToolkit] set PS1
export PS1='\033[01;32m\\u@\\h\033[0m:\033[01;34m\\W\033[0m$ '

EOF
