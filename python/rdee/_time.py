# coding=utf-8

#**********************************************************************
# This function aims to simplify time-statistc by keys
#**********************************************************************
def rdTimer(key: any, init: int = 0):
    import time
    if not init and hasattr(rdTimer, key):
        rst = time.time() - getattr(rdTimer, key)
        setattr(rdTimer, key, time.time())
        print(f">>> time cost is {rst} for {key}")
        return rst
    else:
        setattr(rdTimer, key, time.time())
    return



#**********************************************************************
# This function is used to get MM from times such as YYYYMMDD, 
# YYYYMM
#**********************************************************************
def getMM(times, opt = None) :
    # times : list of time, format : yyyymm, yyyymmdd, yyyymmdhh
    assert type(times[0]) == str, 'Error, [times] should be str!'
    f = lambda x : x[4:6]
    res = [f(i) for i in times]

    return res


#**********************************************************************
# this function is used to resolve month definitions
# such as "201501-201503,201609,201612-201702,201712"
#**********************************************************************
def resolveMonths(months) : 
    # months - YYYYMM,YYYYMM,YYYYMM-YYYYMM,YYYYMM
    # return : an array[] contains all yyyymm
    res = []
    monthDefs = months.split(',')
    for md in monthDefs:
        if '-' not in md:
            res.append(md)
        else:
            ym1, ym2 = md.split('-')
            ymaT = render_ym_series(ym1, ym2) # yyyymm array temp
            res.extend(ymaT)

    return res


#**********************************************************************
# this function is used to resolve date definitions
# such as "201501-201503,201609,201612-201702,201712"
#**********************************************************************
def resolveDates(dateDef) : 
    # dates - YYYYMMDD,YYYYMMDD,YYYYMMDD-YYYYMMDD,YYYYMMDD
    # return : an array[] contains all yyyymmdd
    res = []
    dateDef_arr = dateDef.split(',')
    for ymd in dateDef_arr:
        if '-' not in ymd:
            res.append(ymd)
        else:
            ymd1, ymd2 = ymd.split('-')
            ymdaT = render_ymd_series(ymd1, ymd2) # yyyymmdd array temp
            res.extend(ymdaT)

    return res


#**********************************************************************
# This function is used to calculate MDA8 data from hourly data
#**********************************************************************
def hour2MDA8(data):
    import numpy as np

    assert type(data) == np.ndarray, 'plz use numpy array as parameter <data>'
    nhours = data.shape[0]
    assert nhours % 24 == 0, 'this function <hour2MDA8> need the first dim of data reapresenting hour and ranging from 0 to 23!'
    ndays = nhours // 24

    ndims = len(data.shape)

    newShape = list(data.shape)
    newShape[0] = ndays
    res = np.zeros(newShape)
    res[:] = np.nan

    for d in range(ndays):
        movAvgs = np.zeros([17] + newShape[1:])
        for d in range(17):
            if len(data.shape) > 1:
                movAvgs[d, :] = np.mean(data[d : d + 8, :], 0)
            else:
                movAvgs[d] = np.mean(data[d : d + 8])
        if len(res.shape) > 1:
            res[d, :] = np.max(movAvgs, 0)
        else:
            res[d] = np.max(movAvgs, 0)

    return res


def month2season(ms, opt = {}):
    # ms : array of str like 01, 02, 03, ...... 12 
    #   or integer from 1 to 12
    # opt ->
    #   @outMode : int/integer, name, string
    # ---------------------------------
    # return spring, summer, fall, winter 
    #     or 0, 1, 2, 3
    #     or "0", "1", "2", "3"
    import sys
    import numpy as np

    if 'outMode' in opt:
        outMode = opt['outMode']
    else:
        outMode = "int"

    npm = np.array(ms, dtype = np.int)
    # print(npm)

    seasons = np.empty(npm.size, dtype = np.int)
    # print(seasons)
    seasons = np.where(np.logical_and(npm >= 3, npm <= 5), 0, seasons)
    # print(seasons)
    seasons = np.where(np.logical_and(npm >= 6, npm <= 8), 1, seasons)
    # print(seasons)
    seasons = np.where(np.logical_and(npm >= 9, npm <= 11), 2, seasons)
    # print(seasons)
    seasons = np.where(np.logical_or(npm <= 2, npm == 12), 3, seasons)
    # print(seasons)

    if outMode in ['int', 'integer']:
        return seasons
    elif outMode in ['str', 'string']:
        return ["{:02d}".format(i) for i in seasons] # seasons.astype(np.str)
    elif outMode == 'name':
        names = np.array(["spring", "summer", "fall", "winter"])
        return names[seasons]
    else:
        print("unknown outMode : {}".format(outMode))
        sys.exit(1)


