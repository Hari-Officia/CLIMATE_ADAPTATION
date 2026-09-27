# QUBO-to-QAOA Handoff Contract (Phase L -> Phase M)

**Contract ID:** `CONTRACT-QUBO-QAOA-v1.0`  
**Upstream Phase:** Phase L — Enterprise QUBO Formulation & Mathematical Bridge  
**Downstream Phase:** Phase M — QAOA Implementation & Classical-vs-Quantum Benchmarking  
**Geography:** Tamil Nadu, India (All 38 Districts)  

---

## 1. Input Specifications for Phase M

Phase M **MUST ONLY** consume frozen, verified QUBO instances produced and signed by Phase L.

Phase M is **STRICTLY FORBIDDEN** from:
1. Re-defining objective coefficients $c_i$ or $Q_{ij}$.
2. Removing hard conflict, dependency, or size constraints.
3. Modifying candidate strategies or variable ordering.
4. Altering dynamic penalty weights ($P_{conflict}, P_{dep}, P_{size}$).

---

## 2. Required Payload Fields

```json
{
  "qubo_id": "QUBO-TN-01-abc12345",
  "qubo_hash": "sha256-hex-digest",
  "classical_model_hash": "sha256-hex-digest",
  "candidate_set_id": "CANDSET-TN-01-v1.0",
  "candidate_set_version": "v1.0",
  "logical_variable_count": 17,
  "strategy_variable_count": 14,
  "slack_variable_count": 3,
  "constant_offset": 250.0,
  "linear_terms": {
    "0": -0.35,
    "1": -0.42
  },
  "quadratic_terms": {
    "0,1": -0.15,
    "0,2": 10.0
  },
  "equivalence_certificate": {
    "status": "VERIFIED",
    "feasibility_match": true,
    "optimality_match": true
  }
}
```

---

## 3. Ground-Truth Reference

Every Phase M QAOA experiment must benchmark its output against:
- `classical_optimum` (Phase J/K ExactSolver ground truth $F(x^*)$)
- `decoded_objective`
- `feasibility_status`
- `optimality_gap`
