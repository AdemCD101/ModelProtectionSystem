# 设置CMake最低版本要求
cmake_minimum_required(VERSION 3.10)

# 项目名称
project(ModelProtectionSystem)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)

# 添加源文件
set(SOURCES
    file_locker.cpp  # 直接写文件名，如果在同一目录下
)

# 添加可执行文件
add_executable(ModelProtectionSystem ${SOURCES})
