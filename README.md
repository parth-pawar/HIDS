
# Windows Host-based Intrusion Detection System (HIDS)

## Overview

This project implements a Host-based Intrusion Detection System (HIDS) for Windows. It monitors:

1. Files — detects modifications, new files, or deletions in monitored folders.
2. Processes — detects suspicious or malware-like processes.
3. Event Logs — monitors Windows Security, System, Application, and Windows Defender logs for suspicious events.

Alerts are logged to `alerts.log` and printed in the console in real-time.

---

## Features

* File integrity monitoring using SHA256 hashes.
* Process monitoring for suspicious processes.
* Windows event log monitoring for critical event IDs.
* Baseline creation to establish a reference state for monitored files.
* Alerts written to log and console.
* Configurable monitored folders and ignored files/folders.
* Cross-module tests for file, process, and utility functions.

---
```
## Folder Structure

HIDS/
├─ monitor_files.py      # File monitoring
├─ monitor_proc.py       # Process monitoring
├─ monitor_logs.py       # Log monitoring
├─ utils.py              # Utility functions (hash, alert)
├─ file_baseline.json    # Baseline file (auto-generated)
├─ alerts.log            # Alert log
├─ tests/                # Automated pytest test cases
│   ├─ test_file_monitor.py
│   ├─ test_process_monitor.py
│   └─ test_utils.py
├─ main.py               # Main program to run HIDS
├─ README.md
└─ venv/                 # Virtual environment

```
---

## Installation & Setup

1. Clone the repository:

git clone <repository_url>
cd HIDS

2. Create virtual environment:

python -m venv venv

3. Activate virtual environment:
venv\Scripts\activate

4. Install dependencies:
pip install -r requirements.txt
# (psutil, pywin32, pytest)


## Usage

1. Run HIDS:

python main.py

* If `file_baseline.json` does not exist, it will automatically create a baseline.
* Press Ctrl+C to stop monitoring.

2. Alerts:

* All alerts are logged in `alerts.log` and printed on the console.

---


## Testing

### 2. Automated Testing (Pytest)

1. Activate the virtual environment:
venv\Scripts\activate

2. Run tests:
pytest -v tests/

* All tests are safe:

  * Use temporary folders/files (`tmp_path`) instead of your real files.
  * Mocked processes are used to simulate suspicious processes.
  * The real `file_baseline.json` is never deleted or modified.
 
* Tests include:

  * Baseline creation & file modification detection
  * Suspicious process detection
  * Utility functions (`compute_hash` and `alert`)

---

## Dependencies

* Python 3.11+
* Libraries:

  * psutil (process monitoring)
  * pywin32 (Windows event log monitoring)
  * pytest (automated testing)

---

## Notes

* Baseline creation may take time if monitored folders contain many files.
* Automated tests are **fast** because they use temporary files and mocks.
* Always back up `file_baseline.json` if you want to preserve historical hashes.

---

## Author
Parth Pawar
