

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pre-settings
if (DEFINED FIND_NETCDFF_LOADED)
    return()
endif()
set(FIND_NETCDFF_LOADED TRUE)

include(rdee.colorful)
find_package(netcdf)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> find libnetcdff.a and netcdf.mod
find_path(
    netcdff_lib
    NAMES libnetcdff.a
    HINTS 
        $ENV{NETCDFF}/lib
        $ENV{NETCDF}/lib
        /usr/lib/x86_64-linux-gnu /usr/lib
)
find_path(
    netcdff_include
    NAMES netcdf.mod
    HINTS 
        $ENV{NETCDFF}/include
        $ENV{NETCDF}/include
        /usr/include
)


if (NOT (netcdff_lib AND netcdff_include))
    message(FATAL_ERROR "Error! Cannot find netcdf-fortran, please set the environment : NETCDFF or define NETCDFF when executing cmake")
endif()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> add library of NETCDFF
message(STATUS "§ ${Cyan}(find netcdff)${ColorReset} ${BoldMagenta} NETCDF-Fortran ${ColorReset} detected in ${netcdff_lib}/")

add_library(netcdff INTERFACE IMPORTED)
set_target_properties(netcdff PROPERTIES
    IMPORTED_LIBNAME netcdff)
target_link_libraries(netcdff INTERFACE netcdf)
target_link_directories(netcdff INTERFACE ${netcdff_lib})
target_include_directories(netcdff INTERFACE ${netcdff_include})


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> post-processing
unset(netcdff_lib)
unset(netcdff_include)

message(VERBOSE "§ ${Cyan}(find NETCDFF)${ColorReset} ${Yellow} Please add try_compile and try_run cases for this module in the future.${ColorReset}")