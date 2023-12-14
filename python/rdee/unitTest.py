#coding=utf-8

import rdee

def test_dim_xxx_label_n():
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


def test_month2season():
    import numpy as np

    ms = [1,2,3,4,5,6,7,8,9,10,11,12]

    res = rdee.month2season(ms, {'outMode' : "str"})

    print(res)

def test_dim_xxx_m2s_n():
    yms = ["201701", "201702", "201703", "201704", "201705", "201706", "201707", "201708", "201709", "201710", "201711", "201712"]
    data = [1,2,3,4,5,6,7,8,9,10,11,12]

    res = rdee.dim_xxx_m2s_n(data, 0, yms, "sum")
    print(res)


def test_write_nc_var():
    import netCDF4 as nc4
    import numpy as np

    ncf = nc4.Dataset('test/test_write_nc_var.nc', 'w')
    rdee.write_nc_var(ncf, "test1", [1,2,3,4]) # (ncf, var, varName)
    rdee.write_nc_var(ncf, "test3", ["q","a"]) 
    rdee.write_nc_var(ncf, "test2", np.arange(16).reshape(2, 4, 2))


    ncf.close()


def test_ind_eq_map():
    import numpy as np
    arrP = [1,2,3,4,5,6,7,8,9,10]
    arrC = [2,4,7]

    res = rdee.ind_eq_map(arrP, arrC)

    print(type(res))
    print(res)

    res2 = rdee.ind_eq_map(arrP, np.array(arrC))
    print(type(res2))
    print(res2)


def test_dim_xxx_cate_n():
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



def test_transform_time_reso_rtc():
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


def test_xxx_inte():
    import rdee
    import numpy as np

    data = np.array([1,2,3,4,5,6,7,8,9,10])
    values = np.array([1,2,3,4,5,6,7,8,9,10])
    method = "sum"
    intervals = [[0, 3], [3, 6]]

    print(rdee.xxx_inte(data, values, intervals, method))

    intervals2 = [[0, 3], [[3, 6], [9, 10]]]

    print(rdee.xxx_inte(data, values, intervals2, method))


def test_splitAsciiDef_singleTS():
    print(rdee.splitAsciiDef_singleTS('A-C,G,Q-Z', '-', ','))


def test_split_by_true_sep():
    s = "a,b,(c,d),e"

    print(rdee.split_by_true_sep(s, ','))


if __name__ == '__main__':
    # test_dim_xxx_label_n()

    # test_month2season()

    # test_dim_xxx_m2s_n()

    # test_write_nc_var()

    # test_ind_eq_map()

    # test_dim_xxx_cate_n()

    # test_transform_time_reso_rtc()

    # test_splitAsciiDef_singleTS()

    test_split_by_true_sep()