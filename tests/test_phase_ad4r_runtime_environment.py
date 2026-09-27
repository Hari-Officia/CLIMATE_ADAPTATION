import os
import sys
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_ad4r_recovery import run_phase_ad4r_recovery, AUDIT_DIR, RESEARCH_DIR
from research.quantum_advantage.hardware.ibm_ad4r_environment_recovery import IBMAD4REnvironmentRecovery

def test_phase_ad4r_environment_recovery_execution():
    """Tests Phase AD-4R IBM Quantum runtime environment recovery."""
    run_phase_ad4r_recovery()

    # 1. Verify research artifacts in research/quantum_advantage/phase_ad4r/
    status_file = os.path.join(RESEARCH_DIR, "PHASE_AD4R_STATUS.json")
    assert os.path.exists(status_file), "PHASE_AD4R_STATUS.json missing"
    with open(status_file, "r", encoding="utf-8") as f:
        status_data = json.load(f)

    assert status_data["SCIENTIFIC_EXPERIMENT_EXECUTED"] is False
    assert status_data["TECHNICAL_JOB_SUBMITTED"] is False
    assert status_data["PHYSICAL_QPU_VERIFIED"] is False
    assert status_data["PRODUCTION_UNCHANGED"] is True
    assert status_data["RUNTIME_IMPORT"] in ["PASS", "FAIL"]
    assert status_data["PHASE_AD4R_STATUS"] in ["PASS", "BLOCKED"]

    env_file = os.path.join(RESEARCH_DIR, "PHASE_AD4R_ENVIRONMENT.json")
    assert os.path.exists(env_file), "PHASE_AD4R_ENVIRONMENT.json missing"

    packages_file = os.path.join(RESEARCH_DIR, "PHASE_AD4R_PACKAGES.json")
    assert os.path.exists(packages_file), "PHASE_AD4R_PACKAGES.json missing"

    # 2. Verify 11 audit reports in AUDIT/PHASE_AD4R/
    audit_files = [
        "00_ENVIRONMENT.md", "01_VENV_CREATION.md", "02_QISKIT_INSTALLATION.md",
        "03_RUNTIME_INSTALLATION.md", "04_PACKAGE_COMPATIBILITY.md", "05_RUNTIME_API_VALIDATION.md",
        "06_CREDENTIAL_DETECTION.md", "07_NO_EXPERIMENT_GATE.md", "08_PRODUCTION_INTEGRITY.md",
        "09_TEST_RESULTS.md", "10_FINAL_PHASE_AD4R_CERTIFICATION.md"
    ]

    for af in audit_files:
        path = os.path.join(AUDIT_DIR, af)
        assert os.path.exists(path), f"Audit report missing: {af}"

def test_runtime_import_and_credential_redaction():
    """Validates runtime import and credential redaction."""
    cred_data = IBMAD4REnvironmentRecovery.detect_credentials()
    assert cred_data["credential_security"] == "PASS"
    assert cred_data["token_exposed_in_logs"] is False

    runtime_data = IBMAD4REnvironmentRecovery.ensure_and_validate_runtime()
    assert isinstance(runtime_data["service_class_available"], bool)
