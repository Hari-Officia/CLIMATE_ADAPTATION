"""
Workflow State & Checkpoint Manager (Phase O)
Manages the canonical state object of a decision workflow:
- Tracks stage execution history, timestamps, and stage statuses
- Creates immutable stage output snapshots
- Manages workflow checkpointing and staleness propagation
"""

import hashlib
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class DecisionWorkflowState:
    def __init__(
        self,
        request_id: str,
        workflow_id: str,
        decision_id: str,
        district_id: str,
        hazard_ids: Optional[List[str]] = None,
        optimization_mode: str = "CLASSICAL"
    ):
        self.request_id = request_id
        self.workflow_id = workflow_id
        self.decision_id = decision_id
        self.district_id = district_id
        self.hazard_ids = hazard_ids or ["coastal_flooding", "urban_heat", "drought"]
        self.optimization_mode = optimization_mode

        self.status = "RUNNING"
        self.current_stage = "DISTRICT_RESOLUTION"
        self.stage_history = []
        self.checkpoints = {}
        self.errors = []
        self.warnings = []

        # Stage Outputs
        self.district_context = {}
        self.climate_context = {}
        self.risk_context = {}
        self.exposure_context = {}
        self.vulnerability_context = {}
        self.resilience_context = {}
        self.priority_context = {}
        self.strategy_candidates = []
        self.classical_optimization_result = {}
        self.qubo_result = {}
        self.qaoa_result = {}
        self.portfolio_validation = {}
        self.evidence_packet = {}
        self.explanation = {}

        self.context_hash = ""
        self.evidence_packet_hash = ""
        self.created_at = datetime.utcnow().isoformat()
        self.completed_at = None

    def start_stage(self, stage_name: str):
        self.current_stage = stage_name
        self.stage_history.append({
            "stage": stage_name,
            "status": "RUNNING",
            "start_time": time.time()
        })

    def complete_stage(self, stage_name: str, output_data: Dict[str, Any]):
        end_time = time.time()
        for s in self.stage_history:
            if s["stage"] == stage_name and s["status"] == "RUNNING":
                s["status"] = "COMPLETED"
                s["end_time"] = end_time
                s["duration_ms"] = round((end_time - s["start_time"]) * 1000, 2)
                break

        # Save checkpoint
        self.checkpoints[stage_name] = {
            "timestamp": datetime.utcnow().isoformat(),
            "output_hash": hashlib.sha256(json.dumps(output_data, sort_keys=True, default=str).encode("utf-8")).hexdigest()
        }

    def fail_stage(self, stage_name: str, error_message: str):
        end_time = time.time()
        for s in self.stage_history:
            if s["stage"] == stage_name and s["status"] == "RUNNING":
                s["status"] = "FAILED"
                s["end_time"] = end_time
                s["duration_ms"] = round((end_time - s["start_time"]) * 1000, 2)
                s["error"] = error_message
                break
        self.errors.append({"stage": stage_name, "message": error_message})
        self.status = "FAILED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "workflow_id": self.workflow_id,
            "decision_id": self.decision_id,
            "district_id": self.district_id,
            "status": self.status,
            "current_stage": self.current_stage,
            "stage_history": self.stage_history,
            "errors": self.errors,
            "warnings": self.warnings,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
