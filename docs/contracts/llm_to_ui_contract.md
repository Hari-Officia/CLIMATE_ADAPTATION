# LLM-to-UI Handoff Contract

**Phase:** Phase N — RAG Grounding & Decision Explanation  
**Scope:** Climate Adaptation ONLY  
**Geography:** Tamil Nadu, India (All 38 Districts)  

---

## 1. Response Structure

The LLM Decision Explanation Engine returns a strictly validated JSON payload conforming to `schemas/explanation.schema.json`:

```json
{
  "explanation_id": "EXP-CHE-20260923-001",
  "district_id": "chennai",
  "district_name": "Chennai",
  "decision_summary": "Selected portfolio of 2 climate adaptation strategies for Chennai targeting coastal flooding and urban heat based on MILP optimization.",
  "risk_context_summary": "High risk (0.845) driven by extreme rainfall and coastal inundation.",
  "priority_context_summary": "Adaptation priority score 0.880 under high vulnerability and exposure.",
  "selected_strategies": [
    {
      "strategy_id": "STR-NBS-001",
      "name": "Coastal Wetland and Mangrove Restoration",
      "domain": "Nature-Based Solutions",
      "selection_reason": "Selected by MILP optimizer to maximize flood attenuation while satisfying budget constraint.",
      "evidence_status": "SUPPORTED",
      "citation_ids": ["CIT-TN-CAP-003-045"]
    }
  ],
  "optimization_explanation": {
    "solver_type": "MILP_EXACT",
    "objective_description": "Maximizing cumulative adaptation benefit under risk and cost constraints.",
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
  "uncertainties": [
    "Data uncertainty regarding local rainfall frequency under extreme warming scenarios."
  ],
  "limitations": [
    "Strategy applicability restricted to coastal flood risk areas."
  ],
  "conflicts": [],
  "citation_ids": ["CIT-TN-CAP-003-045"],
  "validation_status": "VERIFIED"
}
```

---

## 2. Mandatory Formatting Rules
- UI components must display citation badges linked to source document titles, organization, and page numbers.
- QAOA section must display "Quantum Advantage: Not Established" whenever `quantum_advantage_claimed` is false.
- Costs and timelines must render as "N/A - Insufficient evidence in official record" unless explicitly present in citation metadata.
