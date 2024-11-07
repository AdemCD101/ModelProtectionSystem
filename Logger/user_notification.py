# user_notification.py

import logging
from config import USER_NOTIFICATION_SETTING

# 设置日志
logging.basicConfig(
    filename='user_notification.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def notify_user(message):
    """
    通知用户相关信息。
    :param message: 通知内容字符串
    """
    if USER_NOTIFICATION_SETTING:
        logging.info(f"通知用户: {message}")
        print(f"通知用户: {message}")
    else:
        logging.warning("用户通知功能被禁用。")
        print("用户通知功能被禁用。")

if __name__ == "__main__":
    notify_user("测试用户通知功能。")