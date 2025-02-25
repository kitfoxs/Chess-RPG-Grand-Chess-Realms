cmake_minimum_required(VERSION 3.12)
project(EasyLinkSDK)

# Enable C++11 standard
set(CMAKE_CXX_STANDARD 11)

# Add pybind11
add_subdirectory(pybind11)

# Include EasyLinkSDK directory
include_directories(EasyLinkSDK/sdk)

# Add the EasyLinkSDK library
add_library(EasyLinkSDK STATIC
    EasyLinkSDK/sdk/EasyLink.cpp
    EasyLinkSDK/sdk/easy_link_c.cpp
)

# Find the hidapi library
find_library(HIDAPI_LIB hidapi)

# Link the hidapi library to the EasyLinkSDK library
target_link_libraries(EasyLinkSDK PRIVATE ${HIDAPI_LIB})

# Create the Python module
pybind11_add_module(easylink easylink_wrapper.cpp)

# Link the EasyLinkSDK library to the wrapper
target_link_libraries(easylink PRIVATE EasyLinkSDK)
