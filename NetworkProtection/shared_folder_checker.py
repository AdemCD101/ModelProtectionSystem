# shared_folder_checker.py

import os
import logging
from config import SHARED_DIRECTORIES

# 设置日志
logging.basicConfig(
    filename='shared_folder_checker.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def check_shared_folders():
    """
    检查系统中是否存在共享目录，以防止敏感文件被共享。
    """
    for shared_dir in SHARED_DIRECTORIES:
        if os.path.exists(shared_dir):
            try:
                # 检查共享目录是否存在
                if os.path.isdir(shared_dir):
                    logging.info(f"检测到共享目录: {shared_dir}")
                    print(f"检测到共享目录: {shared_dir}")
                else:
                    logging.warning(f"路径存在但不是目录: {shared_dir}")
            except Exception as e:
                logging.error(f"检查共享目录时遇到错误: {shared_dir}, 错误: {e}")
                print(f"检查共享目录时遇到错误: {shared_dir}, 错误: {e}")
        else:
            logging.info(f"未检测到共享目录: {shared_dir}")
            print(f"未检测到共享目录: {shared_dir}")

if __name__ == "__main__":
    check_shared_folders()
