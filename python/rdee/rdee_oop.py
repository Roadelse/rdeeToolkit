# coding=utf-8


#**********************************************************************
# this function is simaliar with hasattr, getattr, setattr series
#**********************************************************************
def moveattr(obj, attr_old, attr_new):
    if hasattr(obj, attr_old):
        setattr(obj, attr_new, getattr(obj, attr_old))
        delattr(obj, attr_old)
