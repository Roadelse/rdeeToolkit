
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pre-settings
if (DEFINED FIND_NETCDF_LOADED)
    return()
endif()
set(FIND_NETCDF_LOADED TRUE)

include(rdee.colorful)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> find libnetcdf.a and netcdf.h
find_path(
    netcdf_lib
    NAMES libnetcdf.a libnetcdf.so
    HINTS $ENV{NETCDF}/lib ${NETCDF}/lib /usr/lib/x86_64-linux-gnu
)
find_path(
    netcdf_include
    NAMES netcdf.h
    HINTS $ENV{NETCDF}/include ${NETCDF}/include /usr/include
)

if (NOT (netcdf_lib AND netcdf_include))
    message(FATAL_ERROR "Error! Cannot find netcdf, please set the environment : NETCDF or define NETCDF when executing cmake")
endif()

message(STATUS "§ ${Cyan}(find netcdf)${ColorReset} ${BoldMagenta} NETCDF ${ColorReset} detected in ${netcdf_lib}/")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> add library of NETCDF
add_library(netcdf INTERFACE IMPORTED)
set_target_properties(netcdf PROPERTIES
    IMPORTED_LIBNAME netcdf)
target_link_directories(netcdf INTERFACE ${netcdf_lib})
target_include_directories(netcdf INTERFACE ${netcdf_include})
if (DEFINED ENV{NETCDF_DEP_INC_DIRS})
    message(STATUS "§ ${Cyan}(find netcdf)${ColorReset} add include directories: $ENV{NETCDF_DEP_INC_DIRS}")
    target_include_directories(netcdf INTERFACE $ENV{NETCDF_DEP_INC_DIRS})
endif()
if (DEFINED ENV{NETCDF_DEP_LINK_DIRS})
    message(STATUS "§ ${Cyan}(find netcdf)${ColorReset} add link directories: $ENV{NETCDF_DEP_LINK_DIRS}")
    target_link_directories(netcdf INTERFACE $ENV{NETCDF_DEP_LINK_DIRS})
endif()
if (DEFINED ENV{NETCDF_DEP_LINK_LIBS})
    message(STATUS "§ ${Cyan}(find netcdf)${ColorReset} add link libraries: $ENV{NETCDF_DEP_LINK_LIBS}")
    target_link_libraries(netcdf INTERFACE $ENV{NETCDF_DEP_LINK_LIBS})
endif()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> post-processing
unset(netcdf_lib)
unset(netcdf_include)

message(VERBOSE "§ ${Cyan}(find netcdf)${ColorReset} ${Yellow} Please add try_compile and try_run cases for this module in the future.${ColorReset}")