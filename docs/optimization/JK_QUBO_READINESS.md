# Phase J/K Documentation — QUBO Readiness Report

## 1. Mathematical Formulation Alignment
Phase J/K formulates binary decision variables $x_i \in \{0, 1\}$ for each candidate strategy in `StrategyCandidateSet`.

## 2. Decision Variable Mapping
```
Candidate Strategy (Phase I) → Binary Decision Variable x_i → Qubit x_i (Phase L)
```

## 3. Constraint to Penalty Transformation Plan (Phase L Handoff)
- Hard conflict $x_i + x_j \le 1 \implies P_{conflict} \cdot x_i x_j$
- Dependency $x_A \le x_B \implies P_{dep} \cdot x_A (1 - x_B)$
- Portfolio size $\sum x_i \le K \implies P_{size} \cdot (\sum x_i - K)^2$

## 4. Status
Phase J/K provides exact ground-truth values and classical baselines for Phase L QUBO formulation.
