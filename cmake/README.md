
# Preface

This repo contains all my custom cmake modules

# rdee.cmake

+ key cmake module, should be always include first
+ set necessary CMAKE variables
+ include preliminary modules
+ set authority of files


# modules/

## custom functions

+ `rdee.checksys.cmake` : check system, wsl, Sunway, ...
+ `rdee.colorful.cmake` : set ANSI colorful variables
+ `rdee.python.cmake` : find python and macro for checking python library

## find_package

All these modules below get an `INTERFACE IMPORTED` library target which holds all link and include informations along dependencies. 

+ `FindRdee_fortran.cmake` : find my custom rdee_fortran fortran library
+ `FindEasyNC.cmake` : find my custom EasyNC fortran library
+ `Findnetcdf.cmake` : find netcdf library
+ `Findnetcdff.cmake` : find netcdff library


# scripts/

contains several useful scripts to be executed

+ eval-args.sh : a wrapper to run something, support convenience to run executable at different environment.

# test

several tests to include modules & scripts in this repo

+ basic : only find some packages and do some 
+ demo.rdee_fortran : include findrdee_fortran to build a demo using rdee_fortan
+ demo.EasyNC : include findEasyNC to build a demo using EasyNC