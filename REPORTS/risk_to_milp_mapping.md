# Risk to MILP Adaptation Mapping Audit

## Executive Summary

This audit evaluates the architectural connection and data flow between the **Machine Learning Risk Prediction Subsystem** (XGBoost models for Flood, Drought, Heatwave) and the **Mixed-Integer Linear Programming (MILP) Adaptation Optimization Subsystem** (scipy.optimize.milp).

**INTEGRATION STATUS**: NOT CURRENTLY INTEGRATED

---

## 1. Subsystem Interface Inspection

| Subsystem | Input Data | Output Data | Primary File / Code |
|---|---|---|---|
| **ML Risk Prediction** | 53-feature weather/climate vector (	emp_max, 
ainfall, soil_wetness, SPI, etc.) | Hazard predicted probabilities: (\text{Flood})$, (\text{Drought})$, (\text{Heatwave})$ | ackend/agents/risk_agent.py, Models/*.pkl |
| **MILP Adaptation Optimization** | Candidate strategy IDs (candidate_strategy_ids), Max portfolio size (=5$) | Binary strategy selection vector  \in \{0, 1\}^N$, Optimal portfolio objective (x)$ | ackend/services/optimization/solvers/milp_solver.py, ackend/services/optimization/objective_service.py |

---

## 2. Theoretical vs. Actual Data Flow

### Theoretical Target Architecture
`
ML RISK OUTPUT (Flood, Drought, Heatwave probabilities)
      ↓
TRANSFORMATION (District risk weighting & exposure scaling)
      ↓
MILP INPUT (Risk-weighted strategy objective coefficients c_i)
      ↓
OBJECTIVE / CONSTRAINT (Maximize sum(c_i * x_i) subject to K <= 5)
      ↓
ADAPTATION STRATEGY SELECTION
`

### Actual Code Implementation (ackend/services/optimization/objective_service.py)
`python
def build_objective_coefficients(self, candidate_strategy_ids: List[str], district_context: Dict[str, Any] = None) -> List[float]:
    coefficients = []
    for sid in candidate_strategy_ids:
        # Static lookup from config/master/strategies.json
        hazard_score = 1.0 if strat.get('primary_hazard_id') in ['HAZ-FLD', 'HAZ-HTW', 'HAZ-DRG'] else 0.5
        priority_score = 1.0 if horizon == 'IMMEDIATE' else (0.8 if horizon == 'SHORT_TERM' else 0.5)
        evidence_score = 1.0 if ev_strength == 'VERY_STRONG' else (0.8 if ev_strength == 'STRONG' else 0.5)
        
        # c_i is completely static and independent of district ML predicted risk probabilities!
        c_i = round(0.35 * hazard_score + 0.35 * priority_score + 0.30 * evidence_score, 4)
        coefficients.append(c_i)
    return coefficients
`

---

## 3. Disconnect Audit Findings

1. **Unused Parameter**: The district_context dictionary parameter in uild_objective_coefficients is default None and is ignored during coefficient calculation.
2. **Static Coefficients**: Objective coefficients $ are computed entirely from static strategy metadata fields (primary_hazard_id, planning_horizon, evidence_strength) defined in config/master/strategies.json.
3. **No Risk Scaling**: High dynamic risk predictions (e.g. (\text{Flood}) = 0.5789$) do not increase the weight of flood strategies (STR-BLT-002, STR-EWS-001, STR-DRN-001) in the MILP objective matrix.
4. **Conclusion**: The ML risk outputs and MILP adaptation optimization operate as decoupled, standalone modules.

---

## 4. Remediation / Integration Recommendation

To establish true Risk-to-Adaptation coupling in future iterations:
- Transform dynamic risk scores into strategy utility multipliers:
  c_i(\text{district}) = R(\text{hazard}_i) \times \text{Exposure}_i \times \text{Priority}_i \times \text{Evidence}_i
- Pass live district risk predictions from RiskAgent directly into ObjectiveService.build_objective_coefficients.
