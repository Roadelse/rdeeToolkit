#coding=utf-8

# ................. standard lib
import unittest
import inspect
# ................. project lib
from .. import _array
from .. import *
# ................. 3rd libs



class TestPrior(unittest.TestCase):
    def setUp(self):
        print(f"\nRunning test: {self.id()}")

    def test_dim_xxx_label_n(self):
        # test : dim_xxx_label_n, dim_xxx_n, get_unique_values_1d_stable
        import numpy as np

        data1 = np.array([1,2,3,4,5,6,7,8,9,10])
        labels1 = [0,0,0,1,1,1,2,2,3,4]
        labels1B = np.array([4, 0,0,0,1,1,1,2,2,3])

        res1 = rdee.dim_xxx_label_n(data1, labels1B, 0, "sum")
        print(res1)

        # data2 = data1.reshape(2, 5)
        # labels2 = ["a", "b", "b", "c", "d"]
        # res2 = rdee.dim_xxx_label_n(data2, labels2, 1, "sum")
        # print(data2)
        # print(res2)

        # data3 = np.arange(16).reshape(4,2,2)
        # labels3 = ["a", "b", "b", "c"]
        # res3 = rdee.dim_xxx_label_n(data3, labels3, 0, "sum")
        # print(data3)
        # print(res3)


    def test_month2season(self):
        import numpy as np

        ms = [1,2,3,4,5,6,7,8,9,10,11,12]

        res = rdee.month2season(ms, {'outMode' : "str"})

        print(res)

    def test_dim_xxx_m2s_n(self):
        yms = ["201701", "201702", "201703", "201704", "201705", "201706", "201707", "201708", "201709", "201710", "201711", "201712"]
        data = [1,2,3,4,5,6,7,8,9,10,11,12]

        res = rdee.dim_xxx_m2s_n(data, 0, yms, "sum")
        print(res)


    def test_write_nc_var(self):
        import netCDF4 as nc4
        import numpy as np

        ncf = nc4.Dataset('test/test_write_nc_var.nc', 'w')
        rdee.write_nc_var(ncf, "test1", [1,2,3,4]) # (ncf, var, varName)
        rdee.write_nc_var(ncf, "test3", ["q","a"]) 
        rdee.write_nc_var(ncf, "test2", np.arange(16).reshape(2, 4, 2))


        ncf.close()


    def test_ind_eq_map(self):
        import numpy as np
        arrP = [1,2,3,4,5,6,7,8,9,10]
        arrC = [2,4,7]

        res = rdee.ind_eq_map(arrP, arrC)

        print(type(res))
        print(res)

        res2 = rdee.ind_eq_map(arrP, np.array(arrC))
        print(type(res2))
        print(res2)


    def test_dim_xxx_cate_n(self):
        # test : test_dim_xxx_cate_n, createSlice
        import numpy as np

        data1 = np.array([1,2,3,4,5,6,7,8,9,10,11])
        labels1 = [0,0,0,1,1,1,2,2,3,4,1]
        cates1 = [0, 1, 2, 3, 4]

        res1 = rdee.dim_xxx_cate_n(data1, labels1, cates1, 0, "sum")
        print(res1)

        data2 = np.array([[1,2,3,4,5], [6,7,8,9,10]])
        labels2 = [0,1,0,2,1]
        cates2 = [0,1,2]
        res2 = rdee.dim_xxx_cate_n(data2, labels2, cates2, 1, "sum")
        print(res2)



    def test_transform_time_reso_rtc(self):
        import configPCS
        import netCDF4 as nc4
        import numpy as np

        config = configPCS.GC({'case' : 'hist', 'tc' : 8})

        f1 = nc4.Dataset(config['WRF_L1_DAILY_DATA'])
        f2 = nc4.Dataset(config['WRF_L1_MONTHLY_DATA'])
        f3 = nc4.Dataset(config['WRF_L1_SEASONAL_DATA'])
        f4 = nc4.Dataset(config['WRF_L1_OMONTHLY_DATA'])
        f5 = nc4.Dataset(config['WRF_L1_OSEASONAL_DATA'])

        T2_f1 = f1.variables['T2'][:].filled(np.nan)
        days = f1.variables['days'][:]
        T2_f2 = f2.variables['T2'][:].filled(np.nan)
        T2_f3 = f3.variables['T2'][:].filled(np.nan)
        T2_f4 = f4.variables['T2'][:].filled(np.nan)
        T2_f5 = f5.variables['T2'][:].filled(np.nan)

        opt_ttrr = {}
        opt_ttrr['method'] = "avg"
        opt_ttrr['time_reso_dst'] = "monthly"
        opt_ttrr['time_fmt_src'] = "%Y%m%d"

        T2_f1_MONTHLY = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
        print(np.sum(np.abs(T2_f1_MONTHLY['data'] - T2_f2)))

        opt_ttrr['time_reso_dst'] = "seasonal"
        T2_f1_SEASONAL = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
        print(np.sum(np.abs(T2_f1_SEASONAL['data'] - T2_f3)))

        opt_ttrr['time_reso_dst'] = "Omonthly"
        T2_f1_OMONTHLY = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
        print(np.sum(np.abs(T2_f1_OMONTHLY['data'] - T2_f4)))

        opt_ttrr['time_reso_dst'] = "Oseasonal"
        T2_f1_OSEASONAL = rdee.transform_time_reso_rtc(T2_f1, 0, days, opt_ttrr)
        print(np.sum(np.abs(T2_f1_OSEASONAL['data'] - T2_f5)))


    def test_xxx_inte(self):
        import rdee
        import numpy as np

        data = np.array([1,2,3,4,5,6,7,8,9,10])
        values = np.array([1,2,3,4,5,6,7,8,9,10])
        method = "sum"
        intervals = [[0, 3], [3, 6]]

        print(rdee.xxx_inte(data, values, intervals, method))

        intervals2 = [[0, 3], [[3, 6], [9, 10]]]

        print(rdee.xxx_inte(data, values, intervals2, method))


    def test_splitAsciiDef_singleTS(self):
        print(rdee.splitAsciiDef_singleTS('A-C,G,Q-Z', '-', ','))


    def test_split_by_true_sep(self):
        s = "a,b,(c,d),e"

        print(rdee.split_by_true_sep(s, ','))


        
