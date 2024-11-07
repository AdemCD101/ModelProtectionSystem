# file_watcher.py
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    filename='file_watcher.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class FileWatcherHandler(FileSystemEventHandler):
    def __init__(self, protected_files):
        self.protected_files = protected_files

    def on_modified(self, event):
        if not event.is_directory and event.src_path in self.protected_files:
            logging.warning(f"Protected file modified: {event.src_path}")
            print(f"[WARNING] Protected file modified: {event.src_path}")
            # Handle the unauthorized modification if needed.

    def on_deleted(self, event):
        if not event.is_directory and event.src_path in self.protected_files:
            logging.warning(f"Protected file deleted: {event.src_path}")
            print(f"[WARNING] Protected file deleted: {event.src_path}")
            # Handle the unauthorized deletion if needed.

    def on_created(self, event):
        # Handle creation of potential unauthorized copies of the protected files
        base_name = os.path.basename(event.src_path)
        for protected_file in self.protected_files:
            if base_name in protected_file and event.src_path != protected_file:
                logging.warning(f"Unauthorized copy created: {event.src_path}")
                print(f"[WARNING] Unauthorized copy created: {event.src_path}")
                # Optionally delete the unauthorized copy
                try:
                    os.remove(event.src_path)
                    logging.info(f"Unauthorized copy deleted: {event.src_path}")
                except Exception as e:
                    logging.error(f"Failed to delete unauthorized copy: {event.src_path}, Error: {e}")


def start_file_watcher(protected_files):
    event_handler = FileWatcherHandler(protected_files)
    observer = Observer()

    for file_path in protected_files:
        directory = os.path.dirname(file_path)
        observer.schedule(event_handler, directory, recursive=False)
        logging.info(f"Started watching directory: {directory}")
        print(f"Started watching directory: {directory}")

    observer.start()
    try:
        while True:
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
    start_file_watcher(PROTECTED_FILES)