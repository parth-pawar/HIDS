import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from monitor_proc import check_processes
from unittest.mock import patch

@patch("psutil.process_iter")
def test_suspicious_process(mock_proc_iter, capsys):
    # Simulate a suspicious process
    mock_proc_iter.return_value = [
        type("proc", (object,), {"info": {"name": "notepad.exe"}})()
    ]

    check_processes()

    captured = capsys.readouterr()
    assert "Suspicious process detected" in captured.out
