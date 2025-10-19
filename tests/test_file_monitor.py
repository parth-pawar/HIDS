import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from monitor_files import create_baseline, check_files, MONITORED_FOLDERS, BASELINE_FILE

def test_baseline_creation(tmp_path):
    # Use temporary folder instead of real monitored folders
    MONITORED_FOLDERS.clear()
    MONITORED_FOLDERS.append(tmp_path)

    # Use temporary baseline file
    temp_baseline = tmp_path / "file_baseline.json"
    original_baseline = BASELINE_FILE
    import monitor_files
    monitor_files.BASELINE_FILE = str(temp_baseline)

    # Create dummy file
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello HIDS!")

    # Create baseline
    create_baseline()
    assert os.path.exists(temp_baseline)

    # Restore original baseline path
    monitor_files.BASELINE_FILE = original_baseline

def test_file_modification(tmp_path, capsys):
    MONITORED_FOLDERS.clear()
    MONITORED_FOLDERS.append(tmp_path)

    # Use temporary baseline file
    temp_baseline = tmp_path / "file_baseline.json"
    original_baseline = BASELINE_FILE
    import monitor_files
    monitor_files.BASELINE_FILE = str(temp_baseline)

    # Create dummy file and baseline
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello HIDS!")
    create_baseline()

    # Modify file
    test_file.write_text("Modified content")

    # Check files
    check_files()
    captured = capsys.readouterr()
    assert "File modified" in captured.out

    # Restore original baseline path
    monitor_files.BASELINE_FILE = original_baseline
