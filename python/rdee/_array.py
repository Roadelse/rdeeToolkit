# coding=utf-8




#**********************************************************************
# this function is used to create slice according to spepcified index 
# for some dimensions
#**********************************************************************
def createSlice(ndims, targetSliceDict: dict = None, targetIndexDict: dict = None):
    # ndims : int, the number of total dimensions
    # targetSliceDict : slice parameters for specified dimension, such as {3 : [1, 3]}, {3 : [3]} (keep dimension), {1 : 0} (reduce dimension)
    # targetIndexDict : indexe for specified dimension, such as {3 : [2,4,6,8,10,12]}

    # ref - https://stackoverflow.com/questions/24398708/slicing-a-numpy-array-along-a-dynamically-specified-axis
    # https://stackoverflow.com/questions/31094641/dynamic-axis-indexing-of-numpy-ndarray

    sls = [slice(None)] * ndims
    if targetSliceDict is not None:
        for k in targetSliceDict.keys():
            sls[k] = slice(*targetSliceDict[k])

    if targetIndexDict is not None:
        for k in targetIndexDict:
            sls[k] = targetIndexDict[k]

    return tuple(sls)



#**********************************************************************
# this function is used to get unique values for 1d array without sort
#**********************************************************************
def get_unique_values_1d_stable(data):
    import numpy as np

    data_np = np.array(data)
    assert len(data_np.shape) == 1, 'function <get_unique_values_1d_stable> : param-data should be a 1-d array!'

    u, ind = np.unique(data_np, return_index = True)

    res = u[np.argsort(ind)]

    return res




#**********************************************************************
# this function is a "map" of function np.argwhere
#**********************************************************************
def ind_eq_map(arrP, arrC, **kwargs):
    import numpy as np
    import sys

    allowMissing = False
    allowRepeat = False
    autoSort = True
    if 'allowMissing' in kwargs:
        allowMissing = kwargs['allowMissing']
    if 'allowRepeat' in kwargs:
        allowRepeat = kwargs['allowRepeat']
    if 'autoSort' in kwargs:
        autoSort = kwargs['autoSort']

    arrP_np = np.array(arrP)


    res = []
    for e in arrC:
        poss = np.argwhere(arrP_np == e).reshape(-1)
        if poss.size == 0:
            if not allowMissing:
                print(f"Error in function<ind_eq_map> cannot find value {e}!")
                sys.exit(1)
        elif poss.size > 1:
            if allowRepeat:
                res.extend(poss)  # it's ok for a list extending an nd-array
            else:
                print(f"Error in function<ind_eq_map> : value {e} repeats! set allowRepeat if it is ok!")
                sys.exit(1)
        else:
            res.extend(poss)

    if autoSort:
        res.sort()

    return res


#**********************************************************************
# this function is used to get indexes for intersection from 2 arrays
#**********************************************************************
def getIntersectInd(arr1, arr2):
    import numpy as np
    arrI = np.intersect1d(arr1, arr2)
    return ind_eq_map(arr1, arrI, allowMissing = True), ind_eq_map(arr2, arrI, allowMissing = True)


#**********************************************************************
# This function is used to convert nd-array to 1d-array and remove 
# nan values
#**********************************************************************
def get1dR(nda) : # nd-array
    import numpy as np
    nda_1d = nda.reshape(-1)
    nda_1dR = nda_1d[~np.isnan(nda_1d)]

    return nda_1dR

#**********************************************************************
# This function is used to convert edge value to center value for bins
#**********************************************************************
def E2C(arr): 
    # arr : 1d array, representing edges for each bin
    import numpy as np
    res = np.empty(len(arr) - 1)
    for i in range(res.size) :
        res[i] = (arr[i] + arr[i + 1] ) / 2

    return res


#**********************************************************************
# This function is used to sync two arrays which own Nan values in 
# different positions
#**********************************************************************
def sync_array(arr1, arr2, opt = {}):
    # arr1, arr2 : two arrays need to be synchronized
    # opt : not used by now

    import numpy as np
    import sys

    type1 = type(arr1)
    type2 = type(arr2)
    assert type1 == type2, 'arr1 and arr2 must have the same type!'

    if type1 == np.ndarray :
        # print("synchronizing numpy.ndarray")
        index1 = np.argwhere(~np.isnan(arr1)).reshape(-1)
        index2 = np.argwhere(~np.isnan(arr2)).reshape(-1)
        indexU = np.intersect1d(index1, index2)
        return arr1[indexU], arr2[indexU]
    else:
        print("type {} is not supported by now! plz add the code!".format(type1))
        sys.exit(1)


