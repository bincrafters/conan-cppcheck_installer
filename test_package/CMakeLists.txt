cmake_minimum_required(VERSION 2.8.11)

project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_program(CPPCHECK_CMD cppcheck)

if ( NOT CPPCHECK_CMD )
    message(FATAL_ERROR "cppcheck not found!")
else()
	message(STATUS "Found cppcheck")
	execute_process(COMMAND ${CPPCHECK_CMD} --version)
endif()





