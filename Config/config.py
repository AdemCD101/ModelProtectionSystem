# config.py

import os

# 配置项，用于管理应用程序中的各种常量和配置参数

# VTube Studio模型路径配置
VTS_MODEL_PATH = r"D:\SteamLibrary\steamapps\common\VTube Studio\VTube Studio_Data\StreamingAssets\Live2DModels"
# 测试模型路径配置
TEST_MODEL_PATH = os.path.join(VTS_MODEL_PATH, "ShanLan-test")
# 核心模型文件路径配置
CORE_MODEL_FILE = os.path.join(TEST_MODEL_PATH, "ShanLan-Basic.moc3")

# 权限控制配置
READ_ONLY_PERMISSION = '444'  # Unix 下只读权限
WINDOWS_READ_ONLY_COMMAND = ["icacls", "{file_path}", "/grant", "Everyone:R"]

# 日志文件配置
LOG_FILE_DIRECTORY = os.path.join(os.getcwd(), 'logs')
ACTION_LOG_FILE = os.path.join(LOG_FILE_DIRECTORY, 'action.log')
INTEGRITY_LOG_FILE = os.path.join(LOG_FILE_DIRECTORY, 'file_integrity.log')
PERMISSION_LOG_FILE = os.path.join(LOG_FILE_DIRECTORY, 'file_permission.log')

# 监控配置
MONITOR_DIRECTORIES = [VTS_MODEL_PATH, TEST_MODEL_PATH]
MONITOR_CORE_FILES = [CORE_MODEL_FILE]

# 用户通知相关配置
NOTIFICATION_METHOD = "console"  # 可选择 "console"、"gui" 或其他通知方式

# 网络保护配置
ALLOWED_PROCESSES = ["VTube Studio.exe"]

# 共享目录配置
SHARED_FOLDER_WARNING = "共享目录检测到敏感文件，建议立即停止共享。"

# 剪贴板和拖拽保护配置
CLIPBOARD_CLEAR_MESSAGE = "剪贴板已清空，防止非法拷贝操作。"
DRAG_DROP_WARNING = "拖拽操作已被阻止，防止敏感文件泄露。"

# 默认重试次数和延迟配置
DEFAULT_RETRY_COUNT = 5
DEFAULT_RETRY_DELAY = 3  # 单位：秒

# 创建日志目录
if not os.path.exists(LOG_FILE_DIRECTORY):
    os.makedirs(LOG_FILE_DIRECTORY)

# 配置函数

def get_config_value(key):
    return globals().get(key, None)

if __name__ == "__main__":
    # 测试配置项
    print("VTS模型路径:", VTS_MODEL_PATH)
    print("日志目录:", LOG_FILE_DIRECTORY)
    print("监控目录:", MONITOR_DIRECTORIES)