#**********************************************************************
# This function is used to sync 4 arrays which own Nan values in 
# different positions
#**********************************************************************
def sync_4array(arr1, arr2, arr3, arr4, opt = {}):
    # arr1, arr2 : two arrays need to be synchronized
    # opt : not used by now

    import numpy as np
    import sys

    type1 = type(arr1)
    type2 = type(arr2)
    type3 = type(arr3)
    type4 = type(arr4)
    assert type1 == type2 and type1 == type3 and type1 == type4, 'arr1234 must have the same type!'

    if type1 == np.ndarray :
        # print("synchronizing numpy.ndarray")
        index1 = np.argwhere(~np.isnan(arr1)).reshape(-1)
        index2 = np.argwhere(~np.isnan(arr2)).reshape(-1)
        index3 = np.argwhere(~np.isnan(arr3)).reshape(-1)
        index4 = np.argwhere(~np.isnan(arr4)).reshape(-1)
        indexU = np.intersect1d(np.intersect1d(index1, index2), np.intersect1d(index3, index4))
        return arr1[indexU], arr2[indexU], arr3[indexU], arr4[indexU]
    else:
        print("type {} is not supported by now! plz add the code!".format(type1))
        sys.exit(1)



#**********************************************************************
# This function is used to sync 6 arrays which own Nan values in 
# different positions
#**********************************************************************
def sync_6array(arr1, arr2, arr3, arr4, arr5, arr6, opt = {}):
    # arr1, arr2 : two arrays need to be synchronized
    # opt : not used by now

    import numpy as np
    import sys

    type1 = type(arr1)
    type2 = type(arr2)
    type3 = type(arr3)
    type4 = type(arr4)
    type5 = type(arr5)
    type6 = type(arr6)
    assert type1 == type2 and type1 == type3 and type1 == type4 and type1 == type5 and type1 == type6, 'arr123456 must have the same type!'

    if type1 == np.ndarray :
        # print("synchronizing numpy.ndarray")
        index1 = np.argwhere(~np.isnan(arr1)).reshape(-1)
        index2 = np.argwhere(~np.isnan(arr2)).reshape(-1)
        index3 = np.argwhere(~np.isnan(arr3)).reshape(-1)
        index4 = np.argwhere(~np.isnan(arr4)).reshape(-1)
        index5 = np.argwhere(~np.isnan(arr5)).reshape(-1)
        index6 = np.argwhere(~np.isnan(arr6)).reshape(-1)
        indexU = np.intersect1d(np.intersect1d(np.intersect1d(index1, index2), np.intersect1d(index3, index4)), np.intersect1d(index5, index6))
        return arr1[indexU], arr2[indexU], arr3[indexU], arr4[indexU], arr5[indexU], arr6[indexU]
    else:
        print("type {} is not supported by now! plz add the code!".format(type1))
        sys.exit(1)

#**********************************************************************
# This function is used to get first unconsistent values for each 
# element
# for example : 
#       1,1,2,3,1,1,1,3,3,3,2
#       x   x x x     x     x   (x means the target positions)
#**********************************************************************
def get_start_pos_for_continuous_values(series):
    res = []
    for i, s in enumerate(series):
        if not res or s != series[res[-1]]:
            res.append(i)
    return res


#**********************************************************************
# This function is similar with get_start_pos_for_continuous_values, 
# except for the processing method of the last element 
# This function use a pseudo position at the last for convenience 
#**********************************************************************
def get_start_pos_for_continuous_values2(series):
    res = []
    for i, s in enumerate(series):
        if not res or s != series[res[-1]]:
            res.append(i)
    res.append(len(series))
    return res


#**********************************************************************
# This function is used to calculate average according to labels
#**********************************************************************
def dim_avg_label_n(data, label, n):
    import numpy as np
    import warnings
    # warnings.simplefilter("ignore")

    assert n == 0, 'only support n == 0 by now! plz add code'
    sps = get_start_pos_for_continuous_values2(label)
    newShape = [len(sps) - 1] + list(data.shape[1:])
    res = np.zeros(newShape)
    res[:] = np.nan
    for i in range(newShape[0]):
        if len(newShape) > 1:
            res[i, :] = np.nanmean(data[sps[i] : sps[i+1], :], n)
        else:
            res[i] = np.nanmean(data[sps[i] : sps[i+1]], n)
    return res


def xxx(data, method):
    import numpy as np
    # data_np = np.array(data)
    if method == "avg":
        return np.nanmean(data)
    elif method == 'sum':
        return np.nansum(data)
    elif method == 'max':
        return np.nanmax(data)
    elif method == 'min':
        return np.nanmin(data)
    else:
        print("unknown method : {}".format(method))
        sys.exit(1)
    



