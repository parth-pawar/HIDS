import threading
import time
import os
from monitor_files import create_baseline, check_files
from monitor_logs import monitor_logs
from monitor_proc import check_processes

BASELINE_FILE = "file_baseline.json"

def run_file_monitor(interval=30):
    while True:
        check_files()
        time.sleep(interval)

def run_log_monitor(interval=30):
    monitor_logs(interval=interval)

def run_process_monitor(interval=30):
    while True:
        check_processes()
        time.sleep(interval)

if __name__ == "__main__":
    print("=== Windows Host-based Intrusion Detection System (HIDS) ===")

    if not os.path.exists(BASELINE_FILE):
        print("Creating baseline for monitored folders...")
        create_baseline()
    else:
        print("Baseline already exists. Skipping creation.")

    # Start monitoring threads
    t1 = threading.Thread(target=run_file_monitor, daemon=True)
    t2 = threading.Thread(target=run_log_monitor, daemon=True)
    t3 = threading.Thread(target=run_process_monitor, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    print("\n[+] HIDS is running... Monitoring files, processes, and logs.")
    print("[*] Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] HIDS stopped by user.")
