# Phase J/K Documentation — Problem Definition

## 1. Objective Function
$$\max_{x \in \{0,1\}^N} F(x) = \sum_{i=1}^N c_i x_i + \sum_{i < j} Q_{ij} x_i x_j$$

## 2. Constraints
- Portfolio Size Bound: $\sum_{i=1}^N x_i \le K$
- Hard Incompatibility Conflicts: $x_i + x_j \le 1 \quad \forall (i,j) \in \text{Conflicts}$
- Prerequisite Dependencies: $x_A - x_B \le 0 \quad \forall (A,B) \in \text{Dependencies}$
