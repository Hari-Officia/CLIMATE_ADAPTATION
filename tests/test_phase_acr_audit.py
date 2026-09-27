import os
import sys
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.run_phase_acr_audit import run_phase_acr_audit, AUDIT_DIR, RESEARCH_DIR

def test_phase_acr_audit_execution():
    """Tests Phase AC-R authenticity and execution audit."""
    run_phase_acr_audit()

    # 1. Verify research artifacts in research/quantum_advantage/phase_acr/
    status_file = os.path.join(RESEARCH_DIR, "PHASE_ACR_STATUS.json")
    assert os.path.exists(status_file), "PHASE_ACR_STATUS.json missing"
    with open(status_file, "r") as f:
        status_data = json.load(f)
    assert status_data["PHASE_ACR_STATUS"] == "PASS"
    assert status_data["IS_SIMULATOR"] is True
    assert status_data["PHYSICAL_QPU_VERIFIED"] is False
    assert status_data["JOBS_PHYSICAL"] == 0
    assert status_data["JOBS_TOTAL"] > 0
    assert status_data["JOBS_HARDWARE_CALIBRATED_SIM"] == status_data["JOBS_TOTAL"]
    assert status_data["RESULTS_RECLASSIFIED"] is True
    assert status_data["REAL_HARDWARE_STATUS"] == "NOT_VERIFIED"
    assert status_data["PHASE_AC_STATUS"] == "BLOCKED"

    backend_file = os.path.join(RESEARCH_DIR, "PHASE_ACR_BACKEND_IDENTITY.json")
    assert os.path.exists(backend_file), "PHASE_ACR_BACKEND_IDENTITY.json missing"

    provider_file = os.path.join(RESEARCH_DIR, "PHASE_ACR_PROVIDER_IDENTITY.json")
    assert os.path.exists(provider_file), "PHASE_ACR_PROVIDER_IDENTITY.json missing"

    job_auth_file = os.path.join(RESEARCH_DIR, "PHASE_ACR_JOB_AUTHENTICITY.csv")
    assert os.path.exists(job_auth_file), "PHASE_ACR_JOB_AUTHENTICITY.csv missing"
    with open(job_auth_file, "r") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == status_data["JOBS_TOTAL"]
    for r in rows:
        assert r["evidence_level"] == "LEVEL_2"
        assert r["corrected_label"] == "HARDWARE_CALIBRATED_SIMULATION"

    reclass_file = os.path.join(RESEARCH_DIR, "PHASE_ACR_RESULT_RECLASSIFICATION.csv")
    assert os.path.exists(reclass_file), "PHASE_ACR_RESULT_RECLASSIFICATION.csv missing"

    trace_file = os.path.join(RESEARCH_DIR, "PHASE_ACR_EXECUTION_TRACE.md")
    assert os.path.exists(trace_file), "PHASE_ACR_EXECUTION_TRACE.md missing"

    report_file = os.path.join(RESEARCH_DIR, "PHASE_ACR_FINAL_REPORT.md")
    assert os.path.exists(report_file), "PHASE_ACR_FINAL_REPORT.md missing"

    # 2. Verify 18 audit reports in AUDIT/PHASE_ACR/
    audit_files = [
        "00_BACKEND_IDENTITY.md", "01_PROVIDER_IDENTITY.md", "02_RUNTIME_OBJECT_TYPES.md",
        "03_SIMULATOR_DETECTION.md", "04_SHERBROOKE_STATUS.md", "05_EXECUTION_CALL_TRACE.md",
        "06_JOB_ID_VERIFICATION.md", "07_RAW_RESULT_VERIFICATION.md", "08_CALIBRATION_AUTHENTICITY.md",
        "09_PHYSICAL_QUBIT_VERIFICATION.md", "10_TRANSPILATION_VERIFICATION.md", "11_HARDWARE_ENGINE_AUDIT.md",
        "12_FALLBACK_AUDIT.md", "13_22_JOB_AUTHENTICITY.md", "14_RESULT_RECLASSIFICATION.md",
        "15_SECURITY.md", "16_PRODUCTION_INTEGRITY.md", "17_FINAL_ACR_CERTIFICATION.md"
    ]

    for af in audit_files:
        path = os.path.join(AUDIT_DIR, af)
        assert os.path.exists(path), f"Audit report missing: {af}"
