#!/usr/bin/env python3
# coding=utf-8

"""
This module contains a main class which wraps numpy.ndarray and providing several operations in relation to spatial and temporal processing
"""

#@ import
import datetime
import os.path
from enum import Enum


import numpy as np
from typing import Sequence
from ._o_globalstate import logger
from ._x_time import Time
from ._o_error import ShouldNeverSeeError
from ._x_array import Array

class DRPC4T(Enum):
    """
    This Enum class DRPC (dimension-reduced processing category) contains several DRP categories
    while the value > 100 denotes it can only be operated in 1-dimension
    """
    ALL_AVG = 0
    ALL_MAX = 1
    ALL_MIN = 2
    ALL_INDEX = 3
    ALL_RANDOM = 4
    ALL_MAVG = 5
    YEAR_AVG = 100
    YEAR_MAX = 101
    YEAR_MIN = 102



class _tarray(np.ndarray):
    def __new__(cls, data, *args, **kwargs):
        obj = np.asarray(data).view(cls)
        return obj

    def __init__(self, data, tdim: int, tseq: Sequence):
        from ._xx_redtime import realtimeseries

        assert isinstance(tdim, int)
        assert 0 <= tdim < len(self.shape)
        assert hasattr(tseq, "__len__") and len(tseq) == self.shape[tdim]

        self.tdim: int = tdim
        self.rts: Sequence = realtimeseries(tseq)  #@ ?? | if non-monotonic?
        # self.isTimeContinuous: bool = ??


    def drp(self, op: DRPC4T, opArgs: dict = None):
        """
        This function aims to do the dimension-reduced processing across the time dimension
        """
        from ._xx_redtime import realevel

        if op == DRPC4T.ALL_AVG:
            rst = self.mean(axis=self.tdim)
        elif op == DRPC4T.ALL_MAX:
            rst = self.max(axis=self.tdim)
        elif op == DRPC4T.ALL_MIN:
            rst = self.min(axis=self.tdim)
        elif op == DRPC4T.ALL_INDEX:
            rst = self[Array.createSlice(self.shape, targetIndexDict={self.tdim: opArgs["index"]})]
        elif op == DRPC4T.YEAR_AVG:
            if self.rts.timescale <= realevel.YEAR:
                raise ValueError
            #@ status | ts > realevel.YEAR
            



class _sarray(np.ndarray):
    def __init__(self, data, sim, sval):
        pass


class tsarray(_tarray, _sarray):
    def __init__(self, data, tdim, tval, sdim, sval):
        pass



