import os
import json
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_MASTER_DIR = BASE_DIR / "config" / "master"
SCHEMAS_DIR = BASE_DIR / "schemas"

def test_canonical_districts_registry():
    path = CONFIG_MASTER_DIR / "districts.json"
    assert path.exists(), "Master districts registry must exist"
    with open(path, "r", encoding="utf-8") as f:
        districts = json.load(f)
    assert len(districts) == 38, f"Expected 38 districts, found {len(districts)}"
    
    canonical_ids = [d["canonical_district_id"] for d in districts]
    assert len(set(canonical_ids)) == 38, "Canonical district IDs must be unique"
    for cid in canonical_ids:
        assert cid.startswith("DIST-TN-"), f"Invalid ID format: {cid}"

def test_canonical_hazards_registry():
    path = CONFIG_MASTER_DIR / "hazards.json"
    assert path.exists(), "Master hazards registry must exist"
    with open(path, "r", encoding="utf-8") as f:
        hazards = json.load(f)
    hazard_ids = [h["hazard_id"] for h in hazards]
    assert "HAZ-FLD" in hazard_ids
    assert "HAZ-DRG" in hazard_ids
    assert "HAZ-HTW" in hazard_ids

def test_canonical_feature_contract():
    path = CONFIG_MASTER_DIR / "feature_contracts.json"
    assert path.exists(), "Feature contract registry must exist"
    with open(path, "r", encoding="utf-8") as f:
        fct = json.load(f)
    assert fct["feature_contract_id"] == "FCT-53-001"
    assert fct["total_features"] == 53
    assert len(fct["continuous_features"]) == 15
    assert len(fct["district_onehot_features"]) == 38

def test_canonical_models_registry():
    path = CONFIG_MASTER_DIR / "models.json"
    assert path.exists(), "Models registry must exist"
    with open(path, "r", encoding="utf-8") as f:
        models = json.load(f)
    for m in models:
        assert m["feature_contract_id"] == "FCT-53-001"
        assert m["status"] == "ACTIVE"

def test_immutable_snapshot_integrity():
    snapshot_dir = BASE_DIR / "knowledge_base" / "v1.0.0_verified"
    assert snapshot_dir.exists(), "Verified snapshot v1.0.0_verified must exist"
    version_file = BASE_DIR / "KNOWLEDGE_BASE_VERSION.md"
    assert version_file.exists(), "KNOWLEDGE_BASE_VERSION.md must exist"

def test_rev001_guardrail():
    queue_file = BASE_DIR / "AUDIT" / "21_REVIEW_QUEUE.csv"
    assert queue_file.exists(), "Review queue must exist"
    with open(queue_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "REV-001" in content, "REV-001 must remain in review queue"
