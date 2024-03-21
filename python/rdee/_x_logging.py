#!/usr/bin/env python3
# coding=utf-8

"""
This module contains functions serving logging during script running
"""

#@sk <import>
import os.path
import sys
import logging
import logging.config
#@sk </import>


def getAllHandlers(lgr: logging.Logger) -> list[logging.Handler]:
    """
    This function aims to get all handlers for given logger, via go through all its ancestor loggers
    """
    rstList: list[logging.Handler] = []
    while lgr is not None:
        rstList.extend(lgr.handlers)
        lgr = lgr.parent
    return rstList


def has_stdout_handler(lgr: logging.Logger) -> bool:
    """
    This function aims to check if a logger has a stdout StreamHandler
    """
    ahs: list[logging.Handler] = getAllHandlers(lgr)
    for h in ahs:
        if isinstance(h, logging.StreamHandler) and h.stream is sys.stdout:
            return True
    return False


def getLogger(name, configfile: str = "logging.config", clevel = logging.DEBUG, flevel = logging.DEBUG, fpath: str = "", propagate: bool = True) -> logging.Logger:
    """
    This function aims to get a logging.Logger according to arg:name, after loading local selected/default config file.
    :param name: target name for logger
    :param configfile: local config file path
    :param clevel: used to set console handler level during initializing a new logger 
    :param flevel: used to set file handler level during initializing a new logger   
    :param fpath: used to set logfile path for file handler during initializing a new logger 

    :return: a logging.Logger
    """

    #@sk <inner-functions>
    #@sk <config desc="load local configfile"/>
    def config():
        if os.path.exists(configfile):
            logging.config.fileConfig(configfile)

    #@sk <envfilter desc="add default environment filter"/>
    def envfilter(record: logging.LogRecord) -> bool:
        #@sk <once-through desc="get filter targets in this running"/>
        if not hasattr(envfilter, "targets"):
            targetStr = os.getenv("reDebugTargets")
            if targetStr:
                setattr(envfilter, "targets", targetStr.split(","))
            else:
                setattr(envfilter, "targets", None)

        #@sk <judge desc="judge if record should be filtered based on targets"/>
        targets = getattr(envfilter, "targets")
        if targets is None:
            return True
        else:
            return record.funcName in targets
    #@sk </inner-functions>


    #@sk <once-through desc="load local config file"/>
    if not hasattr(getLogger, "configured"):
        config()
        setattr(getLogger, "configured", 1)

    #@sk <core desc="get logger, set logger">
    logger: logging.Logger = logging.getLogger(name)

    if envfilter not in logger.filters:  #@sk branch add filter at first get
        logger.addFilter(envfilter)
    
    if logger.handlers:  #@sk branch return if logger has been configured in local config or last call
        return logger
    
    #@sk <set-logger desc="setting logger based on arguments" />
    logger.setLevel(logging.DEBUG)

    if not has_stdout_handler(logger) and clevel is not None:  #@sk branch set console handler
        sh = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter('\033[4m%(asctime)s \033[0m (\033[33m%(funcName)s\033[0m) [\033[32m%(levelname)s\033[0m]  %(message)s', '%Y-%m-%d %H:%M:%S')
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        logger.addHandler(sh)

    if flevel is not None and fpath != "":  #@sk branch set file handler
        fh = logging.FileHandler(fpath)
        fmt = logging.Formatter('%(asctime)s (%(funcName)s) [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fh.setFormatter(fmt)
        fh.setLevel(flevel)
        logger.addHandler(fh)
    
    #@sk </core>

    return logger


