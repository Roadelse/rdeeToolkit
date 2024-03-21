#coding=utf-8

# ................. standard lib
import os
import os.path

import unittest
import inspect

import numpy as np


# ................. project lib
# ................. 3rd libs



# class TestPrior(unittest.TestCase):
#     def setUp(self):
#         print(f"\nRunning test: {self.id()}")

#     def test_dim_xxx_label_n(self):
#         # test : dim_xxx_label_n, dim_xxx_n, get_unique_values_1d_stable
#         import numpy as np

#         data1 = np.array([1,2,3,4,5,6,7,8,9,10])
#         labels1 = [0,0,0,1,1,1,2,2,3,4]
#         labels1B = np.array([4, 0,0,0,1,1,1,2,2,3])

#         res1 = rdee.dim_xxx_label_n(data1, labels1B, 0, "sum")
#         print(res1)

#         # data2 = data1.reshape(2, 5)
#         # labels2 = ["a", "b", "b", "c", "d"]
#         # res2 = rdee.dim_xxx_label_n(data2, labels2, 1, "sum")
#         # print(data2)
#         # print(res2)

#         # data3 = np.arange(16).reshape(4,2,2)
#         # labels3 = ["a", "b", "b", "c"]
#         # res3 = rdee.dim_xxx_label_n(data3, labels3, 0, "sum")
#         # print(data3)
#         # print(res3)


#     def test_month2season(self):
#         import numpy as np

#         ms = [1,2,3,4,5,6,7,8,9,10,11,12]

#         res = rdee.month2season(ms, {'outMode' : "str"})

#         print(res)

#     def test_dim_xxx_m2s_n(self):
#         yms = ["201701", "201702", "201703", "201704", "201705", "201706", "201707", "201708", "201709", "201710", "201711", "201712"]
#         data = [1,2,3,4,5,6,7,8,9,10,11,12]

#         res = rdee.dim_xxx_m2s_n(data, 0, yms, "sum")
#         print(res)


#     def test_write_nc_var(self):
#         import netCDF4 as nc4
#         import numpy as np

#         ncf = nc4.Dataset('test/test_write_nc_var.nc', 'w')
#         rdee.write_nc_var(ncf, "test1", [1,2,3,4]) # (ncf, var, varName)
#         rdee.write_nc_var(ncf, "test3", ["q","a"]) 
#         rdee.write_nc_var(ncf, "test2", np.arange(16).reshape(2, 4, 2))


#         ncf.close()


#     def test_ind_eq_map(self):
#         import numpy as np
#         arrP = [1,2,3,4,5,6,7,8,9,10]
#         arrC = [2,4,7]

#         res = rdee.ind_eq_map(arrP, arrC)

#         print(type(res))
#         print(res)

#         res2 = rdee.ind_eq_map(arrP, np.array(arrC))
#         print(type(res2))
#         print(res2)


#     def test_dim_xxx_cate_n(self):
#         # test : test_dim_xxx_cate_n, createSlice
#         import numpy as np

#         data1 = np.array([1,2,3,4,5,6,7,8,9,10,11])
#         labels1 = [0,0,0,1,1,1,2,2,3,4,1]
#         cates1 = [0, 1, 2, 3, 4]

#         res1 = rdee.dim_xxx_cate_n(data1, labels1, cates1, 0, "sum")
#         print(res1)

#         data2 = np.array([[1,2,3,4,5], [6,7,8,9,10]])
#         labels2 = [0,1,0,2,1]
#         cates2 = [0,1,2]
#         res2 = rdee.dim_xxx_cate_n(data2, labels2, cates2, 1, "sum")
#         print(res2)



#     def test_transform_time_reso_rtc(self):
#         import configPCS
#         import netCDF4 as nc4
#         import numpy as np

#         config = configPCS.GC({'case' : 'hist', 'tc' : 8})

#         f1 = nc4.Dataset(config['WRF_L1_DAILY_DATA'])
#         f2 = nc4.Dataset(config['WRF_L1_MONTHLY_DATA'])
#         f3 = nc4.Dataset(config['WRF_L1_SEASONAL_DATA'])
#         f4 = nc4.Dataset(config['WRF_L1_OMONTHLY_DATA'])
#         f5 = nc4.Dataset(config['WRF_L1_OSEASONAL_DATA'])

#         T2_f1 = f1.variables['T2'][:].filled(np.nan)
#         days = f1.variables['days'][:]
#         T2_f2 = f2.variables['T2'][:].filled(np.nan)
#         T2_f3 = f3.variables['T2'][:].filled(np.nan)
#         T2_f4 = f4.variables['T2'][:].filled(np.nan)
#         T2_f5 = f5.variables['T2'][:].filled(np.nan)