#**********************************************************************
# This function is an abstract function from np.nanmena, np.nanmax, 
# np.nanmin, and all functions owning shape of dim_xxx_n
#**********************************************************************
def dim_xxx_n(data, idim, method):
    import numpy as np
    import sys
    # import warnings
    # warnings.simplefilter("ignore")

    assert type(data) == np.ndarray, '{}'.format(type(data))
    if method == 'avg':
        res = np.nan if np.all(np.isnan(data)) else np.nanmean(data, idim)
    elif method == 'max':
        res = np.nan if np.all(np.isnan(data)) else np.nanmax(data, idim)
    elif method == 'min':
        res = np.nan if np.all(np.isnan(data)) else np.nanmin(data, idim)
    elif method == 'sum':
        res = np.nan if np.all(np.isnan(data)) else np.nansum(data, idim) # In NumPy versions <= 1.9.0 Nan is returned for slices that are all-NaN or empty. In later versions zero is returned.  
    else:
        print("unknwon method : {}".format(method))
        sys.exit(1) 

    return res


#**********************************************************************
# This function is used to calculate avg/sum/max/min/... according to 
# labels
#**********************************************************************
def dim_xxx_label_n(data, labels, idim, method):
    import numpy as np
    import warnings
    import sys
    # warnings.simplefilter("ignore")

    sps2 = get_start_pos_for_continuous_values2(labels)
    oriShape = list(data.shape)
    newShape = oriShape.copy()
    newShape[idim] = len(sps2) - 1
    ndims = len(newShape)

    labelsU = get_unique_values_1d_stable(labels)

    res = np.zeros(newShape)
    res[:] = np.nan
    for i in range(newShape[idim]):
        if ndims == 1 and idim == 0:
            res[i] = dim_xxx_n(data[sps2[i] : sps2[i + 1]], idim, method)
        elif ndims > 1 and idim == 0:
            res[i, :] = dim_xxx_n(data[sps2[i] : sps2[i + 1], :], idim, method)
        elif ndims == 2 and idim == 1:
            res[:, i] = dim_xxx_n(data[:, sps2[i] : sps2[i + 1]], idim, method)
        else:
            print("function <dim_xxx_label_n> : unknown ndims = {} and idim = {}, plz add code".format(ndims, idim))
            sys.exit(1)


    return {'data' : res, 'labels' : labelsU}




#**********************************************************************
# This function is used to calculate avg/sum/max/min/... according to 
# labels and categories
#**********************************************************************
def dim_xxx_cate_n(data, labels, cates, idim, method):
    # data : nd array
    # labels : 1d array, size should be equal to size of data $idim dimension
    # cates : 1d array, subset of labels
    # method : avg, sum, max, min
    import numpy as np

    if type(data) != np.ndarray:
        data_np = np.array(data)
    else:
        data_np = data

    oldShape = list(data_np.shape)
    assert oldShape[idim] == len(labels), 'function <dim_xxx_cate_n> : length of labels must be the same as length of data idim dimension!'


    newShape = oldShape.copy()
    newShape[idim] = len(cates)

    res = np.empty(newShape, dtype = data_np.dtype)
    # print(res.dtype)

    labels_np = np.array(labels)

    for i, c in enumerate(cates):
        slT_res = createSlice(len(newShape), targetIndexDict = {idim : i})
        slT_data = createSlice(len(oldShape), targetIndexDict = {idim : np.argwhere(labels_np == c).reshape(-1).tolist()})
        # print(dim_xxx_n(data[slT_data], idim, method))
        # print(slT_data)
        res[slT_res] = dim_xxx_n(data_np[slT_data], idim, method)

    return res


def xxx_inte(data, values, intervals, method):
    import numpy as np
    assert type(data) == np.ndarray, "Error, plz use numpy.ndarray!"

    assert data.shape == values.shape, "Error, data and values must own the same shape!"

    res = np.zeros(len(intervals))
    res[:] = np.nan
    count = np.zeros(len(intervals), dtype = np.int32)

    for i, inte in enumerate(intervals):
        if type(inte[0]) == list or type(inte[0]) == tuple:
            holder = np.array([])
            for inte2 in inte:
                minV, maxV = inte2
                tarIndex = np.argwhere(np.logical_and(values >= minV, values < maxV)).reshape(-1)
                if tarIndex.size == 0:
                    continue
                else:
                    count[i] += tarIndex.size
                    holder = np.append(holder, data[tarIndex])
            res[i] = xxx(holder, method)
                    

        else:
            minV, maxV = inte
            tarIndex = np.argwhere(np.logical_and(values >= minV, values < maxV)).reshape(-1)
            if tarIndex.size == 0:
                continue
            else:
                count[i] = tarIndex.size
                res[i] = xxx(data[tarIndex], method)

    return {method : res, 'count' : count}

