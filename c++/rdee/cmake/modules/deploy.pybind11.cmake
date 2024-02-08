#@ <prepare>

if (DEPLOY_PYBIND11_LOADED)
	return()
endif()
set(DEPLOY_PYBIND11_LOADED TRUE)

include(rdee.colorful)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

execute_process(
    COMMAND ${Python3_EXECUTABLE} -c "import pybind11"
    RESULT_VARIABLE EXIT_CODE
)

if (NOT EXIT_CODE EQUAL 0)
    if (DEFINED INSTALL_PYTHON_LIB)
        execute_process(
            COMMAND pip "install pybind11 -i https://pypi.tuna.tsinghua.edu.cn/simple"
            RESULT_VARIABLE PIP_INSTALL_STATUS
        )
        if (NOT PIP_INSTALL_STATUS EQUAL 0)
            message(FATAL_ERROR "Error, cannot find ${libname} in python!")
        endif()
    else()
        message(FATAL_ERROR "Error, cannot find ${libname} in python!")
    endif()
endif()

if (NOT DEFINED PYBIND11_DEPLOY_DIR)
    set(PYBIND11_DEPLOY_DIR ${CMAKE_CURRENT_LIST_DIR})
endif()

if (EXISTS ${PYBIND11_DEPLOY_DIR}/pybind11)
    message(STATUS "§ ${Cyan}(deploy.pybind11)${ColorReset} skip, pybind11 already existed: ${PYBIND11_DEPLOY_DIR}")
    return()
endif()


message(STATUS "§ ${Cyan}(deploy.pybind11)${ColorReset} Try to locate include-dir and cmake-dir from python pybind11 module")
execute_process(
    COMMAND ${Python3_EXECUTABLE} -m "pybind11 --cmakedir"
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
)
execute_process(
    COMMAND pwsh -Command '"-I/home/roadelse/Software/idep/miniconda3/include/python3.11 -I/home/roadelse/Software/idep/miniconda3/lib/python3.11/site-packages/pybind11/include".Replace("-I", "").Split(" ") | where {$_ -match "pybind11/include$"}'
    OUTPUT_VARIABLE PYBIND11_INCLUDE_DIR
)
if (NOT DEFINED PYBIND11_INCLUDE_DIR)
    message(FATAL_ERROR "No include dir")
endif()


execute_process(
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${PYBIND11_INCLUDE_DIR} ${PYBIND11_DEPLOY_DIR}/include
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${PYBIND11_CMAKE_DIR} ${PYBIND11_DEPLOY_DIR}/cmake
)

set(pybind11_DIR ${PYBIND11_DEPLOY_DIR}/cmake)

find_package(pybind11 REQUIRED)

include_directories(${PYBIND11_DEPLOY_DIR}/include)


# Below is an alternative method which downloads pybind11 from github, but, in fact unnecessary.
# find_path(PYBIND11_INCLUDE_DIR "pybind11.h" PATHS ${CMAKE_SOURCE_DIR}/thirdparty/pybind11/include/pybind11)
# file(GLOB_RECURSE PYBIND11_HEADERS "${CMAKE_SOURCE_DIR}/**/pybind11.h")
# list(LENGTH PYBIND11_HEADERS PYBIND11_HEADERS_COUNT)


# message("${PYBIND11_INCLUDE_DIR}")
# message("${CMAKE_SOURCE_DIR}")

# if (NOT PYBIND11_HEADERS_COUNT EQUAL 0)
#     if (PYBIND11_HEADERS_COUNT GREATER 1)
#         message(WARNING "§ Multiple pybind11.h headers found, using the first one.")
#     endif()

#     list(GET PYBIND11_HEADERS 0 PYBIND11_HEADER)
#     get_filename_component(PYBIND11_INCLUDE_DIR ${PYBIND11_HEADER} DIRECTORY)
#     message("§ Found pybind11.h in: ${PYBIND11_INCLUDE_DIR}")
#     set(pybind11_DIR $PYBIND11_INCLUDE_DIR/..)  # usualy include "pybind11/pybind11.h"
# else()
#     # message(FATAL_ERROR "Cannot find pybind11.h!")
#     message(STATUS "Cannot find pybind11.h, cloning it from Github: https://github.com/pybind/pybind11.git")

#     if (NOT DEFINED PYBIND11_CLONE_DIR)
#         set(PYBIND11_CLONE_DIR ${CMAKE_CURRENT_LIST_DIR})
#     endif()
#     execute_process(
#         COMMAND git clone --depth 1 https://github.com/pybind/pybind11.git ${CMAKE_SOURCE_DIR}/thirdparty/pybind11
#         RESULT_VARIABLE GIT_CLONE_RESULT
#     )
#     if(NOT GIT_CLONE_RESULT EQUAL 0)
#         message(FATAL_ERROR "Git clone failed with ${GIT_CLONE_RESULT} for pybind11,please check your git setup or network connection.")
#     endif()
# endif()



