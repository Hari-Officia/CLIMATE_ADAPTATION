# RAG-to-LLM Context Handoff Contract

**Phase:** Phase N — RAG Grounding & Decision Explanation  
**Scope:** Climate Adaptation ONLY  
**Geography:** Tamil Nadu, India (All 38 Districts)  

---

## 1. Handoff Specification

The RAG Context Assembler constructs a structured, immutable evidence packet for a given district decision request. The LLM Explanation Engine consumes this packet as untrusted document text in isolated context blocks.

```json
{
  "request_id": "REQ-CHE-20260923",
  "district_id": "chennai",
  "district_name": "Chennai",
  "hazard_profile": ["coastal_flooding", "urban_heat", "drought"],
  "risk_score": 0.845,
  "adaptation_priority_score": 0.880,
  "candidate_strategy_ids": ["STR-NBS-001", "STR-ENG-002", "STR-URB-001"],
  "selected_portfolio": {
    "solver_type": "MILP_EXACT",
    "selected_strategy_ids": ["STR-NBS-001", "STR-URB-001"],
    "objective_value": 4.875,
    "qaoa_metrics": {
      "experiment_id": "EXP-QAOA-CHE-001",
      "p_depth": 2,
      "feasibility_probability": 0.689,
      "objective_gap": 0.470,
      "quantum_advantage": false
    }
  },
  "retrieved_evidence": [
    {
      "claim_id": "CLM-TN-CAP-003-012",
      "chunk_id": "CHK-TN-CAP-003-045",
      "source_id": "TN-CAP-003",
      "document_id": "DOC-TN-CAP-003",
      "citation_id": "CIT-TN-CAP-003-045",
      "claim_text": "Restoration of urban wetlands and coastal mangroves enhances natural flood attenuation capacity.",
      "evidence_type": "POLICY_RECOMMENDATION",
      "source_tier": "Tier 1",
      "organization": "Greater Chennai Corporation",
      "publication_year": 2023,
      "page": 42,
      "section": "4.2 Flood Attenuation"
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
  "evidence_packet_hash": "a8f9c2d1e3f4b5a678901234567890abcdef1234567890abcdef1234567890ab"
}
```

---

## 2. Invariant Rules
1. **Immutable Portfolio:** Selected strategy IDs cannot be added or removed by the LLM.
2. **Immutable Numeric Metrics:** Risk scores, priority values, and QAOA metrics must match the input exactly.
3. **Citation Bound:** The LLM may only reference citation IDs explicitly provided in the `citations` list.
