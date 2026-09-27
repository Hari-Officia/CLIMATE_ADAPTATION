import os
import sys
import json
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_ad4r2_reconciliation import run_phase_ad4r2_reconciliation

def test_phase_ad4r2_reconciliation():
    """Top-level test for Phase AD-4R2 reconciliation script execution."""
    run_phase_ad4r2_reconciliation()
    status_file = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_ad4r2", "PHASE_AD4R2_STATUS.json")
    assert os.path.exists(status_file)
