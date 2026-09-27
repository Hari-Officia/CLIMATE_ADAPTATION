"""
Test Suite: Periodic Re-Certification & Research Governance
Verifies 15 certification dimensions, scientific contracts, assumptions registry, claim matrix,
independent verification scripts, baseline immutability, and 38-district independent reconstruction.
"""
import json
import pytest
from pathlib import Path

from scripts.recertification.verify_scientific_contracts import verify_scientific_contracts
from scripts.recertification.verify_data_contracts import verify_data_contracts
from scripts.recertification.verify_feature_contract import verify_feature_contract
from scripts.recertification.verify_labels import verify_labels
from scripts.recertification.verify_leakage import verify_leakage
from scripts.recertification.verify_temporal_validation import verify_temporal_validation
from scripts.recertification.verify_models import verify_models
from scripts.recertification.verify_gis import verify_gis
from scripts.recertification.verify_exposure import verify_exposure
from scripts.recertification.verify_vulnerability import verify_vulnerability
from scripts.recertification.verify_resilience import verify_resilience
from scripts.recertification.verify_priority import verify_priority
from scripts.recertification.verify_strategies import verify_strategies
from scripts.recertification.verify_evidence import verify_evidence
from scripts.recertification.verify_rag import verify_rag
from scripts.recertification.verify_llm import verify_llm
from scripts.recertification.verify_optimization import verify_optimization
from scripts.recertification.verify_qubo import verify_qubo
from scripts.recertification.verify_qaoa import verify_qaoa
from scripts.recertification.verify_provenance import verify_provenance
from scripts.recertification.verify_reproducibility import verify_reproducibility
from scripts.recertification.verify_security import verify_security
from scripts.recertification.verify_backup_restore import verify_backup_restore
from scripts.recertification.verify_38_districts import verify_38_districts
from scripts.recertification.verify_claims import verify_claims
from scripts.recertification.verify_uncertainty import verify_uncertainty
from scripts.recertification.verify_sensitivity import verify_sensitivity
from scripts.run_periodic_recertification import run_recertification

def test_scientific_contracts_verification():
    res = verify_scientific_contracts()
    assert res["status"] == "PASS"
    assert res["contract_count"] >= 13

def test_data_contracts_verification():
    res = verify_data_contracts()
    assert res["status"] == "PASS"
    assert res["districts_verified"] == 38

def test_feature_contract_verification():
    res = verify_feature_contract()
    assert res["status"] == "PASS"
    assert res["total_features"] == 53

def test_labels_verification():
    res = verify_labels()
    assert res["status"] == "PASS"

def test_leakage_verification():
    res = verify_leakage()
    assert res["status"] == "PASS"
    assert res["target_leakage"] == "CLEAN"

def test_temporal_validation_verification():
    res = verify_temporal_validation()
    assert res["status"] == "PASS"

def test_models_verification():
    res = verify_models()
    assert res["status"] == "PASS"

def test_gis_verification():
    res = verify_gis()
    assert res["status"] == "PASS"

def test_exposure_verification():
    res = verify_exposure()
    assert res["status"] == "PASS"

def test_vulnerability_verification():
    res = verify_vulnerability()
    assert res["status"] == "PASS"

def test_resilience_verification():
    res = verify_resilience()
    assert res["status"] == "PASS"

def test_priority_verification():
    res = verify_priority()
    assert res["status"] == "PASS"

def test_strategies_verification():
    res = verify_strategies()
    assert res["status"] == "PASS"

def test_evidence_verification():
    res = verify_evidence()
    assert res["status"] == "PASS"

def test_rag_verification():
    res = verify_rag()
    assert res["status"] == "PASS"

def test_llm_verification():
    res = verify_llm()
    assert res["status"] == "PASS"

def test_optimization_verification():
    res = verify_optimization()
    assert res["status"] == "PASS"

def test_qubo_verification():
    res = verify_qubo()
    assert res["status"] == "PASS"

def test_qaoa_verification():
    res = verify_qaoa()
    assert res["status"] == "PASS"
    assert res["quantum_advantage"] == "NOT_ESTABLISHED"
    assert res["objective_gap"] == 0.4700

def test_provenance_verification():
    res = verify_provenance()
    assert res["status"] == "PASS"
    assert res["system_versions_count"] >= 8
    assert "context_hash" in res

def test_reproducibility_verification():
    res = verify_reproducibility()
    assert res["status"] == "PASS"
    assert res["reproducibility"] == "100% DETERMINISTIC"

def test_security_verification():
    res = verify_security()
    assert res["status"] == "PASS"

def test_backup_restore_verification():
    res = verify_backup_restore()
    assert res["status"] == "PASS"

def test_38_districts_verification():
    res = verify_38_districts()
    assert res["status"] == "PASS"
    assert res["districts_verified"] == 38

def test_claims_verification():
    res = verify_claims()
    assert res["status"] == "PASS"

def test_uncertainty_verification():
    res = verify_uncertainty()
    assert res["status"] == "PASS"

def test_sensitivity_verification():
    res = verify_sensitivity()
    assert res["status"] == "PASS"

def test_full_periodic_recertification_runner():
    payload = run_recertification()
    assert payload["recertification_status"] == "CONDITIONALLY_RECERTIFIED"
    assert payload["baseline"] == "BASE-3.0.0-20260923"
    assert payload["release"] == "3.0.0-certified"
    assert payload["districts_verified"] == 38
    assert payload["quantum_advantage_established"] is False
    assert len(payload["certification_dimensions"]) == 15
    
    json_path = Path("AUDIT/RECERTIFICATION/final_recertification_status.json")
    assert json_path.exists()
    
    audit_files = list(Path("AUDIT/RECERTIFICATION").glob("*.md"))
    assert len(audit_files) >= 36
