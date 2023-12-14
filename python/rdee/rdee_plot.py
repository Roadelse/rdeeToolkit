# coding=utf-8


#**********************************************************************
# This function is used to trim png figures
# ImageMagick must be installed!
#**********************************************************************
def trimPic(pic):
    import os
    import platform

    if platform.system() == 'Windows':
        os.system("magick convert -trim " + pic + " " + pic)
    else:
        os.system("convert -trim " + pic + " " + pic)