#**********************************************************************
# Convert definition of a series of integer into an array
# supporting "to" and "sep" sign
#**********************************************************************
def splitIntsDef_singleTS(idef, to, sep):
# to : from A to B, usually "-", such as 2015-2020, 1-9
# sep : seperator, usually ",", such as "1,3,5,7"
# ===========
# only support one to and sep char, if need multiple, use 'splitInitsDef'
    sections = idef.split(sep)
    rst = []
    for s in sections:
        if to in s:
            spair = s.split(to)
            rst.extend(list(range(int(spair[0]), int(spair[1]) + 1)))
        else:
            rst.append(s)

    return rst


#**********************************************************************
# Convert definition of a series of integer into an array
# supporting "to" and "sep" sign
#**********************************************************************
def splitAsciiDef_singleTS(adef, to, sep):
    # to : from A to B, usually "-", such as 2015-2020, 1-9
    # sep : seperator, usually ",", such as "1,3,5,7"
    # ===========
    # only support one to and sep char, if need multiple, use 'splitInitsDef'
    sections = adef.split(sep)
    rst = []
    for s in sections:
        if to in s:
            spair = s.split(to)
            assert len(spair[0]) == 1 and len(spair[1]) == 1
            asciiS = ord(spair[0])
            asciiE = ord(spair[1])
            assert asciiE > asciiS
            rst.extend([chr(i) for i in range(asciiS, asciiE + 1)])
            # rst.extend(list(range(int(spair[0]), int(spair[1]) + 1)))
        else:
            rst.append(s)

    return rst



#**********************************************************************
# Convert definition of a series of integer into an array
# supporting "to" and "sep" sign
#**********************************************************************
def splitIntsDef(idef, to, sep):
    if isinstance(to, str):
        to_arr = [c for c in to]
    else:
        to_arr = to
    if isinstance(sep, str):
        sep_arr = [c for c in sep]
    else:
        sep_arr = sep
    assert isinstance(idef, str)

    assert len(set(to_arr)) == len(to_arr)
    assert len(set(sep_arr)) == len(sep_arr)
    assert len(set(to_arr)) + len(set(sep_arr)) == len(set(to_arr) | set(sep_arr))

    s1 = 0
    i = 0
    rst = []
    p_sep = -1
    p_to = -1
    while i <= len(idef):
        if i == len(idef) or idef[i] in sep_arr: # order matters
            if p_to == -1 :
                rst.append(int(idef[p_sep + 1 : i]))
            else:
                is_pair = idef[p_sep + 1 : i].split(idef[p_to])
                ip1 = int(is_pair[0])
                ip2 = int(is_pair[1])
                if ip2 >= ip1:
                    rst.extend(list(range(ip1, ip2 + 1)))
                else:
                    rst.extend(list(range(ip1, ip2 - 1, -1)))
            p_to = -1
            p_sep = i
        elif idef[i] in to_arr:
            assert p_to == -1, "Error! continous sep"
            p_to = i
        i += 1

    return rst


#**********************************************************************
# Concatenate string arrays by element
#**********************************************************************
def concat_strA_ew(sep, *args): 
    assert isinstance(sep, str), 'Error in func::concat_str, wrong type for sep, must be str!'
    
    Lens = [len(x) for x in args]
    assert len(set(Lens)) == 1, 'Error in func::concat_str, more than one length!'
    L = Lens[0]
    
    rst = []
    for i in range(L):
        rst.append(sep.join([str(x[i]) for x in args]))
    
    return rst




#**********************************************************************
# split array
#**********************************************************************
def asplit(n_or_array, segments, random=False):
    import numpy as np
    if isinstance(n_or_array, int):
        _array = np.array(range(n_or_array))
    else:
        _array = np.array(n_or_array)
    
    if random:
        np.random.shuffle(_array)
    
    assert isinstance(segments, (list, tuple))
    if max(segments) < 2:  # do not use <= 1, in avoidance of floating implicit
        assert np.isclose(np.sum(segments), 1), f'Error! sum should be close to 1, now is {sum(segments)}'
        _lengths = [round(len(_array)*r) for r in segments]
        _lengths[-1] = _lengths[-1] + len(_array) - sum(_lengths)
    else:
        assert sum(segments) == len(_array)
        _lengths = segments
    
    indexx = list(range(len(_array)))  # index's index

    ret = []
    i = 0
    for L in _lengths:
        ret.append(_array[indexx[i : i+L]].tolist())
        i += L

    return ret
    