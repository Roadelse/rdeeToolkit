#!/usr/bin/env python3
# coding=utf-8


###########################################################
# This script aims to union init-scripts and modulefiles  #
# from multiple projects into one 						  #
###########################################################


# 2024-01-11 	init
# 2024-01-13 	Bug fix for sort-function sf(x) (not strictly correct, just a workaround)
# 2024-02-21    Mitigated to rdeeToolkit/bin, use manually set outfile


import sys, os, os.path


def main(outfile, infiles):
	def sf(x):
			if x.startswith('prepend-path'):
				rst = 2
			elif x.startswith('setenv') or x.startswith('export'):
				rst = 1
			elif x.startswith('set-alias') or x.startswith('alias'):
				rst = 3
			else:
				rst = 10
			
			if '$' in x:
				rst += 0.5
			return rst
	
	if infiles[0].endswith('.sh'):
		lang = "bash"
	else:
		lang = "module"
		

	lines = []
	for f in infiles:
		lines.extend(open(f).read().splitlines())


	lines_V = [L for L in lines if not L.startswith('#')]  #>- V: valid
	lines_VU = list(set(lines_V))  #>- V: valid, U: unique

	lines_VUS = sorted(lines_VU, key=sf)  #>- V: valid, U: unique, S: sorted


	with open(outfile, 'w') as f:
		if lang == 'bash':
			f.write("#!/bin/bash\n\n")
		else:
			f.write("#%Module 1.0\n\n")

		f.write('\n'.join(lines_VUS))
		f.write('\n')


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2:])