class TestArray(unittest.TestCase):
    def setUp(self):
        print(f"\nRunning test: {self.id()}")

    def test_asplit(self):
        a1 = list(range(10))
        s1, s2 = _array.asplit(a1, (0.8, 0.2))
        assert s1 == list(range(8))
        assert s2 == list(range(8, 10))
        s1, s2 = _array.asplit(a1, (0.8, 0.2), random=True)
        assert s1 != list(range(8))


class TestCode(unittest.TestCase):
    def setUp(self):
        print(f"\nRunning test: {self.id()}")

    def test_get_submodules(self):
        import numpy as np
        sms = get_submodules(np)
        self.assertTrue(len(sms) > 30)

    def test_search_api(self):
        import numpy as np
        r = search_api(np, 'random')
        self.assertTrue(len(r) == 3)

    def test_reformat_comments(self):
        """
        Aims to test function:reformat_comments, mainly focusing on its runnability rather than correctness

        @2024-01-06     init
        """
        
        content = """#!/bin/bash
# <L1> l1 comments
# <L2> l2 comments
echo hello u
    # <L3> l3 comments
"""
        ctt_rc_lines = reformat_comments(content).splitlines()
        self.assertEqual(len(ctt_rc_lines), 5)
        self.assertTrue(ctt_rc_lines[-1].startswith('    #'))
        self.assertGreater(len(ctt_rc_lines[1]), 40)
        self.assertGreater(len(ctt_rc_lines[2]), 15)


def run(targets: str):
    """
    Support TestCase Level selection, automatically get target TestCases and load them into a suite, finally run the suite
    """
    allTestCases = []
    for k, v in globals().items():
        if inspect.isclass(v) and issubclass(v, unittest.TestCase):
            allTestCases.append(v)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    # suite.addTest(loader.loadTestsFromTestCase(TestTNA))
    runner = unittest.TextTestRunner()
    # runner.run(suite)

    if targets.lower() == 'all':
        target_tcs = allTestCases
    else:
        target_tcs_name = targets.split(',')
        target_tcs = []
        for tcn in target_tcs_name:
            if '.' in tcn:
                tcn_classname, tcn_methodname = tcn.split('.')
                v = globals().get(tcn_classname)
                if inspect.isclass(v) and issubclass(v, unittest.TestCase) and hasattr(v, tcn_methodname):
                    target_tcs.append((v, tcn_methodname))
            else:
                v = globals().get(tcn)
                if inspect.isclass(v) and issubclass(v, unittest.TestCase):
                    target_tcs.append(v)

    for tc in target_tcs:
        if isinstance(tc, tuple):
            suite.addTest(tc[0](tc[1]))
        else:
            suite.addTest(loader.loadTestsFromTestCase(tc))
    runner.run(suite)
