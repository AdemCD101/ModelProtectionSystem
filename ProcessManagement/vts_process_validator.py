# vts_process_validator.py

import psutil
import logging
from config import VTS_PROCESS_NAME

# 设置日志
logging.basicConfig(
    filename='vts_process_validator.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def is_vts_running():
    """
    验证VTube Studio进程是否正在运行。
    :return: 如果进程存在则返回True，否则返回False。
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == VTS_PROCESS_NAME.lower():
                logging.info(f"VTube Studio 正在运行: PID {proc.info['pid']}, Name {proc.info['name']}")
                print(f"VTube Studio 正在运行: PID {proc.info['pid']}, Name {proc.info['name']}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    logging.warning("未检测到 VTube Studio 进程。")
    print("未检测到 VTube Studio 进程。")
    return False

if __name__ == "__main__":
    is_vts_running()
