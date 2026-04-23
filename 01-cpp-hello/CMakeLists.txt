cmake_minimum_required(VERSION 3.14)
project(hello-server)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)
FetchContent_Declare(
  httplib
  GIT_REPOSITORY https://github.com/yhirose/cpp-httplib.git
  GIT_TAG        v0.16.0
)
FetchContent_MakeAvailable(httplib)

add_executable(server main.cpp)
target_link_libraries(server PRIVATE httplib::httplib)
