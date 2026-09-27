# QAOA-to-RAG/LLM Handoff Contract (Phase M -> Phase N)

**Contract ID:** `CONTRACT-QAOA-RAG-LLM-v1.0`  
**Upstream Phase:** Phase M — Enterprise QAOA Implementation & Classical-vs-Quantum Benchmarking  
**Downstream Phase:** Phase N — RAG Evidence Integration & LLM Decision Explanation  
**Geography:** Tamil Nadu, India (All 38 Districts)  

---

## 1. Input Specifications for Phase N

Phase N (RAG / LLM Explanation Engine) **MUST ONLY** consume frozen, structured QAOA experiment payloads generated and signed by Phase M.

Phase N is **STRICTLY FORBIDDEN** from:
1. Re-running QAOA circuit simulation or modifying optimal portfolio selections $x^*$.
2. Fabricating claims of "quantum advantage", "quantum supremacy", or "faster quantum execution".
3. Overriding classical or QAOA optimization metrics, objective values, or constraint feasibility results.
4. Generating unverified qualitative efficacy or cost claims not present in Phase M database models.

---

## 2. Required Payload Fields

```json
{
  "qaoa_experiment_id": "EXP-QAOA-CHENNAI-a1b2c3d4",
  "certificate_id": "CERT-QAOA-CHENNAI-a1b2c3d4",
  "qubo_id": "QUBO-CHENNAI-10a477d2",
  "qubo_hash": "070d35fdddb3c2ec473ea9b27496aee1ed4694415ca6f1c7847f4d3aef002c33",
  "classical_model_hash": "e6d30ccd315c94eed6be972ef34c01f516714b89a7ccfde15bcb74a9b867821d",
  "district_id": "chennai",
  "selected_strategy_ids": ["STR-CIN-001", "STR-EWS-001", "STR-HTR-001", "STR-WTR-001", "STR-WTR-002"],
  "classical_optimum": 4.875,
  "qaoa_best_objective": 4.875,
  "objective_gap": 0.0,
  "feasible_probability": 0.354,
  "optimal_probability": 0.128,
  "qaoa_depth_p": 2,
  "shots": 1000,
  "status": "VERIFIED"
}
```

---

## 3. Allowed LLM Explanation Scope

Phase N LLM explanations may explain:
- Why the selected adaptation strategies ($x^*$) address local flood, heatwave, and drought hazards.
- What evidence claims in Phase I support the selected strategies.
- Which hard conflicts, dependencies, and portfolio size limits ($K=5$) were active during optimization.
- Measured classical-vs-QAOA convergence performance without hyping quantum capabilities.
