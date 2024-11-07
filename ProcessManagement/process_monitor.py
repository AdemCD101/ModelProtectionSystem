import psutil
import logging

# Configure logging
logging.basicConfig(
    filename='process_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ProcessMonitor:
    def __init__(self, unauthorized_processes, whitelisted_processes):
        self.unauthorized_processes = unauthorized_processes
        self.whitelisted_processes = whitelisted_processes

    def terminate_unauthorized_processes(self):
        for process_name in self.unauthorized_processes:
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    try:
                        psutil.Process(proc.info['pid']).terminate()
                        logging.warning(f"Terminated unauthorized process: {proc.info['name']} ({proc.info['pid']})")
                        print(f"[WARNING] Terminated unauthorized process: {proc.info['name']} ({proc.info['pid']})")
                    except Exception as e:
                        logging.error(f"Failed to terminate process {proc.info['name']}: {e}")

    def check_whitelisted_processes(self):
        # Ensure whitelisted processes are running properly
        for proc in psutil.process_iter(['pid', 'name']):
            if any(allowed.lower() in proc.info['name'].lower() for allowed in self.whitelisted_processes):
                logging.info(f"Whitelisted process is running: {proc.info['name']} ({proc.info['pid']})")

if __name__ == "__main__":
    UNAUTHORIZED_PROCESSES = [
        'totalcmd', 'filezilla', 'winscp'
    ]
    WHITELISTED_PROCESSES = [
        'VTube Studio.exe'
    ]

    process_monitor = ProcessMonitor(UNAUTHORIZED_PROCESSES, WHITELISTED_PROCESSES)

    try:
        while True:
            process_monitor.terminate_unauthorized_processes()
            process_monitor.check_whitelisted_processes()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Process monitor manually stopped.")
        print("Process monitor manually stopped.")
