# network_activity_monitor.py

import psutil
import logging
import time
from config import MONITORED_PORTS, DEFAULT_NETWORK_CHECK_INTERVAL

# 设置日志
logging.basicConfig(
    filename='network_activity_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def monitor_network_activity():
    """
    监控网络活动的指定端口。
    """
    while True:
        for conn in psutil.net_connections(kind='inet'):
            try:
                if conn.laddr.port in MONITORED_PORTS:
                    logging.info(f"监测到端口活动: PID {conn.pid}, Port {conn.laddr.port}, Status {conn.status}")
                    print(f"监测到端口活动: PID {conn.pid}, Port {conn.laddr.port}, Status {conn.status}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        time.sleep(DEFAULT_NETWORK_CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_network_activity()
