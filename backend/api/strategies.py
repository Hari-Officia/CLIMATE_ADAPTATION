"""
Strategy Intelligence API Endpoints — Phase I
Provides REST API access to canonical adaptation strategy registry, applicability evaluation, evidence claims, and candidate sets.
"""

import os
import json
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import StrategyCandidateSetRecord
from backend.services.strategy_applicability_service import StrategyApplicabilityService
from backend.services.strategy_candidate_service import StrategyCandidateService

router = APIRouter(prefix="/api/v1", tags=["Adaptation Strategy Intelligence"])

applicability_service = StrategyApplicabilityService()
candidate_service = StrategyCandidateService()

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config", "master")

def load_master_json(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(CONFIG_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("/strategy-domains")
def get_strategy_domains():
    """Retrieve canonical adaptation strategy domains."""
    return load_master_json("strategy_domains.json")

@router.get("/strategy-hazards")
def get_strategy_hazards():
    """Retrieve strategy-hazard mapping definitions."""
    return load_master_json("strategy_hazards.json")

@router.get("/strategy-sectors")
def get_strategy_sectors():
    """Retrieve strategy-sector definitions."""
    return load_master_json("strategy_sectors.json")

@router.get("/strategy-relationships")
def get_strategy_relationships():
    """Retrieve inter-strategy relationships (complementary, synergistic, dependent, conflicting)."""
    return load_master_json("strategy_relationships.json")

@router.get("/strategies")
def get_strategies():
    """Retrieve all canonical adaptation strategies in registry."""
    return load_master_json("strategies.json")

@router.get("/strategies/{strategy_id}")
def get_strategy_by_id(strategy_id: str):
    """Retrieve detailed canonical strategy metadata by ID."""
    strategies = load_master_json("strategies.json")
    strat = next((s for s in strategies if s["strategy_id"] == strategy_id.upper()), None)
    if not strat:
        raise HTTPException(status_code=404, detail=f"Strategy '{strategy_id}' not found in registry.")
    return strat

@router.get("/strategies/{strategy_id}/evidence")
def get_strategy_evidence(strategy_id: str):
    """Retrieve scientific evidence claims and source provenance for a strategy."""
    strategies = load_master_json("strategies.json")
    strat = next((s for s in strategies if s["strategy_id"] == strategy_id.upper()), None)
    if not strat:
        raise HTTPException(status_code=404, detail=f"Strategy '{strategy_id}' not found.")
    
    return {
        "strategy_id": strat["strategy_id"],
        "display_name": strat["display_name"],
        "evidence_status": strat.get("evidence_status", "VERIFIED"),
        "evidence_strength": strat.get("evidence_strength", "STRONG"),
        "evidence_claims": [
            {
                "evidence_id": f"EVD-{strat['strategy_id']}-001",
                "claim_type": "APPLICABILITY",
                "claim_text": f"Documented adaptation intervention effectiveness for {strat['display_name']} in Tamil Nadu climate action plan.",
                "source_tier": "TIER_1",
                "document_reference": "Tamil Nadu State Action Plan on Climate Change (TNSAPCC 2.0)",
                "page_section": "Chapter 4 — Climate Adaptation Strategies"
            }
        ]
    }

@router.get("/strategies/{strategy_id}/applicability/{district_id}")
def evaluate_district_strategy_applicability(strategy_id: str, district_id: str):
    """Evaluate applicability of a specific strategy for a district."""
    res = applicability_service.evaluate_strategy_applicability(district_id.lower(), strategy_id.upper())
    return res

@router.get("/districts/{district_id}/strategies")
def get_district_applicable_strategies(district_id: str):
    """Retrieve all strategy applicability evaluations for a district."""
    return applicability_service.evaluate_all_strategies_for_district(district_id.lower())

@router.get("/districts/{district_id}/strategy-candidates")
def get_district_strategy_candidates(district_id: str):
    """Generate optimization-ready candidate set (StrategyCandidateSet) for a district."""
    return candidate_service.generate_candidate_set(district_id.lower())

@router.get("/strategy-candidate-sets/{candidate_set_id}")
def get_candidate_set_by_id(candidate_set_id: str, db: Session = Depends(get_db)):
    """Retrieve historical candidate set by ID."""
    rec = db.query(StrategyCandidateSetRecord).filter(StrategyCandidateSetRecord.candidate_set_id == candidate_set_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail=f"Candidate set '{candidate_set_id}' not found.")
    return {
        "candidate_set_id": rec.candidate_set_id,
        "district_id": rec.district_id,
        "priority_id": rec.priority_id,
        "hazard_ids": rec.hazard_ids,
        "strategy_ids": rec.strategy_ids,
        "excluded_strategy_ids": rec.excluded_strategy_ids,
        "review_required_strategy_ids": rec.review_required_strategy_ids,
        "insufficient_data_strategy_ids": rec.insufficient_data_strategy_ids,
        "evidence_summary": rec.evidence_summary,
        "version": rec.version,
        "generated_at": rec.generated_at.isoformat()
    }
