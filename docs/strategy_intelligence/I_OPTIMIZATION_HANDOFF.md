# Phase I Documentation — Handoff to Classical Optimization (Phase J/K)

## 1. Hand-off Protocol
Phase I passes immutable candidate sets (`StrategyCandidateSet`) directly downstream to Phase J/K Classical Strategy Portfolio Optimization.

## 2. Decision Variable Formulation
Each candidate strategy in `candidate_set.strategy_ids` corresponds to a binary decision variable $x_i \in \{0, 1\}$ in the downstream optimization formulation.

```
StrategyCandidateSet → Binary Decision Variables {x_1, x_2, ..., x_n} → Phase J/K Classical Portfolio Optimization
```

## 3. Downstream Phase
**PHASE J/K: CLASSICAL ADAPTATION STRATEGY OPTIMIZATION FOUNDATION**
