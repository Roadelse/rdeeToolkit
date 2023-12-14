# coding=utf-8


#**********************************************************************
# this function is used to calculate metrics
#**********************************************************************
def evaMetrics(xs, base):
    from scipy import stats
    import numpy as np

    assert xs.shape == base.shape and len(xs.shape) == 1, 'xs and base should own the same length as an 1-dimensional array!'
    R, rp = stats.pearsonr(xs, base)
    lens = len(xs)

    BIAS = sum(xs - base) / lens
    ERROR = sum(abs(xs - base)) / lens
    NMB = sum(xs - base) / sum(base) * 100
    NME = sum(abs(xs - base)) / sum(base) * 100
    FBIAS = sum((xs - base) / (xs + base)) / lens * 2 * 100
    FERROR = sum(abs((xs - base) / (xs + base))) / lens * 2 * 100
    RSME = np.sqrt(((xs - base).astype('double') ** 2).mean())

    a, b = np.polyfit(base, xs, 1)

    return dict(R=R, rp= rp, BIAS= BIAS, ERROR= ERROR, NMB= NMB, NME= NME, FBIAS= FBIAS, FERROR= FERROR, RSME=RSME, a=a, b=b)



#**********************************************************************
# this script is used to calculate left T,TD and RH given 2 of them
# ref : https://bmcnoldy.rsmas.miami.edu/Humidity.html
#**********************************************************************
def T_TD_RH(T = None, TD = None, RH = None):
    # Last update @ 2021-07-28 14:11:15
    from math import log, exp
    if T == None:
        assert TD != None and RH != None, "function <T_TD_RH> : T, TD and RH, 2 of them should be assigned manually! Error"
        res = 243.04*(((17.625*TD)/(243.04+TD))-log(RH/100))/(17.625+log(RH/100)-((17.625*TD)/(243.04+TD)))
    elif TD == None:
        assert T != None and RH != None, "function <T_TD_RH> : T, TD and RH, 2 of them should be assigned manually! Error"
        res = 243.04*(log(RH/100)+((17.625*T)/(243.04+T)))/(17.625-log(RH/100)-((17.625*T)/(243.04+T)))
    elif RH == None:
        assert T != None and TD != None, "function <T_TD_RH> : T, TD and RH, 2 of them should be assigned manually! Error"
        res = 100*(exp((17.625*TD)/(243.04+TD))/exp((17.625*T)/(243.04+T)))

    return res



#**********************************************************************
# this script is used to convert MEE obs (ug/m3) to ppbv
#**********************************************************************
def MEE_ugm3_to_ppbv(var, data, idim, times):
    import numpy as np
    import sys
    from rdee_array import createSlice


    index_nso = np.argwhere(times < "20180901").reshape(-1)
    index_nsn = np.argwhere(times >= "20180901").reshape(-1)

    sl_nso = createSlice(len(data.shape), targetIndexDict = {idim : index_nso})
    sl_nsn = createSlice(len(data.shape), targetIndexDict = {idim : index_nsn})

    res = data.copy()

    if var in ('O3', 'O3_MDA8'):
        res[sl_nso] = res[sl_nso] * 22.4 / 48
        res[sl_nsn] = res[sl_nsn] * 24.5 / 48
    elif var == 'PM25':
        pass
    elif var == 'SO2':
        res[sl_nso] = res[sl_nso] * 22.4 / 64
        res[sl_nsn] = res[sl_nsn] * 24.5 / 64
    elif var == 'NO2':
        res[sl_nso] = res[sl_nso] * 22.4 / 46
        res[sl_nsn] = res[sl_nsn] * 24.5 / 46
    else:
        print("functin <MEEugm3_to_ppbv> : unknown var {}, plz update the code!".format(var))
        sys.exit(1)


    return res