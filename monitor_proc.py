import psutil
from datetime import datetime

ALERT_FILE = "alerts.log"

# Example suspicious processes
SUSPICIOUS_PROCS = ["cmd.exe", "notepad.exe","wscript.exe",
    "cscript.exe",
    "mshta.exe",
    "rundll32.exe",
    "regsvr32.exe",
    "wmic.exe",
    "taskkill.exe",
    "net.exe",
    "schtasks.exe",
    "mimikatz.exe"]  # edit as needed


def log_alert(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} ALERT: {message}"
    print(entry)
    with open(ALERT_FILE, "a") as f:
        f.write(entry + "\n")


def check_processes():
    for proc in psutil.process_iter(['name']):
        try:
            pname = proc.info['name']
            if pname and pname.lower() in [p.lower() for p in SUSPICIOUS_PROCS]:
                log_alert(f"Suspicious process detected: {pname}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
