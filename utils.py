# utils.py
import hashlib
import json
import os
from datetime import datetime

BASELINE_FILE = "baseline.json"
ALERT_LOG = "alerts.log"

def compute_hash(file_path):
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return None

def load_baseline():
    """Load baseline hashes from file."""
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_baseline(baseline):
    """Save baseline hashes to file."""
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

def alert(message):
    """Log and print alerts."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ALERT: {message}"
    print(entry)
    with open(ALERT_LOG, "a") as f:
        f.write(entry + "\n")
