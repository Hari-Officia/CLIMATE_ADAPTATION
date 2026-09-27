# Phase J/K Documentation — Objective Architecture

## 1. Multi-Objective Structure
Component objectives:
1. **Hazard Risk Coverage** ($w = 0.35$)
2. **Adaptation Priority Horizon Alignment** ($w = 0.35$)
3. **Scientific Evidence Quality** ($w = 0.30$)
4. **Complementarity Bonus** ($Q_{ij} = +0.15 \text{ to } +0.25$)

## 2. Formulation
Linear objective coefficients $c_i$ are calculated in `ObjectiveService` and passed to MILP / exact solvers.
