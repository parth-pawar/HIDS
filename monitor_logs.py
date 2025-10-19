import win32evtlog
from datetime import datetime

ALERT_FILE = "alerts.log"

# Event IDs to monitor per log type
SUSPICIOUS_EVENTS = {
    "Security": [4625, 4672, 4688, 4624, 4634, 4720, 4722, 4726, 4732],
    "System": [7034, 7040, 6005, 6006, 6013,7036],
    "Application": [1000, 1001],
    "Microsoft-Windows-Windows Defender/Operational": [1116, 1117],
    "Microsoft-Windows-WindowsUpdateClient": [20],
}


def log_alert(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} ALERT: {message}"
    print(entry)
    with open(ALERT_FILE, "a") as f:
        f.write(entry + "\n")


def monitor_logs(interval=15):
    import time
    import win32evtlog

    last_records = {}

    while True:
        for log_type, event_ids in SUSPICIOUS_EVENTS.items():
            try:
                handle = win32evtlog.OpenEventLog(None, log_type)
                flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
                total_records = win32evtlog.GetNumberOfEventLogRecords(handle)
                last_record = last_records.get(log_type, 0)

                events = win32evtlog.ReadEventLog(handle, flags, 0)
                if events:
                    for event in events:
                        if event.RecordNumber <= last_record:
                            continue
                        if event.EventID in event_ids:
                            timestamp = event.TimeGenerated.Format()
                            provider = str(event.SourceName)
                            eid = event.EventID
                            log_alert(f"EventLog {log_type} | {timestamp} | {provider} | ID: {eid}")

                last_records[log_type] = total_records

            except Exception as e:
                log_alert(f"Could not read {log_type}: {e}")

        time.sleep(interval)