#**********************************************************************
# This function is used to calculate seasonal mean data from monthly data
#**********************************************************************
def dim_xxx_m2s_n(data, idim, yms, method):
    # yms : an array, format : yyyymm
    import numpy as np
    from . import _array

    data_np = np.array(data)

    # yms_np = np.array(yms)
    ys = list(map(lambda x : x[:4], yms))
    ms = list(map(lambda x : x[4:], yms))

    ssI = month2season(ms)
    ss = ssI.astype(np.str)

    yss = np.array([ys[i] + ss[i] for i in range(ss.size)])
    yss2 = yss.copy()
    yss2.sort()

    yssU = np.unique(yss)
    nyss = yssU.size

    ndims = len(data_np.shape)

    res = _array.dim_xxx_cate_n(data, yss, yssU, idim, method)

    return {'data' : res, 'times' : yssU}

#**********************************************************************
# This function is used to transform time-resolution with time-coord 
# remained
#**********************************************************************
def transform_time_reso_rtc(data, idim, time, opt):
    from ._array import dim_xxx_n, dim_xxx_label_n, dim_xxx_cate_n
    # time : an array of strings representing datetime, such as 2017010123, 202106, ... ...

    # opt@
    #   time_reso_dst : "monthly", "annual", ... ...
    #   time_fmt_src : "%Y%m%d%H", ... ...

    assert "time_fmt_src" in opt and "time_reso_dst" in opt, "function <transform_time_reso_rtc>, param-opt must have attr-time_fmt_src and attr-time_reso_dst"

    import numpy as np
    import datetime

    method = "avg"
    if 'method' in opt:
        method = opt['method']

    if opt['time_reso_dst'] == "period" : 
        return {'data' : dim_xxx_n(data, idim, method), 'times' : 'period' }

    pydtms_src = list(map(lambda x : datetime.datetime.strptime(x, opt['time_fmt_src']), time))

    if opt['time_reso_dst'] == 'daily':
        pydtms_dst = list(map(lambda x : datetime.datetime.strftime(x, "%Y%m%d"), pydtms_src))
        res = dim_xxx_label_n(data, pydtms_dst, idim, method)
        return {'data' : res['data'], 'times' : res['labels']}
    elif opt['time_reso_dst'] == 'monthly':
        pydtms_dst = list(map(lambda x : datetime.datetime.strftime(x, "%Y%m"), pydtms_src))
        res = dim_xxx_label_n(data, pydtms_dst, idim, method)
        return {'data' : res['data'], 'times' : res['labels']}
    elif opt['time_reso_dst'] == 'annual':
        pydtms_dst = list(map(lambda x : datetime.datetime.strftime(x, "%Y"), pydtms_src))
        res = dim_xxx_label_n(data, pydtms_dst, idim, method)
        return {'data' : res['data'], 'times' : res['labels']}
    elif opt['time_reso_dst'] == 'seasonal':
        pydtms_dst = list(map(lambda x : datetime.datetime.strftime(x, "%Y%m"), pydtms_src))
        resM = dim_xxx_label_n(data, pydtms_dst, idim, method)
        res = dim_xxx_m2s_n(resM['data'], idim, resM['labels'], method) # {'data' : ..., 'times' : ...}
        return res
    elif opt['time_reso_dst'] == 'Omonthly' :
        pydtms_dst = list(map(lambda x : datetime.datetime.strftime(x, "%Y%m"), pydtms_src))
        resM = dim_xxx_label_n(data, pydtms_dst, idim, method)
        yms = resM['labels']
        mms = getMM(yms)
        mmsU = np.unique(mms)
        res = dim_xxx_cate_n(resM['data'], mms, mmsU, idim, method)
        return {'data' : res, 'times' : mmsU}
    elif opt['time_reso_dst'] == 'Oseasonal' :
        pydtms_dst = list(map(lambda x : datetime.datetime.strftime(x, "%Y%m"), pydtms_src))
        resM = dim_xxx_label_n(data, pydtms_dst, idim, method)
        resS = dim_xxx_m2s_n(resM['data'], idim, resM['labels'], method) # {'data' : ..., 'times' : ...}
        yss = resS['times']
        ss = [x[4] for x in yss]
        ssU = np.unique(ss)
        assert ssU.size == 4, 'function <transform_time_reso_rtc> : unexpected ssu size {}'.format(ssU.size)
        ssU.sort()
        assert np.all(ssU == ['0', '1', '2', '3']), 'function <transform_time_reso_rtc> : unexpected ssU : {}'.format(ssU)

        res = dim_xxx_cate_n(resS['data'], ss, ssU, idim, method)

        return {'data' : res, 'times' : ssU}
    else:
        print("function <transform_time_reso_rtc> : unknown time_reso_dst {}".format(opt['time_reso_dst']))


    


