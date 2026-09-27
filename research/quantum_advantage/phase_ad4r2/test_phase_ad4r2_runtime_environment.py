import os
import sys
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_ad4r2_reconciliation import run_phase_ad4r2_reconciliation, AUDIT_DIR, RESEARCH_DIR
from research.quantum_advantage.hardware.ibm_ad4r2_reconciler import IBMAD4R2Reconciler

def test_phase_ad4r2_runtime_environment():
    """Tests Phase AD-4R2 IBM Quantum runtime environment reconciliation."""
    run_phase_ad4r2_reconciliation()

    # 1. Verify research artifacts in research/quantum_advantage/phase_ad4r2/
    status_file = os.path.join(RESEARCH_DIR, "PHASE_AD4R2_STATUS.json")
    assert os.path.exists(status_file), "PHASE_AD4R2_STATUS.json missing"
    with open(status_file, "r", encoding="utf-8") as f:
        status_data = json.load(f)

    assert status_data["SCIENTIFIC_EXPERIMENT_EXECUTED"] is False
    assert status_data["TECHNICAL_JOB_SUBMITTED"] is False
    assert status_data["PHYSICAL_QPU_VERIFIED"] is False
    assert status_data["PRODUCTION_UNCHANGED"] is True

    env_file = os.path.join(RESEARCH_DIR, "PHASE_AD4R2_ENVIRONMENT.json")
    assert os.path.exists(env_file), "PHASE_AD4R2_ENVIRONMENT.json missing"

    interp_file = os.path.join(RESEARCH_DIR, "PHASE_AD4R2_INTERPRETER.json")
    assert os.path.exists(interp_file), "PHASE_AD4R2_INTERPRETER.json missing"

    # 2. Verify 14 audit reports in AUDIT/PHASE_AD4R2/
    audit_files = [
        "00_ENVIRONMENT.md", "01_PYTHON_PATH.md", "02_VENV_CREATION.md",
        "03_PIP_PROVENANCE.md", "04_QISKIT_INSTALLATION.md", "05_IBM_RUNTIME_INSTALLATION.md",
        "06_RUNTIME_IMPORT.md", "07_MODULE_LOCATION.md", "08_ENVIRONMENT_CONTAMINATION.md",
        "09_NO_AUTHENTICATION.md", "10_NO_EXPERIMENT.md", "11_PRODUCTION_ISOLATION.md",
        "12_TEST_RESULTS.md", "13_FINAL_PHASE_AD4R2_CERTIFICATION.md"
    ]

    for af in audit_files:
        path = os.path.join(AUDIT_DIR, af)
        assert os.path.exists(path), f"Audit report missing: {af}"

def test_reconciliation_module_location():
    """Validates that path reconciliation returns project paths."""
    paths = IBMAD4R2Reconciler.get_paths()
    assert ".venv-ibm-hardware" in paths["research_venv"]
    cred_data = IBMAD4R2Reconciler.detect_credentials()
    assert cred_data["credential_security"] == "PASS"
    assert cred_data["token_exposed_in_logs"] is False
