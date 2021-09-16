cmake_minimum_required(VERSION 3.17)
project(interfaces)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)
link_libraries("tins")
link_libraries("pcap")
link_libraries("jsoncpp")

add_executable(interfaces interfaces.cpp interfaces.h packet_processing.cpp)
