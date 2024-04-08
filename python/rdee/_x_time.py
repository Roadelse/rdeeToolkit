#!/usr/bin/env python3
# coding=utf-8

"""
This module contains several functions with relation to time
"""

#@sk import
import os
import datetime
from abc import ABC, abstractmethod


from typing import Sequence, Any

from ._o_globalstate import logger

class Time:
    def __init__(self, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} class cannot be instantiated")

    @staticmethod
    def get_time_str_and_scale(tval: Sequence) -> list[str]:
        """
        This function convert a sequence of time-denoting values into standard ymdhms string, with the right timescale.
        """

        from ._x_string import String

        #@sk boundary
        if isinstance(tval[0], str):
            strTrim: list[str] = String.trim_suffix(tval)
        elif hasattr(tval[0], "strftime"):
            ymdhms_all = [t.strftime("%Y%m%d%H%M%S") for t in tval]
            strTrim: list[str] = String.trim_suffix(ymdhms_all)
        else:
            logger.error(f"Unknown self.type: {type(tval[0])}, add support in time2str or modify your application")
            raise TypeError

        return strTrim

    @staticmethod
    def is_time_continuous(times: Sequence) -> bool:
        pass