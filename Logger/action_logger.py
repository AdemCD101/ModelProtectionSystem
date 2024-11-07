# action_logger.py

import logging

# 设置日志
logging.basicConfig(
    filename='action.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_action(action_message):
    """
    记录用户执行的操作日志。
    :param action_message: 描述操作的消息字符串
    """
    logging.info(action_message)
    print(f"Action logged: {action_message}")

if __name__ == "__main__":
    log_action("测试日志记录功能。")
