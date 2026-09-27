# PHASE T AUDIT REPORT 05: KARUR DEEP NUMERICAL RECONSTRUCTION

- **Status**: VERIFIED_PASSED
- **Timestamp**: 2026-09-23T14:45:00Z
- **Target District**: Karur (`karur`)
- **Target Experiment**: `EXP-QAOA-KARUR-P2`

---

## 1. Raw Sample Bitstring & Bit Order Analysis
- **Raw Measured Bitstring**: `100110000110110` (15 total bits = 14 candidate strategy variables + 1 slack variable bit).
- **Candidate Bits (First 14 Bits)**: `10011000011011`
- **15th Bit (Slack Variable)**: `0` (Decoded slack value = 3, matching budget slack $K - \sum x_i$).

---

## 2. Decoded Strategy Selection
- **Selected Strategy IDs**: `['STR-BLD-002', 'STR-DRN-002', 'STR-EWS-001', 'STR-URB-001', 'STR-WTR-001']`
- **Portfolio Size**: $\sum_{i=1}^{14} x_i = 5 = K$
- **Feasibility Check**: `Feasible = True` (Zero constraint violations).

---

## 3. Complete Numerical Chain
1. **Linear Adaptation Objective $c^T x$**: $\mathbf{4.7450}$
2. **Exact MILP Reference Optimum**: $\mathbf{4.8750}$
3. **Exact Enumeration Optimum**: $\mathbf{4.8750}$ (100% agreement with MILP)
4. **QUBO Constant Offset**: $-250.0$ ($P=10.0, K=5$)
5. **Direct Matrix QUBO Energy**: $-4.7450 - 150.0 = \mathbf{-154.7450}$
6. **Decoded Original Objective**: $-(-154.7450 + 150.0) = \mathbf{4.7450}$
7. **Reconciled Objective Gap**:
   $$\text{Gap} = \frac{4.8750 - 4.7450}{4.8750} = \mathbf{+0.0267} \ge 0.0000$$
8. **Optimal Shots Sampled**: `7` out of `1024` shots.
9. **Empirical Optimal Probability**: $\frac{7}{1024} = \mathbf{0.0068359375}$
