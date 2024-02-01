#!/usr/bin/env python3
# coding=utf-8

"""
This module contains a main class which wraps numpy.ndarray and providing several operations in relation to spatial and temporal processing
"""

#@sj import
import datetime
import os.path

import numpy as np
from typing import Sequence
from ._o_globalstate import logger
from ._x_time import Time
from ._o_error import NotImplementError


class _tarray(np.ndarray):
    def __new__(cls, data, *args, **kwargs):
        obj = np.asarray(data).view(cls)
        return obj

    def __init__(self, data, tdim: int, tval: Sequence):
        assert isinstance(tdim, int)
        assert 0 <= tdim < len(self.shape)
        assert hasattr(tval, "__len__") and len(tval) == self.shape[tdim]

        self.tdim: int = tdim
        self.tval: Sequence = tval
        self.tval, self.timescale = Time.get_time_str_and_scale(tval)
        self.isTimeContinuous: bool =


    def drp_time(self):
        """
        This function aims to do the dimension-reduced processing across the timescales
        """





class _sarray(np.ndarray):
    def __init__(self, data, sim, sval):
        pass


class tsarray(_tarray, _sarray):
    def __init__(self, data, tdim, tval, sdim, sval):
        pass