#**********************************************************************
# This function is used to calculate the number of days for given month
# supported format : yyyymm
#**********************************************************************
def get_ndays_of_ym(ym):
    import datetime, sys
    dh_py = datetime.datetime.strptime(ym, "%Y%m")
    delta = datetime.timedelta(days = 1)
    count = 0
    while True:
        if dh_py.day == 1 and count > 0:
            break
        dh_py += delta
        count += 1

    return count


#**********************************************************************
# This function is used to render time series 
# with format of "%Y%m%d%H"
#**********************************************************************
def render_dh_series(dh1, dh2):
    import datetime, sys
    dh_format = "%Y%m%d%H"
    dh1_py = datetime.datetime.strptime(dh1, dh_format)
    dh2_py = datetime.datetime.strptime(dh2, dh_format)
    delta = datetime.timedelta(hours = 1)
    res = []
    while dh1_py <= dh2_py:
        res.append(dh1_py.strftime(dh_format))
        dh1_py += delta

    return res


#**********************************************************************
# This function is used to render time series 
# with format of "%Y%m"
#**********************************************************************
def render_ym_series(ym1, ym2):
    import datetime
    from dateutil.relativedelta import relativedelta  # datetime.timedelta doesn't support "months=1"
    ym_format = "%Y%m"
    ym1_py = datetime.datetime.strptime(ym1, ym_format)
    ym2_py = datetime.datetime.strptime(ym2, ym_format)
    delta = relativedelta(months=1)
    res = []
    while ym1_py <= ym2_py:
        res.append(ym1_py.strftime(ym_format))
        ym1_py += delta

    return res



#**********************************************************************
# This function is used to render time series 
# with format of "%Y%m"
#**********************************************************************
def render_ymd_series(ymd1, ymd2):
    import datetime
    # from dateutil.relativedelta import relativedelta  # datetime.timedelta doesn't support "months=1"
    ymd_format = "%Y%m%d"
    ymd1_py = datetime.datetime.strptime(str(ymd1), ymd_format)
    ymd2_py = datetime.datetime.strptime(str(ymd2), ymd_format)
    delta = datetime.timedelta(days=1)
    res = []
    while ymd1_py <= ymd2_py:
        res.append(ymd1_py.strftime(ymd_format))
        ymd1_py += delta

    return res


def render_ymdh_series(ymdh1, ymdh2):
    import datetime
    # from dateutil.relativedelta import relativedelta  # datetime.timedelta doesn't support "months=1"
    ymdh_format = "%Y%m%d%H"
    ymdh1_py = datetime.datetime.strptime(ymdh1, ymdh_format)
    ymdh2_py = datetime.datetime.strptime(ymdh2, ymdh_format)
    delta = datetime.timedelta(hours=1)
    res = []
    while ymdh1_py <= ymdh2_py:
        res.append(ymdh1_py.strftime(ymdh_format))
        ymdh1_py += delta

    return res

# def render_weekday_series(ymd1, ymd2):
#     import datetime

#     ymd_format = "%Y%m%d"
#     ymd1_py = datetime.datetime.strptime(ymd1, ymd_format).date()
#     ymd2_py = datetime.datetime.strptime(ymd2, ymd_format).date()
#     delta = datetime.timedelta(days=1)
#     res = []
#     while ymd1_py <= ymd2_py:
#         res.append(ymd1_py.weekday())
#         ymd1_py += delta

#     return res

def render_weekday_series(ymds): # reload 
    import datetime

    ymd_format = "%Y%m%d"

    res = []
    for ymd in ymds:
        dtT = datetime.datetime.strptime(ymd, ymd_format).date()
        res.append(dtT.weekday())

    return res



#**********************************************************************
# This function is used to shift a time-str-series
#**********************************************************************
def shiftTimeStr(timeStr, shift, unit):
    # timeStr : yyyymmddhh
    import datetime, sys
    dh_format = "%Y%m%d%H"
    dh_py = datetime.datetime.strptime(timeStr, dh_format)
    if 'day' in unit:
        delta = datetime.timedelta(days = shift)
    elif 'hour' in unit:
        delta = datetime.timedelta(hours = shift)
    elif 'month' in unit:
        print("not supported by now, plz add code! need to use another lib")
        sys.exit(1)
    elif 'year' in unit:
        print("not supported by now, plz add code!")
        sys.exit(1)

    dh_res_py = dh_py + delta

    return dh_res_py.strftime(dh_format)


