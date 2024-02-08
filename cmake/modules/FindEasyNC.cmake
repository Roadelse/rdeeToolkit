# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pre-settings
if (DEFINED FIND_EASYNC_LOADED)
    return()
endif()
set(FIND_EASYNC_LOADED TRUE)

include(rdee.checksys)
include(rdee.colorful)
find_package(rdee_fortran)
find_package(netcdff)

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
    EasyNC_lib
    NAMES libEasyNC.a
    HINTS 
        $ENV{EASYNC}/lib $ENV{easync}/lib $ENV{EasyNC}/lib
        ${EASYNC}/lib ${easync}/lib ${EasyNC}/lib
        $ENV{zjxGit}/EasyNC/cbuild${build_suffix}/lib 
        $ENV{zjxHome}/recRoot/GitRepos/EasyNC/cbuild${build_suffix}/lib 
        /mnt/d/recRoot/GitRepos/EasyNC/cbuild${build_suffix}/lib 
        ~/recRoot/GitRepos/EasyNC/cbuild${build_suffix}/lib 
        ~/zjx/recRoot/GitRepos/EasyNC/cbuild${build_suffix}/lib
)

if (NOT EasyNC_lib)
    message(FATAL_ERROR "cannot find EasyNC!")
endif()
message(STATUS "§ ${Cyan}(find EasyNC)${ColorReset} ${BoldMagenta} libEasyNC.a ${ColorReset} detected in ${EasyNC_lib}")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> add library for rdee_fortran
add_library(EasyNC INTERFACE IMPORTED)
set_target_properties(EasyNC PROPERTIES
    IMPORTED_LIBNAME EasyNC)
target_link_libraries(EasyNC INTERFACE rdee_fortran netcdff)
target_link_directories(EasyNC INTERFACE ${EasyNC_lib})
target_include_directories(EasyNC INTERFACE ${EasyNC_lib}/../include)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> post processing
unset(EasyNC_lib)
unset(build_suffix)
message(VERBOSE "§ ${Cyan}(find EasyNC)${ColorReset} ${Yellow} Please add try_compile and try_run cases for this module in the future.${ColorReset}")
