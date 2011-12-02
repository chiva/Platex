#=============================================================================#
# Author: Santiago Reig                                                       #
# Date:   02.12.2011                                                          #
#                                                                             #
# Description: Platex Arduino firmware CMake                                  #
#                                                                             #
#=============================================================================#
set(CMAKE_MODULE_PATH    ${CMAKE_SOURCE_DIR}/cmake/modules)  # CMake module search path
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/cmake/toolchains/Arduino.cmake) # Arduino Toolchain


cmake_minimum_required(VERSION 2.8)
#====================================================================#
#  Setup Project                                                     #
#====================================================================#
project(Platex C CXX)
find_package(Arduino 22 REQUIRED)

add_subdirectory(PlatexFirmata)  # Add example directory to build
