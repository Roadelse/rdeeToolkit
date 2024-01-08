#!/bin/bash

###########################################################
# This scripts aims to build the necessary environment    #
# for using the <rdeeToolkit> properly in Linux.          #
# To be specific, supported functionality includes:       #
#    ● check requirements                                 #
#    ● generate a bash script which set environment       #
#      variables and alias                                #
#    ● generate modulefile                                #
# --------------------------------------------------------#
# by Roadelse                                             #
#                                                         #
# 2024-01-08    init                                      #
###########################################################

myDir=$(cd $(dirname "${BASH_SOURCE[0]}") && readlink -f .)
cd $myDir


# <L1> resolve argument
# ...
# ...
# ...
binary_dir=testBin
setvar_script=${myDir}/setenv.sh
modulefile=${myDir}/rdeeToolkit


cat << EOF > $setvar_script
#!/bin/bash

EOF

cat << EOF > $modulefile
#%Module 1.0

EOF


# <L1> handle binary (executable)
mkdir -p $binary_dir && cd $_
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
        echo -e '\033[33m'"Unknown extension: $f"'\033[0m'
    fi
done

cat << EOF >> $setvar_script
# >>>>>>>>>>>>>>>>> rdee executable
export PATH=${PWD}:\$PATH
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee executable
prepend-path PATH ${PWD}
EOF
cd $myDir


# <L1> python
# maybe check python version??
pylib_path=`realpath ${PWD}/../python`
cat << EOF >> $setvar_script
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
cat << EOF >> $setvar_script
# >>>>>>>>>>>>>>>>> rdee bash library
export PATH=${shlib_path}:\$PATH
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee bash library
prepend-path PATH ${shlib_path}
EOF


# <L1> powershell
pwsh_module_path=`realpath ${PWD}/../powershell`
cat << EOF >> $setvar_script
# >>>>>>>>>>>>>>>>> rdee powershell library
export PSModulePath=${pwsh_module_path}:\$PSModulePath
EOF

cat << EOF >> $modulefile
# >>>>>>>>>>>>>>>>> rdee powershell library
prepend-path PSModulePath ${pwsh_module_path}
EOF

