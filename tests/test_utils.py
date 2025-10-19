import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from utils import compute_hash, alert

def test_compute_hash(tmp_path):
    test_file = tmp_path / "file.txt"
    test_file.write_text("Test content")
    file_hash = compute_hash(str(test_file))
    assert file_hash is not None
    assert len(file_hash) == 64  # SHA256 length

def test_alert(tmp_path, capsys):
    from utils import ALERT_LOG
    import utils

    # Use temporary alert log
    temp_alert_log = tmp_path / "alerts.log"
    original_alert_log = utils.ALERT_LOG
    utils.ALERT_LOG = str(temp_alert_log)

    alert("Test alert")
    captured = capsys.readouterr()
    assert "ALERT: Test alert" in captured.out

    # Restore original alert log
    utils.ALERT_LOG = original_alert_log
