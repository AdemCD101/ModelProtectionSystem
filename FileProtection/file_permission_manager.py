# file_permission_manager.py
import os
import subprocess
import logging

# Configure logging
logging.basicConfig(
    filename='file_permission.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def set_file_readonly(file_path):
    """
    设置文件为只读权限。
    :param file_path: 文件路径
    """
    try:
        if os.name == 'nt':
            # Windows系统使用icacls命令
            subprocess.run(["icacls", file_path, "/grant", "Everyone:R"], check=True, text=True, capture_output=True)
        else:
            # Unix系统使用chmod命令
            subprocess.run(["chmod", "444", file_path], check=True)
        logging.info(f"File set to read-only: {file_path}")
        print(f"File set to read-only: {file_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to set file permissions for {file_path}: {e.stderr}")
        print(f"Failed to set file permissions for {file_path}")

if __name__ == "__main__":
    TEST_FILE = r"D:\\SteamLibrary\\steamapps\\common\\VTube Studio\\VTube Studio_Data\\StreamingAssets\\Live2DModels\\ShanLan-test\\ShanLan-Basic.moc3"
    set_file_readonly(TEST_FILE)

# action_logger.py
import logging

# Configure logging
logging.basicConfig(
    filename='action.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_action(action_message):
    """
    记录用户的操作。
    :param action_message: 操作信息
    """
    logging.info(action_message)
    print(action_message)

if __name__ == "__main__":
    log_action("Test log entry for action_logger.")

# user_notification.py
import logging

def notify_user(message):
    """
    通知用户特定的信息，可以通过不同方式（如GUI、命令行输出等）通知。
    :param message: 要通知的信息
    """
    print(f"[NOTIFICATION]: {message}")
    logging.info(f"User notified: {message}")

if __name__ == "__main__":
    notify_user("This is a test notification.")
