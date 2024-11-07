import os
import time
import logging
import pyperclip
import psutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    filename='file_watcher.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class PermissionsManager:
    def __init__(self, protected_files):
        self.protected_files = protected_files

    def set_read_only(self, file_path):
        try:
            # Set the file to read-only using Windows command
            subprocess.run(["icacls", file_path, "/deny", "*S-1-1-0:(W,D)"], check=True)
            logging.info(f"Set read-only permissions for file: {file_path}")
            print(f"[INFO] Set read-only permissions for file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to set read-only permissions for {file_path}: {e}")

    def reset_permissions(self, file_path):
        try:
            # Reset the file permissions to default
            subprocess.run(["icacls", file_path, "/reset"], check=True)
            logging.info(f"Reset permissions for file: {file_path}")
            print(f"[INFO] Reset permissions for file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to reset permissions for {file_path}: {e}")

    def apply_protection(self):
        for file_path in self.protected_files:
            self.set_read_only(file_path)

    def reset_all_permissions(self):
        for file_path in self.protected_files:
            self.reset_permissions(file_path)

    def apply_read_only_to_all(self):
        for file_path in self.protected_files:
            self.set_read_only(file_path)

class NetworkMonitor:
    def __init__(self, protected_directories):
        self.protected_directories = protected_directories

    def check_shared_directories(self):
        try:
            # Execute the net share command to get all shared directories
            result = subprocess.run(["net", "share"], capture_output=True, text=True, check=True)
            output = result.stdout

            # Check if any protected directory is being shared
            for protected_dir in self.protected_directories:
                if protected_dir.lower() in output.lower():
                    self.remove_shared_directory(protected_dir)
                    logging.warning(f"Unauthorized shared directory removed: {protected_dir}")
                    print(f"[WARNING] Unauthorized shared directory removed: {protected_dir}")
        
        except Exception as e:
            logging.error(f"Failed to check shared directories: {e}")

    def remove_shared_directory(self, directory):
        try:
            # Execute the command to remove shared directory
            subprocess.run(["net", "share", directory, "/delete"], check=True)
            logging.info(f"Removed shared directory: {directory}")
        except Exception as e:
            logging.error(f"Failed to remove shared directory {directory}: {e}")

class NotificationHandler:
    def __init__(self):
        # Initialize tkinter root and hide it for future use
        self.root = tk.Tk()
        self.root.withdraw()

    def show_warning(self, message):
        try:
            # Show warning message box to the user
            messagebox.showwarning("Warning", message)
            logging.info(f"User notified with warning: {message}")
        except Exception as e:
            logging.error(f"Failed to show notification: {e}")

    def show_info(self, message):
        try:
            # Show informational message box to the user
            messagebox.showinfo("Information", message)
            logging.info(f"User notified with information: {message}")
        except Exception as e:
            logging.error(f"Failed to show notification: {e}")

