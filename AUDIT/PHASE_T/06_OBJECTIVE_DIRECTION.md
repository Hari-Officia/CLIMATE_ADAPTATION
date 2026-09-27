# PHASE T AUDIT REPORT 06: OBJECTIVE DIRECTION & GAP FORMULATION

- **Status**: VERIFIED_PASSED
- **Timestamp**: 2026-09-23T14:45:00Z
- **Direction Alignment Matrix**:

```
ORIGINAL_OBJECTIVE_DIRECTION: MAXIMIZATION (f(x) = c^T x)
QUBO_OBJECTIVE_DIRECTION:      MINIMIZATION (H(x) = x^T Q x)
MILP_OBJECTIVE_DIRECTION:      MAXIMIZATION (f_MILP = max c^T x)
QAOA_OBJECTIVE_DIRECTION:      MAXIMIZATION (f_QAOA = c^T x_sampled)
```

---

## 1. Mathematical Gap Formula
For MAXIMIZATION:
$$\text{gap} = \frac{\text{f\_MILP} - \text{f\_QAOA}}{\max(|\text{f\_MILP}|, 1.0)}$$

- If $\text{f\_QAOA} \le \text{f\_MILP} \implies \text{gap} \ge 0.0000$.
- No gap clamping (`np.maximum(0.0, ...)` is strictly prohibited).
- If $\text{f\_QAOA} > \text{f\_MILP}$, `OBJECTIVE_VALIDATION_ANOMALY` is raised.
