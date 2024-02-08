
include(rdee.colorful)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

macro(check_python_lib libname)
    execute_process(
        COMMAND ${Python3_EXECUTABLE} -c "import ${libname}"
        RESULT_VARIABLE EXIT_CODE
    )
    if (EXIT_CODE EQUAL 0)
        message(STATUS "§ ${Cyan}(rdee.python)${ColorReset} find ${BoldMagenta} ${libname} ${ColorReset} in python")
    else()
        message(FATAL_ERROR "Error, cannot find ${libname} in python!")
    endif()
endmacro()
