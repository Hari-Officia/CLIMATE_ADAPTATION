"""
Strategy Candidate Service — Phase I
Generates optimization-ready candidate sets (StrategyCandidateSet) for downstream classical and quantum optimization.
"""

import os
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime
from backend.db.database import get_db_context
from backend.db.models import StrategyCandidateSetRecord, StrategyCandidateRecord, PriorityProfileRecord
from backend.services.strategy_applicability_service import StrategyApplicabilityService

class StrategyCandidateService:
    def __init__(self):
        self.applicability_service = StrategyApplicabilityService()

    def generate_candidate_set(self, district_id: str) -> Dict[str, Any]:
        """
        Generate immutable optimization-ready StrategyCandidateSet for a given district.
        """
        district_id = district_id.lower()
        evaluations = self.applicability_service.evaluate_all_strategies_for_district(district_id)

        strategy_ids = []
        excluded_strategy_ids = []
        review_required_strategy_ids = []
        insufficient_data_strategy_ids = []

        for eval_res in evaluations:
            strat_id = eval_res["strategy_id"]
            status = eval_res["eligibility_status"]

            if status in ["ELIGIBLE", "CONDITIONALLY_ELIGIBLE"]:
                strategy_ids.append(strat_id)
            elif status in ["INELIGIBLE", "NOT_APPLICABLE"]:
                excluded_strategy_ids.append(strat_id)
            elif status == "REQUIRES_REVIEW":
                review_required_strategy_ids.append(strat_id)
            elif status == "INSUFFICIENT_DATA":
                insufficient_data_strategy_ids.append(strat_id)

        # Retrieve Priority Profile ID if available
        priority_id = f"PRIO-{district_id.upper()}-AUTO"
        with get_db_context() as db:
            prio_rec = db.query(PriorityProfileRecord).filter(PriorityProfileRecord.district_id == district_id).first()
            if prio_rec:
                priority_id = prio_rec.priority_id

        candidate_set_id = f"CNDSET-{district_id.upper()}-{uuid.uuid4().hex[:8]}"
        evidence_summary = f"{len(strategy_ids)} candidate strategies eligible, {len(excluded_strategy_ids)} excluded, {len(review_required_strategy_ids)} requiring review."
        generated_at = datetime.utcnow().isoformat()

        candidate_set_payload = {
            "candidate_set_id": candidate_set_id,
            "district_id": district_id,
            "priority_id": priority_id,
            "hazard_ids": ["HAZ-FLD", "HAZ-HTW", "HAZ-DRG"],
            "strategy_ids": strategy_ids,
            "excluded_strategy_ids": excluded_strategy_ids,
            "review_required_strategy_ids": review_required_strategy_ids,
            "insufficient_data_strategy_ids": insufficient_data_strategy_ids,
            "evidence_summary": evidence_summary,
            "version": "1.0.0",
            "generated_at": generated_at
        }

        # Store in PostgreSQL database for immutability & traceability
        with get_db_context() as db:
            set_rec = StrategyCandidateSetRecord(
                candidate_set_id=candidate_set_id,
                district_id=district_id,
                priority_id=priority_id,
                hazard_ids=candidate_set_payload["hazard_ids"],
                strategy_ids=strategy_ids,
                excluded_strategy_ids=excluded_strategy_ids,
                review_required_strategy_ids=review_required_strategy_ids,
                insufficient_data_strategy_ids=insufficient_data_strategy_ids,
                evidence_summary=evidence_summary,
                version="1.0.0",
                generated_at=datetime.utcnow()
            )
            db.add(set_rec)
            db.flush()

            for sid in strategy_ids:
                cand_rec = StrategyCandidateRecord(
                    candidate_id=f"CAND-{uuid.uuid4().hex[:8]}",
                    candidate_set_id=candidate_set_id,
                    strategy_id=sid,
                    eligibility_status="ELIGIBLE"
                )
                db.add(cand_rec)
            db.commit()

        return candidate_set_payload
