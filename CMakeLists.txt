cmake_minimum_required(VERSION 3.10)

project(AI_Class_PathFinder VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

set(SOURCES
        src/main.cpp
        src/algorithms/helpers/Node.cpp
        src/algorithms/bestFirstSearch.cpp
)

include_directories(include)

add_executable(${PROJECT_NAME} ${SOURCES})
