
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pre-settings
if (DEFINED FIND_RDEE_FORTRAN_LOADED)
    return()
endif()
set(FIND_RDEE_FORTRAN_LOADED TRUE)

include(rdee.checksys)
include(rdee.colorful)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ get build_suffix
if (inSW)
    set(build_suffix ".sw")
elseif (${CMAKE_Fortran_COMPILER_ID} STREQUAL "Intel")
    set(build_suffix ".intel")
elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL "GNU")
    set(build_suffix ".gnu")
else()
    message(FATAL_ERROR "Error! Unknown fortran copmiler id : ${CMAKE_Fortran_COMPILER_ID}")
endif()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> find paths
find_path(
    rdee_fortran_lib
    NAMES librdee_fortran.a
    HINTS 
        $ENV{RDEE_FORTRAN}/lib $ENV{rdee_fortran}/lib
        ${RDEE_FORTRAN}/lib ${rdee_fortran}/lib
        $ENV{zjxGit}/rdee_fortran/cbuild${build_suffix}/lib
        $ENV{zjxHome}/recRoot/GitRepos/rdee_fortran/cbuild${build_suffix}/lib
        /mnt/d/recRoot/GitRepos/rdee_fortran/cbuild${build_suffix}/lib
        ~/recRoot/GitRepos/rdee_fortran/cbuild${build_suffix}/lib
        ~/zjx/recRoot/GitRepos/rdee_fortran/cbuild${build_suffix}/lib
)

if (NOT rdee_fortran_lib)
    message(FATAL_ERROR "Error! Cannot find rdee_fortran!")
endif()
message(STATUS "§ ${Cyan}(find rdee_fortran)${ColorReset} ${BoldMagenta} librdee_fortran.a ${ColorReset} detected in ${rdee_fortran_lib}")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> add library for rdee_fortran
add_library(rdee_fortran INTERFACE IMPORTED)
set_target_properties(rdee_fortran PROPERTIES
    IMPORTED_LIBNAME rdee_fortran)
target_link_directories(rdee_fortran INTERFACE ${rdee_fortran_lib})
target_include_directories(rdee_fortran INTERFACE ${rdee_fortran_lib}/../include)


# add_library(rdee_fortran STATIC IMPORTED)
# set_target_properties(rdee_fortran PROPERTIES
#     IMPORTED_LOCATION ${rdee_fortran_lib}/librdee_fortran.a
#     )




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> post processing
unset(rdee_fortran_lib)
unset(build_suffix)

message(VERBOSE "§ ${Cyan}(find rdee_fortran)${ColorReset} ${Yellow} Please add try_compile and try_run cases for this module in the future.${ColorReset}")
