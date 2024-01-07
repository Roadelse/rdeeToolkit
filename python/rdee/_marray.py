# coding=utf-8

# this script contains functions which are set for customized masked array
# we use "very big values" as the fill value

# rma : roadelse masked array


# pause @2021-07-17 02:39:06


def rma_getDefaultFillValue(dtype):
    import numpy as np
    import sys

    typeA = dtype.type
    if typeA == np.float32 or typeA == np.float64:
        fillvalue = -9.96e36
    elif typeA == np.int:
        fillvalue = -2e9
    elif typeA == np.int64:
        fillvalue = -2
    elif typeA == np.str_ or typeA == np.string_:
        fillvalue = "missing_value"
    else:
        print("function <getDefaultFillValue> : unknown typeA = {} and dtype = {}".format(typeA, dtype))
        sys.exit(1)

    return fillvalue


def rma_nma2rma(ma):
    # numpy masked array to customized masked array (pseudo)
    import numpy as np
    assert type(ma) == np.ma.core.MaskedArray, 'function <nma2rma> : param-ma must be numpy.ma.core.MaskedArray! now is {}'.format(type(ma))
    import os

    fillvalue = rma_getDefaultFillValue(ma.dtype)

    res = ma.filled(fillvalue)

    return res