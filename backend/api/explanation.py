"""
Decision Explanation API Router (Phase N)
Provides REST endpoints for evidence-grounded decision explanation generation and output validation.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from backend.services.explanation.llm_explanation_engine import LLMExplanationEngine

router = APIRouter(prefix="/api/v1/explanation", tags=["Decision Intelligence Explanation"])

engine = LLMExplanationEngine()

class ExplanationRequest(BaseModel):
    district_id: str
    query: Optional[str] = None
    evidence_mode: str = "STRICT_GROUNDED"
    detail_level: str = "FULL"

@router.post("/generate")
def generate_explanation(req: ExplanationRequest):
    try:
        res = engine.generate_explanation(req.district_id, req.query)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{district_id}")
def get_district_explanation(district_id: str):
    try:
        return engine.generate_explanation(district_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
