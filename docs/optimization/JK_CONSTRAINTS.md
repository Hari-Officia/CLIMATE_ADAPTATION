# Phase J/K Documentation — Constraint Architecture

## 1. Constraint Matrix Definitions
- **Size Bound**: $\sum_{i=1}^N x_i \le K$
- **Hard Conflicts**: $x_i + x_j \le 1 \quad \forall (i,j) \in \text{Conflicts}$
- **Dependencies**: $x_A - x_B \le 0 \quad \forall (A,B) \in \text{Dependencies}$

## 2. Infeasibility Diagnostic
`ConstraintService` reports specific violation reasons if no feasible assignment satisfies all hard constraints.
