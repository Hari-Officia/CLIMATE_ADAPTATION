# Phase J/K Documentation — Decision Variables

## 1. Binary Decision Variable Definition
For each strategy candidate $i$ in `candidate_set.strategy_ids`, a binary decision variable is declared:
$$x_i \in \{0, 1\}$$
where $x_i = 1$ indicates that strategy $i$ is selected for inclusion in the adaptation portfolio, and $x_i = 0$ indicates non-selection.

## 2. Ineligible Candidates
Ineligible strategies are filtered out prior to optimization and never enter the decision variable vector.
