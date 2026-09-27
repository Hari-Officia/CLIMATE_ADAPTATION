"""
QUBO API Router — Phase L Classical-to-Quantum Mathematical Bridge
Exposes REST endpoints for QUBO model building, variable mapping retrieval, matrix export, equivalence validation, certificates, and district QUBO queries.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from backend.db.database import get_db_context
from backend.db.models import (
    QUBOModelRecord, QUBOVariableRecord, QUBOTermRecord,
    QUBOConstraintRecord, QUBOPenaltyRecord, QUBOCertificateRecord
)
from backend.services.optimization.qubo_builder import QUBOBuilder
from backend.services.optimization.qubo_equivalence_validator import QUBOEquivalenceValidator

qubo_router = APIRouter(tags=["QUBO Optimization Bridge"])

class QUBOBuildRequest(BaseModel):
    district_id: str = Field(..., json_schema_extra={"example": "chennai"})
    max_k: int = Field(5, ge=1, le=15, json_schema_extra={"example": 5})
    scenario_id: str = Field("BASELINE", json_schema_extra={"example": "BASELINE"})

class QUBOValidationRequest(BaseModel):
    district_id: str = Field(..., json_schema_extra={"example": "chennai"})
    max_k: int = Field(5, ge=1, le=15, json_schema_extra={"example": 5})

@qubo_router.post("/build", summary="Build QUBO Model for District")
def build_qubo_model(payload: QUBOBuildRequest):
    """Build exact QUBO model from Phase J/K classical strategy optimization instance."""
    builder = QUBOBuilder()
    try:
        model = builder.build_qubo(district_id=payload.district_id, max_k=payload.max_k, persist=True)
        return model
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"QUBO build failed: {str(e)}")

@qubo_router.post("/validate", summary="Validate Classical-to-QUBO Equivalence")
def validate_qubo(payload: QUBOValidationRequest):
    """Exhaustively validate bitwise equivalence between classical ground truth and QUBO energy global minimum."""
    validator = QUBOEquivalenceValidator()
    try:
        result = validator.validate_qubo_equivalence(district_id=payload.district_id, max_k=payload.max_k, persist=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"QUBO validation failed: {str(e)}")

@qubo_router.get("/{qubo_id}", summary="Get QUBO Model Details")
def get_qubo_model(qubo_id: str = Path(..., json_schema_extra={"example": "QUBO-CHENNAI-10a477d2"})):

    with get_db_context() as db:
        model = db.query(QUBOModelRecord).filter_by(qubo_id=qubo_id).first()
        if not model:
            raise HTTPException(status_code=404, detail=f"QUBO model '{qubo_id}' not found.")
        
        return {
            "qubo_id": model.qubo_id,
            "district_id": model.district_id,
            "candidate_set_id": model.candidate_set_id,
            "classical_model_hash": model.classical_model_hash,
            "qubo_hash": model.qubo_hash,
            "methodology_id": model.methodology_id,
            "candidate_variable_count": model.candidate_variable_count,
            "slack_variable_count": model.slack_variable_count,
            "total_variable_count": model.total_variable_count,
            "linear_term_count": model.linear_term_count,
            "quadratic_term_count": model.quadratic_term_count,
            "constant_offset": model.constant_offset,
            "status": model.status,
            "created_at": model.created_at.isoformat() if model.created_at else None
        }

@qubo_router.get("/{qubo_id}/matrix", summary="Get QUBO Matrix Representation")
def get_qubo_matrix(qubo_id: str = Path(...)):
    with get_db_context() as db:
        model = db.query(QUBOModelRecord).filter_by(qubo_id=qubo_id).first()
        if not model:
            raise HTTPException(status_code=404, detail=f"QUBO model '{qubo_id}' not found.")
        
        terms = db.query(QUBOTermRecord).filter_by(qubo_id=qubo_id).all()
        linear_terms = {}
        quadratic_terms = {}
        
        for t in terms:
            if t.term_type == "LINEAR":
                linear_terms[str(t.variable_i)] = t.coefficient
            else:
                quadratic_terms[f"{t.variable_i},{t.variable_j}"] = t.coefficient

        return {
            "qubo_id": qubo_id,
            "qubo_hash": model.qubo_hash,
            "dimension": model.total_variable_count,
            "constant_offset": model.constant_offset,
            "linear_terms": linear_terms,
            "quadratic_terms": quadratic_terms
        }

@qubo_router.get("/{qubo_id}/variables", summary="Get QUBO Variable Mappings")
def get_qubo_variables(qubo_id: str = Path(...)):
    with get_db_context() as db:
        vars_list = db.query(QUBOVariableRecord).filter_by(qubo_id=qubo_id).order_by(QUBOVariableRecord.index.asc()).all()
        if not vars_list:
            raise HTTPException(status_code=404, detail=f"No variables found for QUBO model '{qubo_id}'.")
        
        return [
            {
                "index": v.index,
                "variable_name": v.variable_name,
                "variable_type": v.variable_type,
                "candidate_id": v.candidate_id,
                "strategy_id": v.strategy_id,
                "slack_constraint_id": v.slack_constraint_id,
                "slack_bit": v.slack_bit,
                "meaning": v.meaning
            } for v in vars_list
        ]

@qubo_router.get("/{qubo_id}/constraints", summary="Get QUBO Constraints & Penalties")
def get_qubo_constraints(qubo_id: str = Path(...)):
    with get_db_context() as db:
        constraints = db.query(QUBOConstraintRecord).filter_by(qubo_id=qubo_id).all()
        return [
            {
                "constraint_id": c.constraint_id,
                "constraint_type": c.constraint_type,
                "original_expression": c.original_expression,
                "qubo_expression": c.qubo_expression,
                "penalty_value": c.penalty_value,
                "verification_status": c.verification_status
            } for c in constraints
        ]

@qubo_router.get("/{qubo_id}/coefficients", summary="Get QUBO Coefficient Terms Ledger")
def get_qubo_coefficients(qubo_id: str = Path(...)):
    with get_db_context() as db:
        terms = db.query(QUBOTermRecord).filter_by(qubo_id=qubo_id).all()
        return [
            {
                "term_id": t.term_id,
                "variable_i": t.variable_i,
                "variable_j": t.variable_j,
                "term_type": t.term_type,
                "coefficient": t.coefficient,
                "provenance": t.provenance
            } for t in terms
        ]

@qubo_router.get("/{qubo_id}/certificate", summary="Get QUBO Equivalence Certificate")
def get_qubo_certificate(qubo_id: str = Path(...)):
    with get_db_context() as db:
        cert = db.query(QUBOCertificateRecord).filter_by(qubo_id=qubo_id).first()
        if not cert:
            raise HTTPException(status_code=404, detail=f"Certificate for QUBO '{qubo_id}' not found.")
        
        return {
            "certificate_id": cert.certificate_id,
            "qubo_id": cert.qubo_id,
            "district_id": cert.district_id,
            "classical_model_hash": cert.classical_model_hash,
            "qubo_hash": cert.qubo_hash,
            "candidate_set_version": cert.candidate_set_version,
            "variable_count": cert.variable_count,
            "tested_state_count": cert.tested_state_count,
            "classical_optimum": cert.classical_optimum,
            "qubo_optimum": cert.qubo_optimum,
            "decoded_objective": cert.decoded_objective,
            "objective_difference": cert.objective_difference,
            "feasibility_match": cert.feasibility_match,
            "optimality_match": cert.optimality_match,
            "status": cert.status,
            "created_at": cert.created_at.isoformat() if cert.created_at else None
        }
