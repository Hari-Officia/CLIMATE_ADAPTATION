"""
RAG API Router (Phase N)
Provides REST endpoints for evidence retrieval, document provenance, source registry inspection, and claim verification.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from backend.services.rag.hybrid_retriever import HybridRetriever
from backend.services.rag.evidence_linker import EvidenceLinker

router = APIRouter(prefix="/api/v1/rag", tags=["RAG Evidence Intelligence"])

retriever = HybridRetriever()
evidence_linker = EvidenceLinker()

class RAGSearchRequest(BaseModel):
    query: str
    district_id: Optional[str] = None
    hazard_ids: Optional[List[str]] = None
    strategy_ids: Optional[List[str]] = None
    top_k: int = 5

@router.post("/search")
def search_evidence(req: RAGSearchRequest):
    try:
        return retriever.retrieve(
            query=req.query,
            district_id=req.district_id,
            hazard_ids=req.hazard_ids,
            strategy_ids=req.strategy_ids,
            top_k=req.top_k
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/source/{source_id}")
def get_source_details(source_id: str):
    source = retriever.sources.get(source_id)
    if not source:
        raise HTTPException(status_code=404, detail=f"Source ID '{source_id}' not found in source registry.")
    return source

@router.get("/document/{document_id}")
def get_document_details(document_id: str):
    doc = retriever.documents.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document ID '{document_id}' not found in document registry.")
    return doc

@router.get("/strategies/{strategy_id}/evidence")
def get_strategy_evidence(strategy_id: str):
    return {
        "strategy_id": strategy_id,
        "evidence_claims": evidence_linker.get_strategy_evidence(strategy_id)
    }
