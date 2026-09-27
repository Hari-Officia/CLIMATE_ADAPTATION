import os
import sys
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_ad4_provisioning import run_phase_ad4_provisioning, AUDIT_DIR, RESEARCH_DIR
from research.quantum_advantage.hardware.ibm_ad4_provisioner import IBMAD4Provisioner

def test_phase_ad4_provisioning_execution():
    """Tests Phase AD-4 account and instance provisioning gate."""
    run_phase_ad4_provisioning()

    # 1. Verify research artifacts in research/quantum_advantage/phase_ad4/
    status_file = os.path.join(RESEARCH_DIR, "PHASE_AD4_STATUS.json")
    assert os.path.exists(status_file), "PHASE_AD4_STATUS.json missing"
    with open(status_file, "r", encoding="utf-8") as f:
        status_data = json.load(f)

    assert status_data["SCIENTIFIC_EXPERIMENT_EXECUTED"] is False
    assert status_data["TECHNICAL_JOB_SUBMITTED"] is False
    assert status_data["PHYSICAL_QPU_VERIFIED"] is False
    assert status_data["PRODUCTION_UNCHANGED"] is True
    assert status_data["CREDENTIAL_SECURITY"] == "PASS"

    env_file = os.path.join(RESEARCH_DIR, "PHASE_AD4_ENVIRONMENT.json")
    assert os.path.exists(env_file), "PHASE_AD4_ENVIRONMENT.json missing"

    cred_file = os.path.join(RESEARCH_DIR, "PHASE_AD4_CREDENTIAL.json")
    assert os.path.exists(cred_file), "PHASE_AD4_CREDENTIAL.json missing"

    backends_file = os.path.join(RESEARCH_DIR, "PHASE_AD4_BACKENDS.json")
    assert os.path.exists(backends_file), "PHASE_AD4_BACKENDS.json missing"
    with open(backends_file, "r", encoding="utf-8") as f:
        backends_data = json.load(f)
    assert backends_data["retired_backends_excluded"] > 0

    # 2. Verify 15 audit reports in AUDIT/PHASE_AD4/
    audit_files = [
        "00_ENVIRONMENT.md", "01_CREDENTIAL_SECURITY.md", "02_PACKAGE_VALIDATION.md",
        "03_API_KEY_DETECTION.md", "04_INSTANCE_DISCOVERY.md", "05_SERVICE_AUTHENTICATION.md",
        "06_AUTH_ERROR_CLASSIFICATION.md", "07_BACKEND_DISCOVERY.md", "08_BACKEND_EXCLUSION.md",
        "09_PHYSICAL_BACKEND_DISCOVERY.md", "10_NO_EXPERIMENT_GATE.md", "11_PRODUCTION_ISOLATION.md",
        "12_TEST_RESULTS.md", "13_SECURITY_AUDIT.md", "14_FINAL_PHASE_AD4_CERTIFICATION.md"
    ]

    for af in audit_files:
        path = os.path.join(AUDIT_DIR, af)
        assert os.path.exists(path), f"Audit report missing: {af}"

def test_missing_credential_blocks():
    """Validates that missing credentials result in BLOCKED status without simulator fallback."""
    cred_info = IBMAD4Provisioner.detect_credentials()
    assert cred_info["credential_security"] == "PASS"
    assert cred_info["token_exposed_in_logs"] is False

    auth_info = IBMAD4Provisioner.authenticate_and_discover()
    if not cred_info["credential_present"]:
        assert auth_info["status"] == "BLOCKED"
        assert auth_info["authentication"] == "BLOCKED_UNAUTHENTICATED"
        assert auth_info["blocking_issue"] in ["IBM_API_KEY_ABSENT", "RUNTIME_PACKAGE_MISSING"]
