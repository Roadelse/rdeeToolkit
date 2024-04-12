#!/usr/bin/env python3
# coding=utf-8


"""
This module serves as a global variable holder for the rdee package
"""

import logging

strict: bool = False

logger: logging.Logger | None = None

debugs: tuple | None = None