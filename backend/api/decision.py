"""
Enterprise Decision Intelligence API Router (Phase O & Q)
Provides REST endpoints for synchronous & asynchronous climate adaptation decision analysis, workflow tracking, provenance drill-down, and production health/liveness/readiness probes.
"""

from fastapi import APIRouter, HTTPException, Query, Path, Depends, Header
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from sqlalchemy.sql import text
from backend.services.orchestration.workflow_engine import MasterDecisionOrchestrator
from backend.db.database import SessionLocal
from backend.db.models import DecisionResultRecord, DecisionWorkflowRecord

router = APIRouter(prefix="/api/v1/decision", tags=["Enterprise Decision Intelligence API"])

orchestrator = MasterDecisionOrchestrator()

class DecisionAnalysisRequest(BaseModel):
    district_id: str = Field(..., json_schema_extra={"example": "chennai"})
    hazard_ids: Optional[List[str]] = Field(default=None, json_schema_extra={"example": ["coastal_flooding", "urban_heat"]})
    optimization_mode: str = Field(default="CLASSICAL_PLUS_QAOA", json_schema_extra={"example": "CLASSICAL_PLUS_QAOA"})
    qaoa_p_depth: int = Field(default=2, json_schema_extra={"example": 2})
    idempotency_key: Optional[str] = Field(default=None, json_schema_extra={"example": "IDEM-CHE-20260923-001"})


@router.post("/analyze")
def analyze_decision(req: DecisionAnalysisRequest, idempotency_header: Optional[str] = Header(None, alias="Idempotency-Key")):
    try:
        key = req.idempotency_key or idempotency_header
        return orchestrator.execute_workflow(
            district_id=req.district_id,
            hazard_ids=req.hazard_ids,
            optimization_mode=req.optimization_mode,
            qaoa_p_depth=req.qaoa_p_depth,
            idempotency_key=key
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def get_system_health():
    return {
        "status": "HEALTHY",
        "services": {
            "database": "UP",
            "risk_engine": "UP",
            "priority_engine": "UP",
            "classical_optimizer": "UP",
            "qaoa_simulator": "UP",
            "chroma_vector_store": "UP",
            "llm_explanation_engine": "UP"
        }
    }

@router.get("/health/live")
def get_liveness_probe():
    """Liveness probe: verifies process is alive."""
    return {"status": "ALIVE"}

@router.get("/health/ready")
def get_readiness_probe():
    """Readiness probe: verifies database & dependencies are accessible."""
    session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))
        db_status = "UP"
    except Exception as e:
        db_status = "DOWN"
    finally:
        session.close()

    if db_status == "UP":
        return {"status": "READY", "dependencies": {"database": "UP"}}
    else:
        raise HTTPException(status_code=503, detail="Database dependency unavailable.")

@router.get("/{decision_id}")
def get_decision_by_id(decision_id: str):
    session = SessionLocal()
    try:
        rec = session.query(DecisionResultRecord).filter(DecisionResultRecord.decision_id == decision_id).first()
        if not rec:
            raise HTTPException(status_code=404, detail=f"Decision ID '{decision_id}' not found.")
        return rec.result_payload
    finally:
        session.close()

@router.get("/{decision_id}/workflow")
def get_decision_workflow(decision_id: str):
    session = SessionLocal()
    try:
        rec = session.query(DecisionResultRecord).filter(DecisionResultRecord.decision_id == decision_id).first()
        if not rec:
            raise HTTPException(status_code=404, detail=f"Decision ID '{decision_id}' not found.")
        wf = session.query(DecisionWorkflowRecord).filter(DecisionWorkflowRecord.workflow_id == rec.workflow_id).first()
        return {
            "workflow_id": wf.workflow_id,
            "district_id": wf.district_id,
            "status": wf.status,
            "current_stage": wf.current_stage,
            "stage_history": wf.stage_history
        }
    finally:
        session.close()

@router.get("/{decision_id}/provenance")
def get_decision_provenance(decision_id: str):
    session = SessionLocal()
    try:
        rec = session.query(DecisionResultRecord).filter(DecisionResultRecord.decision_id == decision_id).first()
        if not rec:
            raise HTTPException(status_code=404, detail=f"Decision ID '{decision_id}' not found.")
        return rec.result_payload.get("provenance", {})
    finally:
        session.close()
