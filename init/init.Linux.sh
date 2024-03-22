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
# 2024-02-20    remove PS1 settings and re-organize via   #
#               CodeSK, update profile processing         #
###########################################################

#@ <prepare>
#@ <.depVars>  dependent variables
myDir=$(cd $(dirname "${BASH_SOURCE[0]}") && readlink -f .)
curDir=$PWD

#@ <.pre-check>
#@ <..python>
if [[ -z `which python3 2>/dev/null` ]]; then
	echo '\033[31m'"Error! Cannot find python interpreter"'\033[0m'
	exit 200
fi

#@ <.arguments>
#@ <..default>
binary_dir=${curDir}/bin
setenvfile=${curDir}/load.rdeeToolkit.sh
modulefile=${curDir}/rdeeToolkit
profile=
#@ <..resolve>
while getopts "b:s:m:p:" arg; do
    case $arg in
    b)
        binary_dir=$OPTARG;;
    s)
        setenvfile=$OPTARG;;
    m)
        modulefile=$OPTARG;; 
    p)
        profile=$OPTARG;;
    esac
done


#@ <.header> create header for setenv and module files
cat << EOF > $setenvfile
#!/bin/bash

EOF

cat << EOF > $modulefile
#%Module 1.0

EOF


#@ <core>
# <.binary> organize executable
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

#@ <..update-sm>
cat << EOF >> $setenvfile
# >>>>>>>>>>>>>>>>> rdee executable
export PATH=${binary_dir}:\$PATH
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee executable
prepend-path PATH ${binary_dir}
EOF
# cd $myDir


#@ <.subprojs>
# <..python> [note|maybe check python version??]
pylib_path=`realpath ${curDir}/../python`
cat << EOF >> $setenvfile
# >>>>>>>>>>>>>>>>> rdee python library
export PYTHONPATH=${pylib_path}:\$PYTHONPATH
export pipsrc1=https://pypi.tuna.tsinghua.edu.cn/simple
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee python library
prepend-path PYTHONPATH ${pylib_path}
setenv pipsrc1 https://pypi.tuna.tsinghua.edu.cn/simple
EOF


# <..bash>
shlib_path=`realpath ${curDir}/../bash`
export PATH=${shlib_path}:$PATH

cat << EOF >> $setenvfile
# >>>>>>>>>>>>>>>>> rdee bash library
export PATH=${shlib_path}:\$PATH
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee bash library
prepend-path PATH ${shlib_path}
EOF


# <..powershell>
pwsh_module_path=`realpath ${curDir}/../powershell`

cat << EOF >> $setenvfile
# >>>>>>>>>>>>>>>>> rdee powershell library
export PSModulePath=${pwsh_module_path}:\$PSModulePath
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee powershell library
prepend-path PSModulePath ${pwsh_module_path}
EOF


# <..alias>
cat << EOF >> $setenvfile

alias cdf='source cdDir'

# >>>>>>>>>>>>>>>>> project based
export reSG_dat=${binary_dir}/.reSG.dat

# >>>>>>>>>>>>>>>>> final
alias iR='source $shlib_path/rdee.sh'

EOF

cat << EOF >> $modulefile

set-alias cdd {source cdDir}

# >>>>>>>>>>>>>>>>> project based
setenv reSG_dat ${binary_dir}/.reSG.dat

# >>>>>>>>>>>>>>>>> final
set-alias iR {source $shlib_path/rdee.sh}

EOF

#@ <post> modify profile
cd $curDir
set -e
if [[ -n $profile ]]; then
    read -p "profile detected, which way to init rdeeToolkit? [setenv|module] default:module " sm
    if [[ -z $sm ]]; then
        sm=module
    fi

    # echo "sm=$sm"
    
    if [[ $sm == "module" ]]; then
        moduledir=$(dirname $modulefile)
        cat << EOF >> .temp
# >>>>>>>>>>>>>>>>>>>>>>>>>>> [rdeeToolkit] init
module use $moduledir
module load rdeeToolkit

EOF
        python3 $myDir/../bin/io/txtop.ra-nlines.py $profile .temp
        rm -f .temp
    elif [[ $sm == "setenv" ]]; then
        cat << EOF >> .temp
# >>>>>>>>>>>>>>>>>>>>>>>>>>> [rdeeToolkit] init
source $setenvfile

EOF
        python3 $myDir/../bin/io/txtop.ra-nlines.py $profile .temp
        rm -f .temp
    else
        echo "Unknown input: $sm"
        exit 200
    fi
fi