#         opt_ttrr = {}
#         opt_ttrr['method'] = "avg"
#         opt_ttrr['time_reso_dst'] = "monthly"
#         opt_ttrr['time_fmt_src'] = "%Y%m%d"

#         T2_f1_MONTHLY = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
#         print(np.sum(np.abs(T2_f1_MONTHLY['data'] - T2_f2)))

#         opt_ttrr['time_reso_dst'] = "seasonal"
#         T2_f1_SEASONAL = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
#         print(np.sum(np.abs(T2_f1_SEASONAL['data'] - T2_f3)))

#         opt_ttrr['time_reso_dst'] = "Omonthly"
#         T2_f1_OMONTHLY = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
#         print(np.sum(np.abs(T2_f1_OMONTHLY['data'] - T2_f4)))

#         opt_ttrr['time_reso_dst'] = "Oseasonal"
#         T2_f1_OSEASONAL = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
#         print(np.sum(np.abs(T2_f1_OSEASONAL['data'] - T2_f5)))


#     def test_xxx_inte(self):
#         import rdee
#         import numpy as np

#         data = np.array([1,2,3,4,5,6,7,8,9,10])
#         values = np.array([1,2,3,4,5,6,7,8,9,10])
#         method = "sum"
#         intervals = [[0, 3], [3, 6]]

#         print(rdee.xxx_inte(data, values, intervals, method))

#         intervals2 = [[0, 3], [[3, 6], [9, 10]]]

#         print(rdee.xxx_inte(data, values, intervals2, method))


#     def test_splitAsciiDef_singleTS(self):
#         print(rdee.splitAsciiDef_singleTS('A-C,G,Q-Z', '-', ','))


#     def test_split_by_true_sep(self):
#         s = "a,b,(c,d),e"

#         print(rdee.split_by_true_sep(s, ','))

        
# class TestArray(unittest.TestCase):
#     def setUp(self):
#         print(f"\nRunning test: {self.id()}")

#     def test_asplit(self):
#         a1 = list(range(10))
#         s1, s2 = _array.asplit(a1, (0.8, 0.2))
#         assert s1 == list(range(8))
#         assert s2 == list(range(8, 10))
#         s1, s2 = _array.asplit(a1, (0.8, 0.2), random=True)
#         assert s1 != list(range(8))


# class TestCode(unittest.TestCase):
#     def setUp(self):
#         print(f"\nRunning test: {self.id()}")

#     def test_get_submodules(self):
#         import numpy as np
#         sms = get_submodules(np)
#         self.assertTrue(len(sms) > 30)

#     def test_search_api(self):
#         import numpy as np
#         r = search_api(np, 'random')
#         self.assertTrue(len(r) == 3)

#     def test_reformat_comments(self):
#         """
#         Aims to test function:reformat_comments, mainly focusing on its runnability rather than correctness

#         @2024-01-06     init
#         """
        
#         content = """#!/bin/bash
# # <L1> l1 comments
# # <L2> l2 comments
# echo hello u
#     # <L3> l3 comments
# """
#         ctt_rc_lines = reformat_comments(content).splitlines()
#         self.assertEqual(len(ctt_rc_lines), 5)
#         self.assertTrue(ctt_rc_lines[-1].startswith('    #'))
#         self.assertGreater(len(ctt_rc_lines[1]), 40)
#         self.assertGreater(len(ctt_rc_lines[2]), 15)

