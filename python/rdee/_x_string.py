#!/usr/bin/env python3
# coding=utf-8

"""
This module contains several functions with relation to string
"""
import os.path
#@sk import
from typing import Sequence


class String:
    def __init__(self, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} class cannot be instantiated")

    @staticmethod
    def trim_suffix(ss: Sequence[str]) -> list[str]:
        """
        This function trims the longest suffix for a sequence of string.
        For example,
            TrimSuffix("20230101000000", "20240202000000")  # get ("20230101", "20240202")
        :param ss: A sequence of string
        :return: A list of trimed string
        """
        longestSuffix_len = len(os.path.commonprefix([s[::-1] for s in ss]))  #@sk use os.path.commonprefix to get longest suffix (prefix for reversed strings in fact)
        return [s[:-longestSuffix_len] for s in ss]
