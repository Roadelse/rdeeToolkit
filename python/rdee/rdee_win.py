# coding=utf-8


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


def path_win2wsl(path_win):
    strT = path_win[3:].replace('\\', '/')
    path_wsl = f"/mnt/{path_win[0].lower()}/{strT}"
    return path_wsl

def path_wsl2win(path_wsl):
    disk = path_wsl[5]
    path_win = disk.upper() + ":\\" + path_wsl[7:].replace('/', '\\')
    return path_win 


