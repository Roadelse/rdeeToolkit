
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> core logic
set(PROJECT_CMAKE_DIR ${CMAKE_CURRENT_LIST_DIR})
list(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/modules)
list(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/scripts)

execute_process(
    COMMAND bash -c "chmod +x ${PROJECT_CMAKE_DIR}/scripts/*"
)

include(rdee.checksys)
include(rdee.colorful)



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> custom functions for specific projects
