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
from ._x_win import createShortCut, GetShortCut, path2wsl, path2win

if os.getenv("RDEEDEV"):
    from rdee.__dev__ import update_jj2
    update_jj2()

# from ._array import *
from ._x_time import Time
from ._xx_redtime import realevel, freetime
# from ._geo import *
# from ._io import *
# from ._code import *
# from ._research import *
# from ._plot import *
# from ._string import *
# from ._oop import *
