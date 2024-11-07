import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    filename='drag_and_drop_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class DragAndDropHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created (potential drag & drop detected): {event.src_path}")
            print(f"File created: {event.src_path}")
            # Attempt to delete the file if it's an unauthorized copy
            if self.is_unauthorized_copy(event.src_path):
                try:
                    os.remove(event.src_path)
                    logging.info(f"Unauthorized copy deleted: {event.src_path}")
                    print(f"Unauthorized copy deleted: {event.src_path}")
                except Exception as e:
                    logging.error(f"Failed to delete unauthorized copy: {event.src_path}, Error: {e}")
                    print(f"Failed to delete unauthorized copy: {event.src_path}, Error: {e}")

    def is_unauthorized_copy(self, file_path):
        # Define conditions that mark the file as unauthorized
        if "copy" in file_path.lower() or "- 副本" in file_path:
            return True
        return False

def monitor_drag_and_drop(target_path):
    event_handler = DragAndDropHandler()
    observer = Observer()
    observer.schedule(event_handler, target_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    TARGET_PATH = r"D:\SteamLibrary\steamapps\common\VTube Studio\VTube Studio_Data\StreamingAssets\Live2DModels"
    monitor_drag_and_drop(TARGET_PATH)
