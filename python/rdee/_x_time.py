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

from ._o_globalstate import logger, strict

class Time:
    def __init__(self, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} class cannot be instantiated")

    @staticmethod
    def get_days_from_ym(year: int|str, month: int|str) -> int:
        """
        Get corresponding number of days based on year and month
        """
        from calendar import isleap
        assert isinstance(year, (int, str))
        assert isinstance(month, (int, str))
        year = int(year)
        month = int(month)
        assert month > 0 and month <= 12
        if not hasattr(Time.get_days_from_ym, "mdays"):
            Time.get_days_from_ym.mdays = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        if isleap(year) and month == 2:
            return 29
        else:
            return Time.get_days_from_ym.mdays[month-1]

    @staticmethod
    def countLeap(year1: int, year2: int, with_left: bool = True, with_right: bool = True):
        """
        Count the number of leap years between 2 years
        """
        from calendar import isleap
        if strict:
            if not isinstance(year1, int):
                raise TypeError
            if not isinstance(year2, int):
                raise TypeError
            if not isinstance(with_left, bool):
                raise TypeError
            if not isinstance(with_right, bool):
                raise TypeError

        if year1 > year2:
            return Time.countLeap(year2, year1, with_right, with_left)

        def countLeapFrom0(yr: int, withB: bool):
            yr = abs(yr)
            return yr // 4 - yr // 100 + yr // 400 + (0 if withB else -1) * isleap(yr)

        return countLeapFrom0(year2, with_right) * (1 if year2 > 0 else -1) - countLeapFrom0(year1, with_left) * (1 if year1 > 0 else -1)

    @staticmethod
    def get_jdays(month: int, day: int, year: int):
        jdays: int = 0
        for i in range(1, month+1): 
            jdays += Time.get_days_from_ym(year, i)
        jdays += day
        return jdays

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