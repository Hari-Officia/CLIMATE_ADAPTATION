# Phase N to Phase O Contract Specification

**Phase N:** Enterprise Retrieval-Augmented Generation (RAG) & Decision Explanation Engine  
**Phase O Target:** Enterprise Decision Intelligence API, Multi-Agent Orchestration & Production Hardening  

---

## 1. Overview

This contract establishes the formal handoff specification between the Phase N Evidence-Grounded Decision Explanation Engine and the upstream Phase O Multi-Agent Orchestrator.

Phase O will request district decision support explanations by invoking `/api/v1/explanation/generate` or using internal Python service functions `generate_district_explanation(district_id)`.

---

## 2. API Handoff Interface

### Request Payload (`POST /api/v1/explanation/generate`)
```json
{
  "district_id": "chennai",
  "hazard_ids": ["coastal_flooding", "urban_heat"],
  "strategy_ids": ["STR-NBS-001", "STR-URB-001"],
  "optimization_result_id": "OPT-CHE-MILP-001",
  "qaoa_experiment_id": "EXP-QAOA-CHE-001",
  "evidence_mode": "STRICT_GROUNDED",
  "detail_level": "FULL"
}
```

### Response Payload (`200 OK`)
```json
{
  "request_id": "REQ-EXP-CHE-001",
  "explanation_id": "EXP-CHE-20260923-001",
  "district_id": "chennai",
  "district_name": "Chennai",
  "strategy_ids": ["STR-NBS-001", "STR-URB-001"],
  "optimization_id": "OPT-CHE-MILP-001",
  "evidence_packet_hash": "a8f9c2d1e3f4b5a678901234567890abcdef1234567890abcdef1234567890ab",
  "context_hash": "c7a8b9d0e1f2a3b45678901234567890abcdef1234567890abcdef1234567890",
  "model": "climate-adaptation-explainer-v1",
  "prompt_version": "1.0.0",
  "retrieval_version": "1.0.0",
  "knowledge_base_version": "v1.0.0_verified",
  "decision_summary": "Selected portfolio of 2 climate adaptation strategies for Chennai based on exact MILP solver outputs and grounded evidence.",
  "selected_strategies": [
    {
      "strategy_id": "STR-NBS-001",
      "name": "Coastal Wetland and Mangrove Restoration",
      "selection_reason": "Selected by MILP optimizer to maximize flood attenuation.",
      "evidence_status": "SUPPORTED",
      "citation_ids": ["CIT-TN-CAP-003-045"]
    }
  ],
  "optimization_explanation": {
    "solver_type": "MILP_EXACT",
    "objective_description": "Maximizing cumulative adaptation benefit.",
    "qaoa_experiment_id": "EXP-QAOA-CHE-001",
    "qaoa_p_depth": 2,
    "qaoa_feasibility_probability": 0.689,
    "objective_gap": 0.470,
    "quantum_advantage_claimed": false
  },
  "evidence": [
    {
      "claim_id": "CLM-TN-CAP-003-012",
      "text": "Restoration of urban wetlands and coastal mangroves enhances natural flood attenuation capacity.",
      "citation_id": "CIT-TN-CAP-003-045"
    }
  ],
  "citations": [
    {
      "citation_id": "CIT-TN-CAP-003-045",
      "source_id": "TN-CAP-003",
      "document_id": "DOC-TN-CAP-003",
      "chunk_id": "CHK-TN-CAP-003-045",
      "title": "Chennai Climate Action Plan (CCAP) 2050",
      "organization": "Greater Chennai Corporation",
      "year": 2023,
      "page": 42,
      "section": "4.2 Flood Attenuation",
      "source_tier": "Tier 1"
    }
  ],
  "uncertainties": ["Data uncertainty regarding extreme sea-level rise."],
  "limitations": ["Applicable only to coastal wetlands."],
  "conflicts": [],
  "validation_status": "VERIFIED"
}
```

---

## 3. Invariants & Phase O Guarantee
1. **Canonical Traceability:** Every response preserves `context_hash`, `evidence_packet_hash`, `knowledge_base_version`, and canonical IDs.
2. **Zero Injected Decision Logic:** Phase O agents can rely on `selected_strategies` as exact outputs from Phase J/K/M without fearing LLM hallucination.
