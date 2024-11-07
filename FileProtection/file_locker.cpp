#include "file_locker.h"
#include <Windows.h>
#include <string>
#include <iostream>

bool FileLocker::lockFile(const std::string& filePath) {
    HANDLE hFile = CreateFile(
        filePath.c_str(),
        GENERIC_READ,
        0, // 不允许其他进程共享访问
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );

    if (hFile == INVALID_HANDLE_VALUE) {
        std::cerr << "Failed to lock file: " << filePath << ", Error: " << GetLastError() << std::endl;
        return false;
    }
    else {
        std::cout << "File locked: " << filePath << std::endl;
        CloseHandle(hFile);
        return true;
    }
}

bool FileLocker::unlockFile(const std::string& filePath) {
    HANDLE hFile = CreateFile(
        filePath.c_str(),
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE, // 允许其他进程共享访问
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );

    if (hFile == INVALID_HANDLE_VALUE) {
        std::cerr << "Failed to unlock file: " << filePath << ", Error: " << GetLastError() << std::endl;
        return false;
    }
    else {
        std::cout << "File unlocked: " << filePath << std::endl;
        CloseHandle(hFile);
        return true;
    }
}
