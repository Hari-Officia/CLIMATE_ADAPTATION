import os
import sys
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_ad2_recovery import run_phase_ad2_recovery, AUDIT_DIR, RESEARCH_DIR
from research.quantum_advantage.hardware.ibm_quantum_authenticator import IBMQuantumAuthenticator

def test_phase_ad2_recovery_execution():
    """Tests Phase AD-2 authentication recovery audit."""
    run_phase_ad2_recovery()

    # 1. Verify research artifacts in research/quantum_advantage/phase_ad2/
    status_file = os.path.join(RESEARCH_DIR, "PHASE_AD2_STATUS.json")
    assert os.path.exists(status_file), "PHASE_AD2_STATUS.json missing"
    with open(status_file, "r", encoding="utf-8") as f:
        status_data = json.load(f)

    assert status_data["SCIENTIFIC_EXPERIMENT_EXECUTED"] is False
    assert status_data["PRODUCTION_UNCHANGED"] is True
    assert status_data["CREDENTIAL_SECURITY"] == "PASS"

    provider_file = os.path.join(RESEARCH_DIR, "PHASE_AD2_PROVIDER.json")
    assert os.path.exists(provider_file), "PHASE_AD2_PROVIDER.json missing"

    backends_file = os.path.join(RESEARCH_DIR, "PHASE_AD2_BACKENDS.json")
    assert os.path.exists(backends_file), "PHASE_AD2_BACKENDS.json missing"
    with open(backends_file, "r", encoding="utf-8") as f:
        backends_data = json.load(f)
    assert len(backends_data["retired_backends"]) > 0
    assert backends_data["retired_backends"][0]["backend_name"] == "ibm_sherbrooke"

    # 2. Verify 19 audit reports in AUDIT/PHASE_AD2/
    audit_files = [
        "00_ENVIRONMENT.md", "01_CREDENTIAL_STATUS.md", "02_AUTHENTICATION.md",
        "03_PROVIDER_IDENTITY.md", "04_BACKEND_DISCOVERY.md", "05_BACKEND_FILTERING.md",
        "06_RETIRED_BACKEND_REJECTION.md", "07_PHYSICAL_BACKEND_SELECTION.md", "08_TECHNICAL_CIRCUIT.md",
        "09_PROVIDER_JOB.md", "10_JOB_RETRIEVAL.md", "11_RAW_RESULT.md",
        "12_CALIBRATION.md", "13_TRANSPILATION.md", "14_PHYSICAL_PROOF.md",
        "15_NO_FALLBACK.md", "16_SECURITY.md", "17_PRODUCTION_INTEGRITY.md",
        "18_FINAL_PHASE_AD2_CERTIFICATION.md"
    ]

    for af in audit_files:
        path = os.path.join(AUDIT_DIR, af)
        assert os.path.exists(path), f"Audit report missing: {af}"

def test_credential_detection_security():
    """Validates credential detection without token leakage."""
    cred_data = IBMQuantumAuthenticator.detect_credentials()
    assert cred_data["credential_security"] == "SECURE_ENVIRONMENT_ONLY"
    assert cred_data["token_exposed_in_logs"] is False
    assert cred_data["credential_status"] in ["PRESENT", "ABSENT", "INVALID_FORMAT"]
