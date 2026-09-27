import os
import sys
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_ad3_verification import run_phase_ad3_verification, AUDIT_DIR, RESEARCH_DIR
from research.quantum_advantage.hardware.ibm_ad3_verifier import IBMAD3Verifier

def test_phase_ad3_verification_execution():
    """Tests Phase AD-3 physical IBM Quantum technical verification."""
    run_phase_ad3_verification()

    # 1. Verify research artifacts in research/quantum_advantage/phase_ad3/
    status_file = os.path.join(RESEARCH_DIR, "PHASE_AD3_STATUS.json")
    assert os.path.exists(status_file), "PHASE_AD3_STATUS.json missing"
    with open(status_file, "r", encoding="utf-8") as f:
        status_data = json.load(f)

    assert status_data["SCIENTIFIC_EXPERIMENT_EXECUTED"] is False
    assert status_data["PRODUCTION_UNCHANGED"] is True
    assert status_data["CREDENTIAL_SECURITY"] == "PASS"

    env_file = os.path.join(RESEARCH_DIR, "PHASE_AD3_ENVIRONMENT.json")
    assert os.path.exists(env_file), "PHASE_AD3_ENVIRONMENT.json missing"

    provider_file = os.path.join(RESEARCH_DIR, "PHASE_AD3_PROVIDER.json")
    assert os.path.exists(provider_file), "PHASE_AD3_PROVIDER.json missing"

    backend_file = os.path.join(RESEARCH_DIR, "PHASE_AD3_BACKEND.json")
    assert os.path.exists(backend_file), "PHASE_AD3_BACKEND.json missing"

    # 2. Verify 18 audit reports in AUDIT/PHASE_AD3/
    audit_files = [
        "00_ENVIRONMENT.md", "01_CREDENTIAL_SECURITY.md", "02_SERVICE_INITIALIZATION.md",
        "03_BACKEND_DISCOVERY.md", "04_BACKEND_FILTERING.md", "05_PHYSICAL_AUTHENTICITY.md",
        "06_BACKEND_PROVENANCE.md", "07_TECHNICAL_CIRCUIT.md", "08_TRANSPILATION.md",
        "09_JOB_SUBMISSION.md", "10_JOB_RETRIEVAL.md", "11_RAW_COUNTS.md",
        "12_CALIBRATION_PROVENANCE.md", "13_AUTHENTICITY_TESTS.md", "14_FAILURE_HANDLING.md",
        "15_PRODUCTION_ISOLATION.md", "16_REPRODUCIBILITY.md", "17_FINAL_PHASE_AD3_CERTIFICATION.md"
    ]

    for af in audit_files:
        path = os.path.join(AUDIT_DIR, af)
        assert os.path.exists(path), f"Audit report missing: {af}"

def test_authenticity_and_redaction():
    """Validates that credentials are redacted and non-simulator fallbacks are prevented."""
    cred_data = IBMAD3Verifier.verify_credentials()
    assert cred_data["credential_security"] == "PASS"
    assert cred_data["token_exposed_in_logs"] is False

    backend_data = IBMAD3Verifier.discover_and_filter_backends()
    assert len(backend_data["retired_backends"]) > 0
    assert backend_data["retired_backends"][0]["backend_name"] == "ibm_sherbrooke"
