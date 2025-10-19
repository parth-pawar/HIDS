import os
import hashlib
import json
import time

# Files to ignore (HIDS self-files)
IGNORED_FILES = [
    r"C:\Users\Hp\Desktop\HIDS\alerts.log",
    r"C:\Users\Hp\Desktop\HIDS\file_baseline.json"
]

# Folders to completely ignore (like venv or HIDS project folder)
IGNORED_FOLDERS = [
    r"C:\Users\Hp\Desktop\HIDS\venv",
    r"C:\Users\Hp\Desktop\HIDS\__pycache__",
    r"C:\Users\Hp\Desktop\HIDS"
]

# Folders to monitor
MONITORED_FOLDERS = [
    r"C:\Users\Hp\Documents",
    r"C:\Users\Hp\Downloads",
    r"C:\Users\Hp\Desktop",
    r"C:\Users\Hp\Pictures",
]

BASELINE_FILE = r"C:\Users\Hp\Desktop\HIDS\file_baseline.json"


def get_file_hash(filepath):
    """Generate SHA256 hash of a file."""
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None


def create_baseline():
    """Create baseline of monitored files."""
    baseline = {}

    for folder in MONITORED_FOLDERS:
        for root, dirs, files in os.walk(folder):
            # Skip ignored folders
            dirs[:] = [d for d in dirs if not any(os.path.join(root, d).startswith(ignored) for ignored in IGNORED_FOLDERS)]

            for file in files:
                filepath = os.path.join(root, file)
                if filepath in IGNORED_FILES:
                    continue

                file_hash = get_file_hash(filepath)
                if file_hash:
                    baseline[filepath] = file_hash

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print("[+] Baseline created and saved.")


def check_files():
    """Check for new, modified, or deleted files."""
    try:
        with open(BASELINE_FILE, "r") as f:
            baseline = json.load(f)
    except FileNotFoundError:
        print("[-] Baseline not found. Run create_baseline() first.")
        return

    current_files = {}

    for folder in MONITORED_FOLDERS:
        for root, dirs, files in os.walk(folder):
            # Skip ignored folders
            dirs[:] = [d for d in dirs if not any(os.path.join(root, d).startswith(ignored) for ignored in IGNORED_FOLDERS)]

            for file in files:
                filepath = os.path.join(root, file)
                if filepath in IGNORED_FILES:
                    continue

                file_hash = get_file_hash(filepath)
                if file_hash:
                    current_files[filepath] = file_hash

    # Compare baseline with current files
    for filepath, old_hash in baseline.items():
        if filepath not in current_files:
            print(f"[ALERT] File deleted: {filepath}")
        elif current_files[filepath] != old_hash:
            print(f"[ALERT] File modified: {filepath}")

    for filepath in current_files:
        if filepath not in baseline:
            print(f"[ALERT] New file detected: {filepath}")