class Test_Logging(unittest.TestCase):
    """
    This class contains several test functions in relation with logging
    """
    def setUp(self) -> None:
        """
        print start information via puer print()
        &
        prepare test directory and enter it
        """
        from .. import rmrf

        print(f"\n***************************************************")
        print(f"Running test: {self.id()}")
        print(f"***************************************************")
        #@sk <get-path/>
        casename, funcname = self.id().split(".")[-2:]
        testDir: str = f"ade.utest/{casename[5:]}/{funcname[5:]}"

        #@sk <os-operation desc="mkdir -> rm -rf -> cd, and store the current working directory"/>
        os.makedirs(testDir, exist_ok=True)
        rmrf(testDir, use_strict=True)
        self.wdir = os.path.curdir  #@sk store working path for go back in self.tearDown()
        os.chdir(testDir)

    def tearDown(self) -> None:
        """
        Go back to original workding directory
        """
        print("\n\n\n")
        os.chdir(self.wdir)
        return super().tearDown()

    def test_getLogger(self):
        """
        This function aims to test getLogger in _x_logging module, which should first resolve selcted/default local logging config then return corresponding logger, and, if not matchable, return a new logger with default settings (but can also controlled a bit via argument)
        This function trying 3 loggers, the "root" and "test1" are defined in local logging.config, and "test2" are not. The consolve should print all information from the 3 loggers, and test1.log & test2.log would be written. While, the latter is checked using self.assert..., but the prior feature needs eyes to see.
        """

        #@sk import
        from .. import getLogger, getAllHandlers 

        #@sk prepare write a local logging.config
        with open("logging.config", "w") as f:
            f.write("""
[loggers]
keys=root,test1

[handlers]
keys=console1,file1

[formatters]
keys=fmtfile,fmtcsl

[filters]
keys=ft1

[logger_root]
level=INFO
handlers=console1
qualname=root

[logger_test1]
level=DEBUG
handlers=file1
qualname=test1
; if set to 0, test1 logger will not trigger root logger handlers
propagate=1

[handler_console1]
class=StreamHandler
level=DEBUG
formatter=fmtcsl
args=(sys.stdout,)

[handler_file1]
class=logging.handlers.RotatingFileHandler
level=DEBUG
formatter=fmtfile
args=('test1.log', 'a', 20000, 5)

[formatter_fmtfile]
format=%(asctime)s  (%(name)s)  [%(levelname)s]  %(message)s
datefmt=%Y-%m-%d %H:%M:%S

[formatter_fmtcsl]
format=\033[4m%(asctime)s \033[0m (\033[33m%(funcName)s\033[0m)  [\033[32m%(levelname)s\033[0m]  %(message)s
datefmt=%Y-%m-%d %H:%M:%S

""")

        #@sk prepare remove the getLogger.configured so it can load the created local config file
        delattr(getLogger, "configured")  #@sk because python -m package will still run the __init__.py statements, while the `logger = getLogger("rdee")` statement will try to load local config file (doesn't exist at that time) and marks it "configured" then.

        #@sk <do desc="do the core statements">
        #@sk <basic desc="test basic functionality" />
        logger = getLogger("root")
        logger1 = getLogger("test1")
        logger2 = getLogger("test2", fpath="test2.log")
        logger.info("info from root")
        logger1.info("info from test1")
        logger2.info("info from test2")
        #@sk <envfilter desc="test envfilter" />
        logger1.info("2nd info from test1")
        os.environ["reDebugTargets"] = "whoru"
        logger3 = getLogger("test3", fpath="test3.log")
        logger2.info("2nd info from test2")
        logger3.info("info from test3")
        #@sk </do>
    

        #@sk check
        self.assertTrue(os.path.exists("test1.log"))
        self.assertTrue(os.path.exists("test2.log"))
        self.assertTrue(os.path.exists("test3.log"))  #@sk log file will be created even no message passed

        self.assertEqual(2, len(open("test1.log").readlines()))
        self.assertEqual(2, len(open("test2.log").readlines()))
        self.assertEqual("", open("test3.log").read())


class Test_basicfunc(unittest.TestCase):
    def setUp(self) -> None:
        print(f"\n***************************************************")
        print(f"Running test: {self.id()}")
        print(f"***************************************************")
        return super().setUp()
    
    def test_singleton(self):
        """
        This function aims to test usage of singleton decorator
        """
        import random
        from .. import singleton

        @singleton
        class cc:
            def __init__(self):
                self.rvalue = random.random()

        ins1 = cc()
        ins2 = cc()
        self.assertEqual(ins1.rvalue, ins2.rvalue)


