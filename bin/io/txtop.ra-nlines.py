#!/usr/bin/env python3
# coding=utf-8

#@ <Introduction>
#@ This script aims to create/append/replace the given multiple string lines into a base file.
#@ It can be implement in many tricks, such as sed or awk, but this scripts provides a more simple and general way 
#@ to do it, avoiding heavy coding at each time.
#@ [-] Usage
#@      ● python3 txtop.ra-nlines.py utest   # do the unit test
#@      ● python3 txtop.ra-nlines.py basefile rafile   # c/a/r content in rafile into basefile
#@ ----------------------------------------------------------------
#@ 2024-02-20       Init
#@ <Introduction/>



#@ import
#@ .STL
import os
import os.path
import sys
from typing import Optional
# import argparse  #@ exp use direct arguments now @2024-02-19 17:24:05

#@ prepare 
#@ .version-check
if sys.version_info < (3, 6):
    print("This script requires Python version 3.6 or higher")
    sys.exit(1)

#@ .global-variables
headerStock = {
    ".py": "#!/usr/bin/env python3\n# coding=utf-8",
    ".sh": "#!/bin/bash",
    "tmod": "#%Module1.0" 
}

#@ core
def ra_nlines(basefile: str, rafile: str, cheader: Optional[str] = None) -> None:
    #@ <prepare>
    #@ <.pre-check>
    assert os.path.exists(rafile)

    #@ <core>
    #@ <.boundary:create>
    if not os.path.exists(basefile):
        if cheader is not None:  #@ exp Empty string is allowed @2024-03-22 11:10:07
            if cheader in headerStock:
                header = headerStock[cheader]
            else:
                header = cheader
        else:
            ext = os.path.splitext(basefile)[1]
            header = headerStock[ext]
        with open(basefile, "w") as f:
            f.write(header.replace(r"\n", "\n") + "\n\n")
            f.write(open(rafile, encoding="utf-8").read())
        return

    #@ <.locate>
    baselines = open(basefile, encoding="utf-8").readlines()
    ralines = open(rafile, encoding="utf-8").readlines()

    imatch = -1
    for i, L in enumerate(baselines):
        if L == ralines[0]:
            assert imatch == -1, f"Error! Multiple matched lines, such as line:{imatch} and line:{i}"
            imatch = i
    
    #@ <.branch:append>
    if imatch == -1:
        with open(basefile, "a") as f:
            f.write("\n")
            f.write(open(rafile, encoding="utf-8").read())
            f.write("\n")
        return

    #@ <.branch:replace>
    #@ <..locate-endline>
    jmatch = -1
    for j in range(imatch, len(baselines)):
         if baselines[j].rstrip() == ralines[-1].rstrip():
            jmatch = j
            break
    assert jmatch != -1

    #@ <..output>
    with open(basefile, "w") as f:
        for i in range(imatch):
            f.write(baselines[i])
        for L in ralines[:-1]:
            f.write(L)
        f.write(baselines[jmatch])
        for i in range(jmatch + 1, len(baselines)):
            f.write(baselines[i])
    
    return


#@ utest
def utest():
    with open("base.py", "w") as f:
        f.write("""123
456
789
101""")
    with open("ra.py", "w") as f:
        f.write("""123\n000\n789""")

    ra_nlines("base.py", "ra.py")
    baseContent = open("base.py", encoding="utf-8").read()
    try:
        assert baseContent == "123\n000\n789\n101", baseContent
    finally:
        os.remove("base.py")
        os.remove("ra.py")
        
#@ entry
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="""arguments for text-opeartion: replace/append multiple lines""")

    if len(sys.argv) == 2 and sys.argv[1] == "utest":  #@ branch unittest
        utest()
    else:  #@ branch comman usage, text file operation
        assert len(sys.argv) in (3, 4)
        ra_nlines(sys.argv[1], sys.argv[2], None if len(sys.argv) == 3 else sys.argv[3])

