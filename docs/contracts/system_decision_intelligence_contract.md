# System Decision Intelligence Contract

**Project:** Quantum Multi-Agent Decision Support System for Climate Adaptation  
**Phase:** Phase O — Enterprise Decision Intelligence API & Multi-Agent Orchestration  
**Scope:** Climate Adaptation ONLY  
**Geography:** Tamil Nadu, India — All 38 Districts  

---

## 1. Request Contract (`POST /api/v1/decision/analyze`)

```json
{
  "district_id": "chennai",
  "hazard_ids": ["coastal_flooding", "urban_heat"],
  "optimization_mode": "CLASSICAL_PLUS_QAOA",
  "qaoa_p_depth": 2,
  "explanation_mode": "STRICT_GROUNDED",
  "detail_level": "FULL",
  "idempotency_key": "IDEM-CHE-20260923-001"
}
```

---

## 2. Response Contract (`200 OK`)

```json
{
  "decision_id": "DEC-CHE-20260923-001",
  "request_id": "REQ-CHE-20260923-001",
  "workflow_id": "WF-CHE-20260923-001",
  "district_id": "chennai",
  "district_name": "Chennai",
  "risk_score": 0.845,
  "hazard_profile": ["coastal_flooding", "urban_heat", "drought"],
  "priority_score": 0.880,
  "selected_strategies": [
    {
      "strategy_id": "STR-NBS-001",
      "name": "Coastal Wetland and Mangrove Restoration",
      "domain": "Nature-Based Solutions",
      "selection_reason": "Selected by MILP solver under budget constraint."
    }
  ],
  "optimization_summary": {
    "solver_type": "MILP_EXACT",
    "objective_value": 4.875,
    "qaoa_p_depth": 2,
    "qaoa_feasibility_probability": 0.689,
    "objective_gap": 0.470,
    "quantum_advantage_claimed": false
  },
  "explanation": {
    "decision_summary": "Optimized climate adaptation decision portfolio for Chennai District, Tamil Nadu.",
    "citations": [
      {
        "citation_id": "CIT-TN-CAP-003-CHK-001",
        "source_id": "TN-CAP-003",
        "title": "Chennai Climate Action Plan 2050",
        "page": 42
      }
    ]
  },
  "provenance": {
    "context_hash": "c7a8b9d0e1f2a3b45678901234567890abcdef1234567890abcdef1234567890",
    "evidence_packet_hash": "a8f9c2d1e3f4b5a678901234567890abcdef1234567890abcdef1234567890ab"
  },
  "validation_status": "VERIFIED",
  "decision_schema_version": "1.0.0",
  "created_at": "2026-09-23T00:30:00Z"
}
```
