#!/usr/bin/env python3
# coding=utf-8

"""
This module contains several functions with relation to time
"""

#@sk import
import os
import datetime

import pandas
from pandas import Timestamp, Timedelta
from typing import Sequence, Any
from enum import Enum, auto

from ._o_globalstate import logger


class timescale(Enum):
    YEAR = 0
    MONTH = 1
    DAY = 2
    HOUR = 3
    MINUTE = 4
    SECOND = 5

    @classmethod
    def getTimescale(cls, s: str):
        assert isinstance(s, str)
        if len(s) == 4:
            return cls.YEAR
        elif len(s) == 6:
            return cls.MONTH
        elif len(s) == 8:
            return cls.DAY
        elif len(s) == 10:
            return cls.HOUR
        elif len(s) == 12:
            return cls.MINUTE
        elif len(s) == 14:
            return cls.SECOND
        else:
            logger.error(f"Wrong length for ymdhms string: {len(s)}")
            raise RuntimeError


class redtime:  #@sk exp RoadElse's DateTIME
    def __init__(self, a1: Any, a2: int | str = None, a3: int = -1, a4: int = -1, a5: int = -1, a6: int = -1, **kwargs):
        self._year = None
        self._month = None
        self._day = None
        self._hour = None
        self._minute = None
        self._second = None

        if isinstance(a1, str):  #@sk branch set time from ymdhs-ordered string
            intchars = ''.join([c for c in a1 if c.isdigit()])
            self.year = int(intchars[:4]) if len(intchars) >= 4 else -1
            self.month = int(intchars[4:6]) if len(intchars) >= 6 else -1
            self.day = int(intchars[6:8]) if len(intchars) >= 8 else -1
            self.hour = int(intchars[8:10]) if len(intchars) >= 10 else -1
            self.minute = int(intchars[10:12]) if len(intchars) >= 12 else -1
            self.second = int(intchars[12:14]) if len(intchars) >= 14 else -1

    # region property
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, i: int):
        assert isinstance(i, int)
        self._year = i

    @property
    def month(self):
        return self.month

    @year.setter
    def month(self, i: int):
        assert isinstance(i, int)
        self._month = i

    @property
    def day(self):
        return self.day

    @year.setter
    def day(self, i: int):
        assert isinstance(i, int)
        self._day = i

    @property
    def hour(self):
        return self.hour

    @year.setter
    def hour(self, i: int):
        assert isinstance(i, int)
        self._hour = i

    @property
    def minute(self):
        return self.minute

    @year.setter
    def minute(self, i: int):
        assert isinstance(i, int)
        self._minute = i


    @property
    def second(self):
        return self.second

    @year.setter
    def second(self, i: int):
        assert isinstance(i, int)
        self._second = i
    # endregion property

    def isreal(self):
        if self.year < 1900 or self.year > 2200:
            return False
        if self.month < 1 or self.month > 12:
            return False
        if self.day < 1 or self.day > 31:  #@sk ?? for different months
            return False
        if self.hour < 0 or self.hour > 59:
            return False
        if self.minute < 0 or self.minute > 59:
            return False
        if self.second < 0 or self.second > 59:
            return False
        return True

    def toreal(self):



    def __new__(cls, a1, *args, **kwargs):
        if isinstance(a1, int):  #@sk branch use datetime.datetime style arguments
            return Timestamp(a1, *args, **kwargs)
        elif isinstance(a1, str):  #@sk branch use time string
            timeformat = None
            if args and isinstance(args[0], str):
                timeformat = args[0]
            if "format" in kwargs:
                timeformat = kwargs["format"]
            if timeformat is not None:
                return Timestamp(datetime.datetime.strptime(a1, timeformat))
            else:

                return datetime.datetime(_year, _month, _day, _hour, _minute, _second)
        elif isinstance(a1, datetime.datetime):
            return a1
        else:
            raise TypeError(f"type(a1) = {type(a1)}")

    def __str__(self):
        return self.strftime("%Y%m%d%H%M%S")

    def __repr__(self):
        return self.strftime("%Y%m%d%H%M%S")

    @classmethod
    def time_range(cls, ):



class Time:
    def __init__(self, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} class cannot be instantiated")

    @staticmethod
    def get_time_str_and_scale(tval: Sequence) -> (list[str], timescale):
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

        return strTrim, timescale.getTimescale(strTrim[0])

    @staticmethod
    def is_time_continuous(times: Sequence) -> bool:
        pass