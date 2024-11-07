# unauthorized_process_terminator.py

import psutil
import logging
from config import ALLOWED_PROCESSES

# 设置日志
logging.basicConfig(
    filename='unauthorized_process_terminator.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def terminate_unauthorized_processes():
    """
    终止所有未被授权的进程。
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 检查进程是否在授权列表中
            if proc.info['name'] not in ALLOWED_PROCESSES:
                proc.terminate()
                logging.info(f"终止未授权进程: PID {proc.info['pid']}, Name {proc.info['name']}")
                print(f"终止未授权进程: PID {proc.info['pid']}, Name {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 忽略无法访问的进程
            pass

if __name__ == "__main__":
    terminate_unauthorized_processes()
