# Phase J/K Documentation — Quantum Research Handoff Specification

## 1. Ground-Truth Baseline Protocol
Phase J/K produces exact optimal portfolios using `ExactSolver` (binary enumeration) and `MILPSolver` (HiGHS MILP). These solutions serve as ground-truth benchmarks for Phase L (QUBO formulation) and Phase M (QAOA implementation).

## 2. Experimental Principles
1. **No Quantum Advantage Claims in Phase J/K**: Quantum algorithms are prohibited in Phase J/K.
2. **Fair Comparison Protocol**: QAOA (Phase M) must be evaluated against the exact same candidate sets, objective weights, and constraint penalty structures established in Phase J/K.
3. **No Softened Problems for QAOA**: QAOA must solve the identical mathematical problem without simplifying constraints.
