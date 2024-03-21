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


#@ func::path2wsl
def path2wsl(path: str, require_existed: bool = False):
    from ._o_globalstate import logger

    # print(logger)
    # print(id(logger))

    if re.match(r'/mnt/[a-z]', path):
        if require_existed:
            if platform.system() == "Linux":
                if not os.path.exists(path):
                    logger.error(f"require_existed=True, but target path doesn't exist! {path}")
                    raise RuntimeError
            else:
                path_win = path2win(path)
                if not os.path.exists(path_win):
                    logger.error(f"require_existed=True, but target path doesn't exist! {path_win}")
                    raise RuntimeError
        return path

    if not re.match(r'[C-N]:\\', path):
        logger.error(f"The arg:path is neither a win path, nor a wsl path: {path}")
        raise RuntimeError

    strT = path[3:].replace('\\', '/')
    path_wsl = f"/mnt/{path[0].lower()}/{strT}"

    if require_existed:
        if platform.system() == "Linux":
            if not os.path.exists(path_wsl):
                logger.error(f"require_existed=True, but target path doesn't exist! {path_wsl}")
                raise RuntimeError
        else:
            if not os.path.exists(path):
                logger.error(f"require_existed=True, but target path doesn't exist! {path}")
                raise RuntimeError

    return path_wsl


#@ func::path2win
def path2win(path: str, require_existed: bool = False):
    from ._o_globalstate import logger

    if re.match(r"[A-Z]:\\", path):
        if require_existed:
            if platform.system() == "Linux":
                path_wsl = path2wsl(path)
                if not os.path.exists(path_wsl):
                    logger.error(f"require_existed=True, but target path doesn't exist! {path_wsl}")
                    raise RuntimeError
            else:
                if not os.path.exists(path):
                    logger.error(f"require_existed=True, but target path doesn't exist! {path}")
                    raise RuntimeError
        return path

    if not re.match(r'/mnt/[a-z]/', path):
        logger.error(f"The arg:path is neither a win path, nor a wsl path: {path}")
        raise RuntimeError

    disk = path[5]
    path_win = disk.upper() + ":\\" + path[7:].replace('/', '\\')
    
    if require_existed:
        if platform.system() == "Linux":
            if not os.path.exists(path):
                logger.error(f"require_existed=True, but target path doesn't exist! {path}")
                raise RuntimeError
        else:
            if not os.path.exists(path_win):
                logger.error(f"require_existed=True, but target path doesn't exist! {path_win}")
                raise RuntimeError

    return path_win 


