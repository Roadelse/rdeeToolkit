#!/usr/bin/env python3
# coding=utf-8

# this file contains some useful functions which are commonly used by myself
# rdee - roadelse

"""
rdee python package, within repository rdeeToolkit

This personal custom package is incubated and extended during my daily research, work and life.
It contains several components, which are arranged via MUEXO protocol.

Author:
    Roadelse - roadelse@qq.com
"""

print("----------------------------rdee: __init__.py")

import os


from rdee import _o_globalstate as ogs

if os.getenv("reStrict") or os.getenv("reStrict_package_rdee"):
    ogs.strict = True

from ._x_logging import getLogger, getAllHandlers, has_stdout_handler

if ogs.logger is None:
    ogs.logger = getLogger("rdee")

from ._o_basefunc import singleton
from ._x_os import rmrf
from ._x_string import String
from ._x_win import createShortCut, GetShortCut, path_win2wsl, path_wsl2win


# from ._array import *
# from ._time import *
# from ._geo import *
# from ._io import *
# from ._code import *
# from ._research import *
# from ._plot import *
# from ._string import *
# from ._oop import *
