# Adaptation Features & Mathematical Parameters Summary

## 🎯 Overview
The **Adaptation Features Subsystem** (`backend/services/optimization/objective_service.py` & `constraint_service.py`) defines the quantitative parameters and objective weights that evaluate adaptation interventions during classical MILP and quantum QUBO portfolio optimization.

---

## 🧮 Strategy Parameter Specifications

| Parameter Symbol | Attribute Name | Scale / Unit | Function in Optimization |
|---|---|---|---|
| $C_i$ | `cost_inr_lakhs` | Lakhs INR ($\ge 0$) | Consumes available district budget limit $B_{\max}$ |
| $\Delta R_i$ | `risk_reduction_pct` | Fraction $[0.0, 1.0]$ | Primary optimization reward coefficient for lowering hazard risk |
| $B_i$ | `co_benefits_score` | Score $[0.0, 1.0]$ | Secondary bonus for economic, ecological, or community benefits |
| $T_i$ | `lead_time_months` | Months ($\ge 1$) | Execution velocity constraint and scheduling priority |
| $S_{ij}$ | `synergy_score` | Score $[0.0, 0.5]$ | Pairwise quadratic interaction reward ($x_i \cdot x_j$) when co-deployed |
| $E_{ij}$ | `conflict_flag` | Binary $\{0, 1\}$ | Enforces mutual exclusion penalty ($x_i + x_j \le 1$) |
| $D_{ij}$ | `dependency_flag` | Binary $\{0, 1\}$ | Enforces prerequisite condition ($x_j \le x_i$) |

---

## ⚖️ Objective Function Formulation

The total linear objective coefficient $c_i$ for strategy $i$ is calculated as:

$$c_i = \left( \alpha \cdot \Delta R_i \right) + \left( \beta \cdot B_i \right) - \left( \gamma \cdot \frac{C_i}{B_{\max}} \right)$$

Where:
* $\alpha = 0.50$ (Risk Reduction Weight)
* $\beta = 0.30$ (Co-Benefits Weight)
* $\gamma = 0.20$ (Cost Efficiency Weight)

The complete quadratic objective maximized by the quantum QUBO solver is:

$$\max_{x} \quad \sum_{i=0}^{N-1} c_i x_i + \sum_{i < j} S_{ij} x_i x_j$$

---

## 💻 Minimal Code Example

```python
# backend/services/optimization/objective_service.py
from typing import List, Dict, Any

class ObjectiveService:
    def __init__(self, alpha: float = 0.50, beta: float = 0.30, gamma: float = 0.20):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def compute_strategy_coefficient(
        self,
        risk_reduction: float,
        co_benefits: float,
        cost: float,
        budget_limit: float
    ) -> float:
        """Derives linear objective coefficient c_i for QUBO builder."""
        normalized_cost = cost / budget_limit if budget_limit > 0 else 1.0
        c_i = (self.alpha * risk_reduction) + (self.beta * co_benefits) - (self.gamma * normalized_cost)
        return round(c_i, 4)

    def build_objective_coefficients(
        self,
        candidate_strategies: List[Dict[str, Any]],
        budget_limit: float = 1000.0
    ) -> List[float]:
        """Returns vector of objective coefficients c_i for candidate set."""
        return [
            self.compute_strategy_coefficient(
                risk_reduction=s.get("risk_reduction_pct", 0.2),
                co_benefits=s.get("co_benefits_score", 0.5),
                cost=s.get("cost_inr_lakhs", 100.0),
                budget_limit=budget_limit
            )
            for s in candidate_strategies
        ]
```
