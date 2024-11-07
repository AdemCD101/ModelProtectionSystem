# process_monitor.py

import psutil
import logging
import time
from config import ALLOWED_PROCESSES, DEFAULT_RETRY_COUNT, DEFAULT_RETRY_DELAY

# 设置日志
logging.basicConfig(
    filename='process_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def is_vts_running():
    """
    检查VTube Studio进程是否正在运行。
    :return: 如果VTS进程在运行，则返回True，否则返回False。
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] in ALLOWED_PROCESSES:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def terminate_unauthorized_processes():
    """
    终止未授权的进程。
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] not in ALLOWED_PROCESSES:
                proc.terminate()
                logging.info(f"终止未授权进程: PID {proc.info['pid']}, Name {proc.info['name']}")
                print(f"终止未授权进程: PID {proc.info['pid']}, Name {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def monitor_processes():
    """
    持续监控进程并确保只有授权的进程在运行。
    """
    retry_count = 0
    while True:
        if is_vts_running():
            retry_count = 0  # 如果VTS进程在运行，则重置重试计数
        else:
            retry_count += 1
            logging.warning("VTube Studio 未检测到正在运行。重试计数: %d", retry_count)
            print("VTube Studio 未检测到正在运行。重试计数: %d" % retry_count)
            if retry_count >= DEFAULT_RETRY_COUNT:
                logging.error("VTube Studio 多次未检测到，可能存在异常情况。")
                print("VTube Studio 多次未检测到，可能存在异常情况。")
                break

        # 终止未授权进程
        terminate_unauthorized_processes()

        # 等待设定的延迟时间
        time.sleep(DEFAULT_RETRY_DELAY)

if __name__ == "__main__":
    monitor_processes()
