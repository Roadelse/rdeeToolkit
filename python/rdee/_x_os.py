#!/usr/bin/env python3
# coding=utf-8

"""
This module contains several functions for os oprations, which may not directly supported in STL:os
"""

#@sk import
import os
import os.path
import shutil

from rdee import _o_globalstate as ogs


def rmrf(directory: str, use_strict: bool = False) -> None:
    #@sk prepare check if use strict
    if ogs.strict:
        use_strict = True

    #@sk boundary if directory doesn't exist
    if not os.path.exists(directory):
        if use_strict:
            raise RuntimeError("Error! Try to rmrf in a non-existed directory")
        return None
    
    #@sk core
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
            if use_strict:  #@sk raise error if use_strict
                raise
