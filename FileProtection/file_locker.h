#ifndef FILE_LOCKER_H
#define FILE_LOCKER_H

#include <string>

class FileLocker {
public:
    // 锁定文件以防止其他进程访问
    static bool lockFile(const std::string& filePath);

    // 解锁文件以允许合法进程访问
    static bool unlockFile(const std::string& filePath);
};

#endif // FILE_LOCKER_H
