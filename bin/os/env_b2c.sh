#!/bin/bash

inf=$1
outf=${inf//sh/csh}
rm -f $outf

while read LINE 
do
	if [[ ! -e $outf ]]; then
		echo '#!/bin/csh' > $outf
		continue
	fi

	if [[ $LINE == "" ]]; then
		echo $LINE >> $outf
	elif [[ $LINE =~ ^#.* ]]; then
		echo $LINE >> $outf
	elif [[ $LINE =~ ^export.* ]]; then
		L2=${LINE/export/setenv}
		L3=${L2/=/ }
		echo $L3 >> $outf
	else
		echo "unexpected line : "
		echo $LINE
		eixt 1
	fi

done < $inf
