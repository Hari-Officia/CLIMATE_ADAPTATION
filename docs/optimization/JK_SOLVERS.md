# Phase J/K Documentation — Solver Architecture

## 1. Classical Solvers
1. **`ExactSolver`**: $2^N$ binary enumeration for exact optimal baseline ($N \le 15$).
2. **`MILPSolver`**: SciPy HiGHS MILP solver (`scipy.optimize.milp`).
3. **`GreedySolver`**: Marginal gain heuristic baseline solver.

All solvers return structured result objects with timing, gap, and feasibility status.
