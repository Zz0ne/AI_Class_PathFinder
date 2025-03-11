cmake_minimum_required(VERSION 3.10)

project(AI_Class_PathFinder VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(SOURCES
        src/main.cpp
)

include_directories(include)

add_executable(${PROJECT_NAME} ${SOURCES})