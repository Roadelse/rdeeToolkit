#!/usr/bin/env python3
# coding=utf-8

"""
This module contains several functions with relation to array operations
"""
from __future__ import annotations

from typing import Sequence
from enum import Enum

import numpy as np

from ._o_globalstate import logger
from ._o_error import ShouldNeverSeeError


class DRPC(Enum):
    """
    This Enum class DRPC (dimension-reduced processing category) contains several DRP categories
    while the value > 100 denotes it can only be operated in 1-dimension
    """
    avg = 0
    max = 1
    min = 2
    index = 3
    random = 4
    mavg = 101

    @classmethod
    def oned_only(cls, val: DRPC) -> bool:
        return val.value > 100


class Array:
    def __init__(self, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} class cannot be instantiated")

    @staticmethod
    def createSlice(ndims, targetSliceDict: dict = None, targetIndexDict: dict = None):
        """
        This function aims to create slice for target dimensions
        For example:
            data[createSlice(len(data.shape), targetSliceDict={0: (3, 5)}, targetIndexDict={2: (5,2,1)})]
        Reference:
            ● https://stackoverflow.com/questions/24398708/slicing-a-numpy-array-along-a-dynamically-specified-axis
            ● https://stackoverflow.com/questions/31094641/dynamic-axis-indexing-of-numpy-ndarray

        :param ndims: Rank of target data
        :param targetSliceDict: Slice for target dimensions
        :param targetIndexDict: Indexs for target dimensions
        :return: Slice, which can be used directly in [...]
        """

        sls = [slice(None)] * ndims
        if targetSliceDict is not None:
            for k in targetSliceDict.keys():
                sls[k] = slice(*targetSliceDict[k])

        if targetIndexDict is not None:
            for k in targetIndexDict:
                sls[k] = targetIndexDict[k]

        return tuple(sls)

    @staticmethod
    def drp(data: np.ndarray, dims: list[int] | tuple[int,...] | int, op: DRPC, mapping: dict[int, list[int]] = None, opArgs: dict = None):
        """
        This function aims to do Dimension-Reduced Processing (drp) operations for selected dimensions.
        Generally the drp is conducted in dimensions, while if you set arg:mapping, firstly the arg:dims must be an int, then the drp is conducted within the target dimension based on provided 1-dimensional mapping

        :param data: Original data where drp is done for it
        :param dims: target dimensions
        :param op: Operation method, be a DRPC Enum variable
        :param mapping: set a dict to turn on 1-dimensional mapping drp
        :param opArgs: set supplementary parameters for different op

        :return: a new np.ndarray with dimension reduced as desgined
        """
        #@sk pre-check
        assert isinstance(data, np.ndarray)
        assert isinstance(dims, (int, list, tuple))
        assert isinstance(op, DRPC)
        if isinstance(dims, int):
            assert len(data.shape) > dims
        else:
            assert len(data.shape) > max(dims)
        if mapping:
            assert isinstance(dims, int)

        #@sk prepare get key variables for later use
        shape = data.shape
        rank = len(shape)
        dimsTuple = (dims,) if isinstance(dims, int) else tuple(dims)

        #@sk branch check and handle mapping mode first
        if mapping:
            if not isinstance(dims, int):  #@sk exp only support 1d mapping now
                raise NotImplementedError("Error! mapping can only be together with 1-dim drp by now.")

            #@sk prepare get key variables for new data
            keys = mapping.keys()
            values = mapping.values()
            assert max([max(vs) for vs in list(values)]) < shape[dims]
            assert sorted(list(keys)) == list(range(len(keys)))
            shapeNew = list(shape)
            shapeNew[dims] = len(mapping.keys())

            #@sk prepare create new data variable with default value
            target_dtype = data.dtype if op in (DRPC.max, DRPC.min) else np.float64
            default_value = 0 if target_dtype in (np.int32, np.int64) else np.nan
            rstData = np.full(shapeNew, default_value, target_dtype)

            #@sk core core logic for mapping mode, i.e., loop each index one by one
            for i in keys:
                rstData[Array.createSlice(rank, targetIndexDict={dims: i})] = Array.drp(data[Array.createSlice(rank, targetIndexDict={dims: mapping[i]})], dims, op, opArgs=opArgs)
            return rstData

        if op == DRPC.avg:  #@sk branch avg
            return data.mean(dimsTuple)
        elif op == DRPC.max:  #@sk branch max
            return data.max(dimsTuple)
        elif op == DRPC.min:  #@sk branch min
            return data.min(dimsTuple)
        elif op == DRPC.index:  #@sk branch index
            assert isinstance(opArgs, dict) and "index" in opArgs  #@sk exp need supplementary parameters
            if not isinstance(dims, int):
                raise NotImplementedError("Error! func:drp doesn't support n-dim and DRPC.index by now.")
            return data[Array.createSlice(rank, targetIndexDict={dims: opArgs["index"]})]
        elif op == DRPC.random:  #@sk branch random
            assert isinstance(opArgs, dict) and "count" in opArgs
            raise NotImplementedError("DRPC.random not implemented")
        elif op == DRPC.mavg:  #@sk branch mavg
            assert isinstance(dims, int)
            raise NotImplementedError("DRPC.mavg not implemented")
        else:  #@sk branch impossible
            raise ShouldNeverSeeError



