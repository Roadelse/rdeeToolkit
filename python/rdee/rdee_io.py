# coding=utf-8


#**********************************************************************
# this function aims to open a text file with several possible encodings
#**********************************************************************
def opens(file, encodings) :
    import sys
    for e in encodings:
        try:
            open(file, encoding=e).read()
            return open(file, encoding=e)
        except:
            pass
    print(f"Error! cannot find valid encoding from {encodings} for {file}")
    sys.exit(1)


#**********************************************************************
# This function aims to create directory if not exists, based on a file path
#**********************************************************************
def ensureFileDirExist(fpath: str):
    """
    param >> fpath : absolute filepath, relative path may be ok as well
    return >> fpath : this funtion will right return the param, make it easy to be embedded into codes
    """
    import os.path as osp
    import os
    os.makedirs(osp.dirname(fpath), exist_ok=True)
    return fpath

def ensureDirExist(dirpath: str):
    """
    param >> fpath : absolute filepath, relative path may be ok as well
    return >> fpath : this funtion will right return the param, make it easy to be embedded into codes
    """
    import os.path as osp
    import os
    os.makedirs(dirpath, exist_ok=True)
    return dirpath


#**********************************************************************
# this function is used to write variable to nc file quickly
# like ncl easy mode
#**********************************************************************
def write_nc_var(ncf, varName, var) :
    import numpy as np

    var_np = np.array(var)

    S = var_np.shape
    ndims = len(S)

    dims_current = list(ncf.dimensions.keys())

    i = 0
    new_dims = [] 
    while len(new_dims) < ndims:
        dimT = 'auto{}'.format(i)
        if dimT in dims_current:
            i += 1
            continue
        new_dims.append(dimT)
        i += 1

    for i, d in enumerate(new_dims):
        ncf.createDimension(d, S[i])

    print("dtype = {}".format(var_np.dtype))
    ncv = ncf.createVariable(varName, var_np.dtype, new_dims)

    # print(var_np.shape)
    ncv[:] = var_np

    return 



#**********************************************************************
# this function is used to log with time
#**********************************************************************
def logT(s, currL = 0, echoL = 0, mpi = False): # from py_rdee
    import time

    if currL < echoL:
        return

    if mpi:
        from mpi4py import MPI
        print("{} - {}, rank = {}".format(time.strftime("%Y/%m/%d %H:%M:%S"), s, MPI.COMM_WORLD.Get_rank()))
    else:
        print("{} - {}".format(time.strftime("%Y/%m/%d %H:%M:%S"), s))



#**********************************************************************
# this function is used to save a dict to csv
#**********************************************************************
def dict2csv(D, oFile, header = None, exist_ok = False):
    assert type(D) == dict, 'function <dict2csv> : Error! param-D must be a dict, now is {}'.format(type(D))
    import os.path
    
    if not exist_ok:
        assert not os.path.exists(oFile), 'function <dict2csv> : Error! oFile {} exists now, remove it or set exist_ok to True'.format(oFile)

    with open(oFile, 'w') as f:
        if header:
            f.write('{}\n'.format(header))
        for k, v in D.items():
            f.write('{},{}\n'.format(k, v))


#**********************************************************************
# This function is used to read data quickly with a flag name from file
# saved by <saveD>
# coupled with <readD>
#**********************************************************************
def readD(name, RM = ''):
    '''
    RM is useless for python verison readD
    '''
    from netCDF4 import Dataset
    import numpy as np

    ncf = Dataset("saveD/" + name + ".nc")
    res = ncf.variables[name][:]
    if type(res) == np.ma.MaskedArray:
        res = res.filled(np.nan)
    return res



#**********************************************************************
# This function is used to read data quickly with a flag name from file
# saved by <saveD>
# coupled with <readD>
#**********************************************************************
def readD_v(fname, vname, RM = '') : 
    from netCDF4 import Dataset
    import numpy as np

    ncf = Dataset("saveD/" + fname + ".nc")
    res = ncf.variables[vname][:]
    if type(res) == np.ma.MaskedArray:
        res = res.filled(np.nan)
    return res
