import win32clipboard
import time
import logging

# Configure logging
logging.basicConfig(
    filename='clipboard_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ClipboardManager:
    def __init__(self):
        self.previous_content = None
        self.error_count = 0
        self.max_errors = 5  # 设置最大错误次数，避免无限循环

    def get_clipboard_data(self):
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return data
        except Exception as e:
            logging.error(f"Error accessing clipboard: {e}")
            print(f"Error accessing clipboard: {e}")
            return None

    def clear_clipboard(self):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
        except Exception as e:
            logging.error(f"Error clearing clipboard: {e}")
            print(f"Error clearing clipboard: {e}")

    def monitor_clipboard(self):
        while True:
            try:
                current_content = self.get_clipboard_data()
                if current_content != self.previous_content:
                    self.previous_content = current_content
                    if current_content:
                        logging.info(f"Clipboard content detected and cleared: {current_content}")
                        print("Clipboard content detected and cleared.")
                        self.clear_clipboard()  # 清空剪贴板内容
                        self.error_count = 0  # 成功访问剪贴板时，重置错误计数
            except Exception as e:
                self.error_count += 1
                logging.error(f"Error accessing clipboard: {e}")
                print(f"Error accessing clipboard: {e}")
                if self.error_count >= self.max_errors:
                    print("Too many errors accessing clipboard, waiting for 10 seconds...")
                    time.sleep(10)
                    self.error_count = 0  # 重置错误计数

            time.sleep(1)  # Check clipboard every second

if __name__ == "__main__":
    manager = ClipboardManager()
    manager.monitor_clipboard()
