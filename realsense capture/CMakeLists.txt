cmake_minimum_required( VERSION 3.0 FATAL_ERROR )
set( CMAKE_VERBOSE_MAKEFILE ON )

project(realsense_capture)

set(CMAKE_CXX_STANDARD 11)

get_filename_component( CINDER_PATH "/Users/manster/Documents/cinder_cmake/" ABSOLUTE )
get_filename_component( APP_PATH "${CMAKE_CURRENT_SOURCE_DIR}/" ABSOLUTE )

include( "${CINDER_PATH}/proj/cmake/modules/cinderMakeApp.cmake" )

include_directories("/Users/manster/Documents/librealsense-1.12.1/include")
LINK_DIRECTORIES("/Users/manster/Documents/librealsense-1.12.1")
LINK_LIBRARIES(librealsense.1.12.1.dylib)

include_directories("/usr/local/include")
LINK_DIRECTORIES("/usr/local/Cellar/opencv/2.4.13.2/lib")
LINK_LIBRARIES(libopencv_core.2.4.13.dylib)
LINK_LIBRARIES(libopencv_highgui.2.4.13.dylib)
LINK_LIBRARIES(libopencv_imgproc.2.4.13.dylib)

ci_make_app(
        APP_NAME    "RealSense_Capture"
        SOURCES     ${APP_PATH}/src/main.cpp
        CINDER_PATH ${CINDER_PATH}
)
