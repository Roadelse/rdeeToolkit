# coding=utf-8

import re
import os.path
import platform

#**********************************************************************
# this function is used to create shortcut
#**********************************************************************
def createShortCut(filename2, lnkname, debug = False):
    # filename2 : should be abspath, or there will be some strange errors
    # from https://www.cnblogs.com/luoheng23/p/11342479.html

    import platform
    assert platform.system() == 'Windows', 'function <createShortCut> : this function could only be run in Windows system! Now in {}'.format(platform.system())

    import os
    import win32com.client as client

    shell = client.Dispatch("WScript.Shell")

    filename = os.path.abspath(filename2)

    if debug : 
        print("filename = {}".format(filename))
        print("link name = {}".format(lnkname))
    
    shortcut = shell.CreateShortCut(lnkname)
    shortcut.TargetPath = filename
    shortcut.save()


#**********************************************************************
# this function is used to get shortcut target path
#**********************************************************************
def GetShortCut(shortcut):
    # from https://www.cnblogs.com/luoheng23/p/11342479.html

    import platform
    assert platform.system() == 'Windows', 'function <createShortCut> : this function could only be run in Windows system! Now in {}'.format(platform.system())

    import win32com.client as client

    shell = client.Dispatch("WScript.Shell")

    return shell.CreateShortCut(shortcut).Targetpath


#@ func::path_win2wsl
def path_win2wsl(path_win):
    strT = path_win[3:].replace('\\', '/')
    path_wsl = f"/mnt/{path_win[0].lower()}/{strT}"
    return path_wsl


#@ func::path_wsl2win
def path_wsl2win(path_wsl: str, require_existed: bool = False):
    from ._x_logging import logger

    if not re.match(r'/mnt/[a-z]/', path_wsl):
        logger.error(f"The arg:path_wsl is not a wsl path for windows: {path_wsl}")
        raise RuntimeError
    

    disk = path_wsl[5]
    path_win = disk.upper() + ":\\" + path_wsl[7:].replace('/', '\\')
    
    if require_existed:
        if platform.system() == "Linux":
            if not os.path.exists(path_wsl):
                logger.error(f"require_existed=True, but target path doesn't exist! {path_wsl}")
                raise RuntimeError
        else:
            if not os.path.exists(path_win):
                logger.error(f"require_existed=True, but target path doesn't exist! {path_win}")
                raise RuntimeError

    return path_win 


