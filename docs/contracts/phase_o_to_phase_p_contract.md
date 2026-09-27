# Phase O to Phase P Handoff Contract Specification

**Upstream Phase:** Phase O — Enterprise Decision Intelligence API & Multi-Agent Orchestration  
**Downstream Target:** Phase P — Enterprise GIS Decision Intelligence Interface & UI  

---

## 1. Overview

Phase O provides the complete, production-hardened API and decision object specification for Phase P (GIS User Interface).

The frontend in Phase P consumes `/api/v1/decision/analyze` or `/api/v1/decision/{decision_id}` to retrieve a canonical `DecisionIntelligenceResult` object containing:
- District GeoJSON boundary and spatial risk layer.
- Composite risk score and hazard breakdown.
- Adaptation priority score and driver breakdown.
- Selected strategy portfolio (exact classical MILP / QAOA output).
- QAOA experiment metrics (`qaoa_p_depth`, `feasibility_probability`, `objective_gap`, `quantum_advantage_claimed=False`).
- Grounded decision explanation with interactive citation badges.
- Data provenance graph, hashes, and validation status.

---

## 2. Invariant Handoff Rules for Phase P
1. Frontend MUST NOT recalculate risk, priority, or optimization scores.
2. Frontend MUST display "Quantum Advantage: Not Established" whenever `quantum_advantage_claimed` is false.
3. Every claim in the evidence panel MUST render its associated `citation_id` with source title, organization, and page number.
