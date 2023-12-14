#!/usr/bin/env python3

# integers, definition to array, using python3

import sys

idef = sys.argv[1]

sep = ','
to = '-'

sections = idef.split(sep)
rst = []
for s in sections:
    if to in s:
        spair = s.split(to)
        rst.extend(list(range(int(spair[0]), int(spair[1]) + 1)))
    else:
        rst.append(s)

print(' '.join([str(_) for _ in rst]))