class Test_string(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_TrimSuffix(self):
        from .. import String

        ss = ["20240201105000", "20240201105100"]
        ssTrim = String.trim_suffix(ss)
        self.assertListEqual(["202402011050", "202402011051"], ssTrim)


class Test_time(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_time_str_and_scale(self) -> None:
        from datetime import datetime
        from .._x_time import Time
        ts1 = (
            datetime(2024, 2, 1, 11, 8, 14, 602249),
            datetime(2024, 2, 1, 11, 8, 15, 135897)
        )
        ts2 = (
            datetime(2024, 2, 1, 11),
            datetime(2021, 2, 1, 13)
        )

        ts1_str = Time.get_time_str_and_scale(ts1)
        self.assertListEqual(["20240201110814", "20240201110815"], ts1_str)
        ts2_str = Time.get_time_str_and_scale(ts2)
        self.assertListEqual(["2024020111", "2021020113"], ts2_str)


class Test_array(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_drp(self):
        """
        This function aims to test Array.drp, including test items:
            ● Array.drp(arr1, dims=1, op=DRPC.max)
                test basic functionality
            ● Array.drp(arr1, dims=2, op=DRPC.min, mapping=...)
                test basic mapping
        """

        from .._x_array import Array, DRPC  #@sk import

        arr1 = np.arange(24).reshape((2,3,4))
        arr1_drp = Array.drp(arr1, dims=1, op=DRPC.max)
        self.assertListEqual([8,9,10,11,20,21,22,23], arr1_drp.reshape(-1).tolist())  #@sk reference list is set manually

        arr1_drp = Array.drp(arr1, dims=2, op=DRPC.min, mapping={0:[2,3], 1:[0, 1]})
        self.assertListEqual([2,0,6,4,10,8,14,12,18,16,22,20], arr1_drp.reshape(-1).tolist())  #@sk reference list is set manually


class Test_win(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_win2wsl(self) -> None:
        from  rdee import path_win2wsl, path_wsl2win
        self.assertEqual("/mnt/d/recRoot/Roadelse/Life/Daily", path_win2wsl(r"D:\recRoot\Roadelse\Life\Daily"))
        self.assertEqual(r"D:\recRoot\Roadelse\Life\Daily", path_wsl2win(r"/mnt/d/recRoot/Roadelse/Life/Daily"))
        
        with self.assertRaises(Exception):
            path_win2wsl(r"D:\recRoot\Roadelse\Life\Daily\ababa", require_existed=True)
        with self.assertRaises(Exception):
            path_wsl2win(r"/mnt/g/recRoot/Roadelse/Life/Daily", require_existed=True)


def run(targets: list[str]) -> None:
    """
    Runner for the test cases & test functions in this utest packaghe
    Support both TestCase-Level and test_function-level selections, automatically get target TestCases/test-functions and load them into a suite, finally run the suite
    :param targets: a list fo targets to be tested, if empty, run all the tests
    """

    #@sk <prepare desc="get all TestCases and TestFunctions in two dictionaries"/>
    allTestCases = {}
    for k, v in globals().items():
        if inspect.isclass(v) and issubclass(v, unittest.TestCase):
            allTestCases[k] = v

    allTestFunctions = {}
    for k, tc in allTestCases.items():
        for mpf in dir(tc):
            if mpf.startswith("test_"):
                allTestFunctions[mpf] = (tc, mpf)

    #@sk <prepare desc="" />
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()

    #@sk <core desc="parse arguments to confirm target TestCases and TestFunctions">
    if not targets:  #@sk branch Handle param-boundary conditions that no targets are set
        target_tcs = list(allTestCases.values())
    else:  #@sk branch normal conditions
        target_tcs = []
        for tcn in targets:
            #@sk <classify desc="parsing 3 kinds of target: TestCase, TestFunction, and TestCase.TestFunction, prefix can be omitted">
            if '.' in tcn:  #@sk branch TestCase.TestFunction
                tcn_classname, tcn_methodname = tcn.split('.')
                tcn_classname = "Test_" + tcn_classname if not tcn_classname.startswith("Test_") else tcn_classname
                tcn_methodname = "test_" + tcn_methodname if not tcn_methodname.startswith("test_") else tcn_methodname

                v = globals().get(tcn_classname)
                if inspect.isclass(v) and issubclass(v, unittest.TestCase) and hasattr(v, tcn_methodname):  #@sk exp use STL:inspect to detect if a symbol denoting class
                    target_tcs.append((v, tcn_methodname))
            elif tcn in allTestCases or f"Test_{tcn}" in allTestCases:  #@sk branch TestCase
                tcn = "Test_" + tcn if not tcn.startswith("Test_") else tcn
                target_tcs.append(allTestCases[tcn])
            elif tcn in allTestFunctions or f"test_{tcn}" in allTestFunctions:  #@sk branch TestFunction
                tcn = "test_" + tcn if not tcn.startswith("test_") else tcn
                target_tcs.append(allTestFunctions[tcn])
            else:  #@sk branch error conditions
                raise RuntimeError(f"Error! Illegal test target, neither TestCase name nor TestFunction name! {tcn}")
            #@sk </classify>
    #@sk </core>


    #@sk <tail desc="run the target tests"/>
    # print(target_tcs)
    for tc in target_tcs:
        if isinstance(tc, tuple):
            suite.addTest(tc[0](tc[1]))  #@sk Here we actually instantiate the TestCase class, the function name is used to tell which function should be tested
        else:
            suite.addTest(loader.loadTestsFromTestCase(tc))
    runner.run(suite)