class FileWatcherHandler(FileSystemEventHandler):
    def __init__(self, protected_files, whitelist_processes, protected_directories):
        self.protected_files = protected_files
        self.whitelist_processes = whitelist_processes
        self.permissions_manager = PermissionsManager(protected_files)
        self.permissions_manager.apply_protection()
        self.network_monitor = NetworkMonitor(protected_directories)
        self.notification_handler = NotificationHandler()

    def clear_clipboard(self):
        # Clear clipboard content to prevent copy-paste actions
        try:
            pyperclip.copy('')
            logging.info("Clipboard cleared.")
        except Exception as e:
            logging.error(f"Failed to clear clipboard: {e}")

    def terminate_process_if_unauthorized(self, process_name):
        # Terminate unauthorized processes
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                try:
                    psutil.Process(proc.info['pid']).terminate()
                    logging.warning(f"Terminated unauthorized process: {proc.info['name']} ({proc.info['pid']})")
                    self.notification_handler.show_warning(f"Unauthorized process terminated: {proc.info['name']}")
                except Exception as e:
                    logging.error(f"Failed to terminate process {proc.info['name']}: {e}")

    def restore_file_extension(self, event_path):
        # Restore file extension if changed
        original_extension = ".moc3"  # Assuming moc3 is the original extension
        if not event_path.endswith(original_extension):
            base_name = os.path.splitext(event_path)[0]
            restored_path = f"{base_name}{original_extension}"
            os.rename(event_path, restored_path)
            logging.info(f"Restored file extension: {restored_path}")
            print(f"[INFO] Restored file extension: {restored_path}")
            self.notification_handler.show_info(f"File extension restored: {restored_path}")

    def on_modified(self, event):
        if not event.is_directory and event.src_path in self.protected_files:
            logging.warning(f"Protected file modified: {event.src_path}")
            print(f"[WARNING] Protected file modified: {event.src_path}")
            self.clear_clipboard()
            self.notification_handler.show_warning(f"Protected file modified: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory and event.src_path in self.protected_files:
            logging.warning(f"Protected file deleted: {event.src_path}")
            print(f"[WARNING] Protected file deleted: {event.src_path}")
            self.notification_handler.show_warning(f"Protected file deleted: {event.src_path}")

    def on_created(self, event):
        base_name = os.path.basename(event.src_path)
        for protected_file in self.protected_files:
            if base_name in protected_file and event.src_path != protected_file:
                logging.warning(f"Unauthorized copy created: {event.src_path}")
                print(f"[WARNING] Unauthorized copy created: {event.src_path}")
                try:
                    os.remove(event.src_path)
                    logging.info(f"Unauthorized copy deleted: {event.src_path}")
                    self.notification_handler.show_warning(f"Unauthorized copy created and deleted: {event.src_path}")
                except Exception as e:
                    logging.error(f"Failed to delete unauthorized copy: {event.src_path}, Error: {e}")

    def on_moved(self, event):
        if event.src_path in self.protected_files:
            # Restore file to original location if moved
            try:
                subprocess.run(["mv", event.dest_path, event.src_path], check=True)
                logging.info(f"Restored moved file to original location: {event.src_path}")
                print(f"[INFO] Restored moved file to original location: {event.src_path}")
                self.notification_handler.show_info(f"File moved and restored: {event.src_path}")
            except Exception as e:
                logging.error(f"Failed to restore moved file: {e}")

    def monitor_unauthorized_processes(self):
        unauthorized_tools = ['totalcmd', 'filezilla', 'winscp']  # Example unauthorized tools
        for tool in unauthorized_tools:
            self.terminate_process_if_unauthorized(tool)

    def allow_whitelisted_processes(self):
        # Ensure whitelisted processes like VTube Studio can access files
        for proc in psutil.process_iter(['pid', 'name']):
            if any(allowed.lower() in proc.info['name'].lower() for allowed in self.whitelist_processes):
                logging.info(f"Whitelisted process is running: {proc.info['name']} ({proc.info['pid']})")

    def monitor_network_shares(self):
        self.network_monitor.check_shared_directories()

    def reset_all_file_permissions(self):
        # Reset permissions for all protected files
        self.permissions_manager.reset_all_permissions()
        self.notification_handler.show_info("All file permissions have been reset to default.")

    def apply_read_only_permissions(self):
        # Apply read-only permissions for all protected files
        self.permissions_manager.apply_read_only_to_all()
        self.notification_handler.show_info("Read-only permissions have been applied to all protected files.")

def start_file_watcher(protected_files, whitelist_processes, protected_directories):
    event_handler = FileWatcherHandler(protected_files, whitelist_processes, protected_directories)
    observer = Observer()

    for file_path in protected_files:
        directory = os.path.dirname(file_path)
        observer.schedule(event_handler, directory, recursive=False)
        logging.info(f"Started watching directory: {directory}")
        print(f"Started watching directory: {directory}")

    observer.start()
    try:
        while True:
            event_handler.monitor_unauthorized_processes()
            event_handler.allow_whitelisted_processes()
            event_handler.monitor_network_shares()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("File watcher manually stopped.")
        print("File watcher manually stopped.")
    observer.join()

if __name__ == "__main__":
    PROTECTED_FILES = [
        r"D:\SteamLibrary\steamapps\common\VTube Studio\VTube Studio_Data\StreamingAssets\Live2DModels\ShanLan-test\ShanLan-Basic.moc3"
    ]
    WHITELIST_PROCESSES = [
        "VTube Studio.exe"
    ]
    PROTECTED_DIRECTORIES = [
        r"D:\SteamLibrary\steamapps\common\VTube Studio\VTube Studio_Data\StreamingAssets\Live2DModels",
        r"D:\SteamLibrary\steamapps\common\VTube Studio\VTube Studio_Data\StreamingAssets\Live2DModels\ShanLan-test"
    ]
    start_file_watcher(PROTECTED_FILES, WHITELIST_PROCESSES, PROTECTED_DIRECTORIES)
