
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pre-settings
if (DEFINED CHECK_SYS_LOADED)
    return()
endif()
set(CHECK_SYS_LOADED TRUE)

include(rdee.colorful)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test inWSL
if(EXISTS /proc/sys/fs/binfmt_misc/WSLInterop)
    message(STATUS "§ ${Cyan}(rdee.checksys)${ColorReset} ${BoldMagenta} WSL ${ColorReset} detected!")
    set(inWSL TRUE)
else()
    set(inWSL FALSE)
endif()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test inSW
set(inSW FALSE)
# message(STATUS "11${CMAKE_Fortran_COMPILER_ID}")
if ("$ENV{inSW}" OR Sunway)
    set(inSW TRUE)
endif()

if (NOT inSW AND DEFINED CMAKE_Fortran_COMPILER_ID AND "${CMAKE_Fortran_COMPILER_ID}" STREQUAL "GNU")
    execute_process(COMMAND bash -c "${CMAKE_Fortran_COMPILER} -v |& grep -Po '(?<=COLLECT_GCC=).*'"
        OUTPUT_VARIABLE COLLECT_GCC)
    string(STRIP ${COLLECT_GCC} COLLECT_GCC)
    get_filename_component(BFC ${COLLECT_GCC} NAME)
    if (${BFC} STREQUAL "swgfortran")
        # message(STATUS "COLLECT_GCC = ${BFC}")
        set(inSW TRUE)
        unset(BFC)
        unset(COLLECT_GCC)
    endif()
endif()
if (NOT inSW AND DEFINED CMAKE_C_COMPILER_ID AND "${CMAKE_C_COMPILER_ID}" STREQUAL "GNU")
    execute_process(COMMAND bash -c "${CMAKE_C_COMPILER} -v |& grep -Po '(?<=COLLECT_GCC=).*'"
        OUTPUT_VARIABLE COLLECT_GCC)
    string(STRIP ${COLLECT_GCC} COLLECT_GCC)
    get_filename_component(BCC ${COLLECT_GCC} NAME)
    if (${BCC} STREQUAL "swgcc")
        # message(STATUS "COLLECT_GCC = ${BCC}")
        set(inSW TRUE)
        unset(BCC)
        unset(COLLECT_GCC)
    endif()
endif()

if (inSW)
    message(STATUS "§ ${Cyan}(rdee.checksys)${ColorReset} ${BoldMagenta} Sunway ${ColorReset} detected!")
endif()


