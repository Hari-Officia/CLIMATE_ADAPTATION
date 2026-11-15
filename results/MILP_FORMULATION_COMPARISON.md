# MILP Formulation Comparison: Priority-Weighted vs Unweighted

> **Executive Audit Notice**: This document details the mathematical disambiguation between the two distinct MILP optimization formulations present in the repository. These formulations serve different pipeline purposes and evaluate different objective functions. They MUST NOT be confused or directly compared by raw objective value.

---

## 1. Formulation Definitions

### Formulation A: Priority-Weighted Research Gate Benchmark
- **Source Module**: `research/quantum_advantage/classical/true_milp_solver.py` via `CanonicalModelInstance`
- **Objective Function**: $F(x) = c^T x = \sum_{i=1}^{14} c_i x_i$
- **Coefficient Generation**: $c_i$ is derived dynamically from risk prediction models (Flood, Drought, Heatwave hazard severity), district vulnerability indices, and strategy domain priorities.
- **District Objective Range**:
  - **Mean**: `3.7948`
  - **Median**: `3.8279`
  - **Min**: `3.0517` (Karur)
  - **Max**: `4.1311` (Kanniyakumari)
  - **Std Dev**: `0.2675`
  - **25th Percentile**: `3.7199`
  - **75th Percentile**: `4.0016`

### Formulation B: Unweighted Live Backend Solver
- **Source Module**: `backend/services/optimization/solvers/milp_solver.py` via `OptimizationService`
- **Objective Function**: $F(x) = c^T x + \text{Synergy Bonuses}$
- **Coefficient Generation**: Uses static base strategy scores without district hazard risk scaling.
- **District Objective Range**:
  - **Mean**: `4.6700`
  - **Median**: `4.6700`
  - **Min**: `4.6700`
  - **Max**: `4.6700`

---

## 2. Mathematical Disambiguation & Rationale

1. **Why Objective Values Differ**:
   - Formulation A scales objective coefficients using local climate risk predictions (e.g. higher flood risk in coastal districts yields higher weights for flood defenses), resulting in district-varying total objective scores (3.0517 to 4.1311).
   - Formulation B evaluates strategy candidates against static baseline efficacy scores, producing an identical objective value of 4.6700 across districts with full candidate sets.
2. **Scientific Validity**:
   - Neither formulation is "better" based on raw magnitude. Raw objective values are non-comparable across different objective functions ($c_{pw} \neq c_{uw}$). Both solvers achieve **100% feasibility and proven mathematical optimality (MIP gap = 0.00%)** under their respective formulations.
