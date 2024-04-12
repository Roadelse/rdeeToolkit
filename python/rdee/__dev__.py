# coding=utf-8

#@ Introduction
#@ This script provides some useful unctions in development period, i.e., it should not be included in the realease version
#@ --------------------------------------------------------
#@ 2024-04-12   init    | implement update_jj2()

#@ import
#@ .STL
import sys
import os
import os.path
import glob
import json

from ._o_globalstate import logger

def update_jj2():
    myDir = os.path.dirname(os.path.abspath(__file__))
    binDir = os.path.join(myDir, "../../bin")
    jj2_dir = os.path.join(myDir, "jj2-pieces")
    jj2_files = glob.glob(f"{jj2_dir}/*.jj2")
    if not jj2_files:
        print("(Unreachable) Warning! Cannot find jj2 files")
        return
    
    jj2_status_file = os.path.join(jj2_dir, "jj2-status.json")
    if not os.path.exists(jj2_status_file):
        jj2_status = {}
    else:
        jj2_status = json.load(open(jj2_status_file, "r"))

    modified = False
    for jf in jj2_files:
        jf_bname = os.path.basename(jf)
        dstfile = jf_bname.split('@')[0] + ".py"
        jj2output = os.path.splitext(jf_bname)[0]
        mtime = os.stat(jf).st_mtime
        mtimeRec = jj2_status.get(jf_bname)
        if mtimeRec is None or mtime < mtimeRec:
            modified = True
            jj2_status[jf_bname] = mtime
            rstat = os.system(f"python {binDir}/io/render-jj2.py -p '#@jj2' -o {jj2_dir} {jf}")
            if rstat:
                raise RuntimeError(f"Failed to render jj2 for {jf}")
            rstat = os.system(f"python {binDir}/io/txtop.ra-nlines.py -r {dstfile} {jj2output}")
            if rstat:
                raise RuntimeError(f"Failed to replace code snippet for {jf} in {dstfile}")
            logger.log("Render & Update jj2")

    if modified:
        json.dump(jj2_status, open("jj2_status_file", "w"))
