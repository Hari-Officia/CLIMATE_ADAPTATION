"""
Strategy Applicability Service — Phase I
Evaluates adaptation strategy applicability per district based on physical context, hazard risk, exposure, vulnerability, and explicit hard/soft conditions.
"""

import os
import json
from typing import Dict, Any, List
from datetime import datetime
from backend.db.database import get_db_context
from backend.db.models import DistrictProfile, StrategyRecord, StrategyConditionRecord

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config", "master")

class StrategyApplicabilityService:
    def __init__(self):
        self.strategies = self._load_json("strategies.json")
        self.domains = self._load_json("strategy_domains.json")
        self.conditions = self._load_json("strategy_conditions.json")

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        path = os.path.join(CONFIG_DIR, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def evaluate_strategy_applicability(self, district_id: str, strategy_id: str, hazard_id: str = None) -> Dict[str, Any]:
        """
        Evaluate single strategy applicability for a given district.
        """
        strategy = next((s for s in self.strategies if s["strategy_id"] == strategy_id), None)
        if not strategy:
            return {
                "strategy_id": strategy_id,
                "district_id": district_id,
                "hazard_id": hazard_id or "UNKNOWN",
                "applicable": False,
                "eligibility_status": "NOT_APPLICABLE",
                "satisfied_conditions": [],
                "failed_conditions": ["UNKNOWN_STRATEGY_ID"],
                "missing_data": [],
                "reasons": ["Strategy ID not found in master registry."],
                "evaluated_at": datetime.utcnow().isoformat()
            }

        # Check district profile
        district_context = self._get_district_context(district_id)
        if not district_context:
            return {
                "strategy_id": strategy_id,
                "district_id": district_id,
                "hazard_id": hazard_id or strategy.get("primary_hazard_id", "HAZ-FLD"),
                "applicable": False,
                "eligibility_status": "INSUFFICIENT_DATA",
                "satisfied_conditions": [],
                "failed_conditions": [],
                "missing_data": ["DISTRICT_PROFILE_RECORD"],
                "reasons": ["District profile record unavailable in database."],
                "evaluated_at": datetime.utcnow().isoformat()
            }

        satisfied_conditions = []
        failed_conditions = []
        missing_data = []
        reasons = []

        # Evaluate conditions specific to strategy
        strat_conditions = [c for c in self.conditions if c["strategy_id"] == strategy_id]
        
        # Default coastal hard check for coastal strategies
        is_coastal_strategy = strategy["domain_id"] == "DOM-CST" or strategy_id == "STR-CST-001"
        is_district_coastal = district_context.get("coastal", False)

        if is_coastal_strategy and not is_district_coastal:
            failed_conditions.append("CND-CST-001: Coastal Exposure Required")
            reasons.append(f"District {district_id} lacks coastal/marine shoreline exposure.")
        elif is_coastal_strategy and is_district_coastal:
            satisfied_conditions.append("CND-CST-001: Coastal Exposure Satisfied")

        # Evaluate other registered conditions
        for cond in strat_conditions:
            cond_id = cond["condition_id"]
            feat_name = cond["feature_name"]
            req_val = cond.get("required_value")
            
            if feat_name == "coastal":
                continue # handled above
            elif feat_name == "population":
                pop = district_context.get("population", 0)
                thresh = cond.get("threshold", 0)
                if pop >= thresh:
                    satisfied_conditions.append(f"{cond_id}: Population Threshold ({pop} >= {thresh})")
                else:
                    failed_conditions.append(f"{cond_id}: Population Below Threshold ({pop} < {thresh})")
                    reasons.append(f"District population ({pop}) below recommended applicability threshold ({thresh}).")

        # Status assignment
        if "CND-CST-001: Coastal Exposure Required" in failed_conditions:
            eligibility_status = "INELIGIBLE"
            applicable = False
        elif strategy.get("evidence_status") in ["REQUIRES_REVIEW", "PARTIALLY_VERIFIED"]:
            eligibility_status = "REQUIRES_REVIEW"
            applicable = True
            reasons.append("Strategy flagged for scientific peer-review.")
        else:
            eligibility_status = "ELIGIBLE"
            applicable = True
            reasons.append("All primary technical and spatial applicability criteria satisfied.")

        return {
            "strategy_id": strategy_id,
            "district_id": district_id,
            "hazard_id": hazard_id or strategy.get("primary_hazard_id", "HAZ-FLD"),
            "applicable": applicable,
            "eligibility_status": eligibility_status,
            "satisfied_conditions": satisfied_conditions,
            "failed_conditions": failed_conditions,
            "missing_data": missing_data,
            "reasons": reasons,
            "evaluated_at": datetime.utcnow().isoformat()
        }

    def _get_district_context(self, district_id: str) -> Dict[str, Any]:
        with get_db_context() as db:
            profile = db.query(DistrictProfile).filter(DistrictProfile.district_id == district_id.lower()).first()
            if profile:
                return {
                    "district_id": profile.district_id,
                    "district_name": profile.district_name,
                    "population": profile.population,
                    "area_km2": profile.area_km2,
                    "population_density": profile.population_density,
                    "urban_percentage": profile.urban_percentage,
                    "coastal": profile.coastal,
                    "elevation_m": profile.elevation_m
                }
            return None

    def evaluate_all_strategies_for_district(self, district_id: str) -> List[Dict[str, Any]]:
        results = []
        for strategy in self.strategies:
            res = self.evaluate_strategy_applicability(district_id, strategy["strategy_id"])
            results.append(res)
        return results
