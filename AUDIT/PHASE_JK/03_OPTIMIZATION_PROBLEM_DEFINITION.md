# Phase J/K Audit — 03 Optimization Problem Definition

## 1. Scope & Objective
Audit mathematical problem formulation for classical adaptation portfolio optimization.

## 2. Formulation
$$\max_{x \in \{0, 1\}^N} F(x) = \sum_{i=1}^N c_i x_i + \sum_{i < j} Q_{ij} x_i x_j$$
subject to:
$$\sum_{i=1}^N x_i \le K$$
$$x_i + x_j \le 1 \quad \forall (i,j) \in \text{Conflicts}$$
$$x_A - x_B \le 0 \quad \forall (A,B) \in \text{Dependencies}$$

- Status: **PASSED**
