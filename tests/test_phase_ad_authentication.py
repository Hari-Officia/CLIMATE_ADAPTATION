import os
import sys
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_ad_authentication import run_phase_ad_authentication, AUDIT_DIR, RESEARCH_DIR
from research.quantum_advantage.hardware.physical_provider_authenticator import PhysicalProviderAuthenticator

def test_phase_ad_authentication_gate():
    """Tests Phase AD physical quantum provider authentication gate."""
    run_phase_ad_authentication()

    # 1. Verify research artifacts in research/quantum_advantage/phase_ad/
    status_file = os.path.join(RESEARCH_DIR, "PHASE_AD_STATUS.json")
    assert os.path.exists(status_file), "PHASE_AD_STATUS.json missing"
    with open(status_file, "r", encoding="utf-8") as f:
        status_data = json.load(f)

    assert status_data["SCIENTIFIC_EXPERIMENT_EXECUTED"] is False
    assert status_data["PRODUCTION_UNCHANGED"] is True
    assert status_data["CREDENTIAL_SECURITY"] == "PASS"

    provider_file = os.path.join(RESEARCH_DIR, "PHASE_AD_PROVIDER.json")
    assert os.path.exists(provider_file), "PHASE_AD_PROVIDER.json missing"

    backends_file = os.path.join(RESEARCH_DIR, "PHASE_AD_BACKENDS.json")
    assert os.path.exists(backends_file), "PHASE_AD_BACKENDS.json missing"
    with open(backends_file, "r", encoding="utf-8") as f:
        backends_data = json.load(f)
    assert len(backends_data["retired_backends"]) > 0
    assert backends_data["retired_backends"][0]["backend_name"] == "ibm_sherbrooke"

    # 2. Verify 25 audit reports in AUDIT/PHASE_AD/
    audit_files = [
        "00_PROVIDER_AUTHENTICATION.md", "01_PACKAGE_ENVIRONMENT.md", "02_CREDENTIAL_SECURITY.md",
        "03_INSTANCE_ACCESS.md", "04_BACKEND_DISCOVERY.md", "05_BACKEND_CLASSIFICATION.md",
        "06_SHERBROOKE_EXCLUSION.md", "07_PHYSICAL_BACKEND_SELECTION.md", "08_PHYSICAL_BACKEND_ASSERTION.md",
        "09_JOB_ID_AUTHENTICITY.md", "10_TECHNICAL_CIRCUIT.md", "11_PROVIDER_RESULT_RETRIEVAL.md",
        "12_RAW_RESULT_VERIFICATION.md", "13_CIRCUIT_IDENTITY.md", "14_TRANSPILATION.md",
        "15_PHYSICAL_MAPPING.md", "16_CALIBRATION.md", "17_TIMING.md", "18_NO_FALLBACK.md",
        "19_PROVIDER_HEALTH.md", "20_SECURITY.md", "21_PRODUCTION_INTEGRITY.md",
        "22_REPRODUCIBILITY.md", "23_REAL_HARDWARE_PROOF.md", "24_FINAL_PHASE_AD_CERTIFICATION.md"
    ]

    for af in audit_files:
        path = os.path.join(AUDIT_DIR, af)
        assert os.path.exists(path), f"Audit report missing: {af}"

def test_credential_security_and_redaction():
    """Validates that credentials are never exposed or hardcoded."""
    cred_info = PhysicalProviderAuthenticator.verify_credentials()
    assert cred_info["credential_security"] == "SECURE_ENVIRONMENT_ONLY"
    assert cred_info["token_exposed_in_logs"] is False
