"""
Test Suite: Quarterly Scientific Review & Research Governance
Verifies baseline immutability manifest, quarterly review engine, schedule, NCR management system (NC-001, NC-002),
evidence conflict engine, change management gates, decision diff engine, and 38-district regression.
"""
import json
import pytest
from pathlib import Path

from lifecycle.quarterly_review.review_scope import get_review_scope
from lifecycle.quarterly_review.review_scheduler import get_schedule
from lifecycle.non_conformities.ncr_engine import NCREngine
from lifecycle.evidence_review.conflict_engine import ConflictEngine
from lifecycle.change_management.change_engine import ChangeEngine
from lifecycle.decision_diff.decision_diff_engine import DecisionDiffEngine
from scripts.run_quarterly_review import run_quarterly_review

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_q01_baseline_manifest_integrity():
    manifest_path = PROJECT_ROOT / "lifecycle" / "baselines" / "BASE-3.0.0-20260923" / "baseline_manifest.json"
    assert manifest_path.exists()
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["baseline_id"] == "BASE-3.0.0-20260923"
        assert data["release"] == "3.0.0-certified"
        assert "artifact_hashes" in data

def test_q02_quarterly_review_schedule():
    schedule = get_schedule()
    assert schedule["next_quarterly_review"] == "2026-12-23"
    assert schedule["annual_recertification"] == "2027-09-23"

def test_q03_review_scope_domains():
    scope = get_review_scope()
    assert scope["domain_count"] == 48

def test_q04_ncr_engine():
    engine = NCREngine()
    ncrs = engine.list_ncr()
    assert len(ncrs) >= 2
    nc_ids = {nc["nc_id"] for nc in ncrs}
    assert "NC-001" in nc_ids
    assert "NC-002" in nc_ids
    
    accepted = engine.get_accepted_risks()
    assert len(accepted) >= 2

def test_q05_evidence_conflict_engine():
    engine = ConflictEngine()
    res = engine.detect_conflicts()
    assert "hierarchy_policy" in res
    assert res["hierarchy_policy"] == "Tier 1 strictly overrides lower tiers"

def test_q06_change_management_gates():
    engine = ChangeEngine()
    assert engine.requires_scientific_review("CLASS 7: Scientific methodology change") is True
    assert engine.requires_scientific_review("CLASS 1: Non-functional maintenance") is False

def test_q07_decision_diff_engine():
    sample1 = {"district_id": "chennai", "risk_score": 0.8, "provenance": {"context_hash": "hash1"}}
    sample2 = {"district_id": "chennai", "risk_score": 0.8, "provenance": {"context_hash": "hash1"}}
    diff = DecisionDiffEngine.compute_diff(sample1, sample2)
    assert diff["is_identical"] is True
    assert diff["risk_score_delta"] == 0.0

def test_q08_research_gap_registry():
    gap_path = PROJECT_ROOT / "research" / "gaps" / "research_gap_registry.json"
    assert gap_path.exists()
    with open(gap_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data["research_gaps"]) >= 3

def test_q09_full_quarterly_review_runner():
    payload = run_quarterly_review()
    assert payload["final_decision"] == "QUARTERLY_REVIEW_CONDITIONALLY_HEALTHY"
    assert payload["baseline"] == "BASE-3.0.0-20260923"
    assert payload["release"] == "3.0.0-certified"
    assert payload["district_status"] == "38/38_VERIFIED"
    
    # Check quarterly review status file
    status_file = PROJECT_ROOT / "AUDIT" / "QUARTERLY_REVIEW" / "quarterly_review_status.json"
    assert status_file.exists()
    
    # Check 36 markdown reports
    audit_files = list((PROJECT_ROOT / "AUDIT" / "QUARTERLY_REVIEW").glob("*.md"))
    assert len(audit_files) >= 36
