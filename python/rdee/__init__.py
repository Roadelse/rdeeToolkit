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

from ._x_logging import *
from ._o_basefunc import singleton
from ._o_globalstate import *
from ._x_os import *
from ._x_string import String

import os
if os.getenv("reStrict") or os.getenv("reStrict_package_rdee"):
    strict = True

logger = getLogger("rdee")

from ._array import *
# from ._time import *
# from ._geo import *
# from ._io import *
# from ._code import *
from ._research import *
# from ._win import *
# from ._plot import *
# from ._string import *
# from ._oop import *
