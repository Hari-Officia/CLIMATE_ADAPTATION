# Phase J/K Documentation — SciPy HiGHS MILP Solver

## 1. MILP Formulation
Formulated via `scipy.optimize.milp` using exact bounds $x \in \{0,1\}^N$ and linear inequality constraints matrix ($A \cdot x \le b$).

## 2. Optimality Gap
HiGHS solver tracks exact primal-dual bounds and reports optimality gap ($0.0$ for proven optimal solutions).
