# Master Audit Report: Project ML Models & MILP Optimization Metrics

> **Scientific Audit Notice**: This document summarizes the actual metrics, formulations, and evaluation results extracted directly from project artifacts (`ProjectCollab/ClimateRisk.ipynb`, `config/master/`, `config/models/model_registry.json`, `Models/`, `38_DISTRICT_QUANTUM_RESEARCH_GATE_V2.csv`, `V2_OBJECTIVE_RECONCILIATION.csv`, `tests/golden/38_district_golden_set.json`, `docs/RISK_DIAGNOSIS.md`, and `AUDIT/`). No synthetic data or unverified metric estimations were introduced.

---

# 1. Executive Summary

## Risk Prediction (Machine Learning)
- **Hazards Evaluated**: Flood (`flood`), Drought (`drought`), Heatwave (`heatwave`).
- **Algorithms Present**: **XGBoost Classifier** (`XGBClassifier` from `xgboost`). Other algorithms (Logistic Regression, Decision Trees, Random Forest, LightGBM, CatBoost, SVM, KNN, MLP, Transformers, LSTM) are cited in literature reviews within the repository but were **NOT experimentally implemented or benchmarked** in code artifacts.
- **Final Selected Models**:
  - **Flood**: `Models/flood_xgboost.pkl` (`MDL-XGB-FLD-001` / `MOD-FLD-XGB-v1.2`)
  - **Drought**: `Models/drought_xgboost.pkl` (`MDL-XGB-DRG-001` / `MOD-DRO-SPI-v1.0`)
  - **Heatwave**: `Models/heatwave_xgboost.pkl` (`MDL-XGB-HTW-001` / `MOD-HTW-ANO-v1.1`)
- **Primary Metrics Obtained**:
  - **Flood (Test Set, 41,648 samples)**: PR-AUC = `0.0745`, Recall = `0.3377` (33.77%), Precision = `0.1006` (10.06%), F1 = `0.1550` (15.50%), ROC-AUC = `0.9062`, Accuracy = `0.9867` (98.67%).
  - **Flood (Validation Set, 27,740 samples)**: PR-AUC = `0.0026`, Recall = `0.0132`, Precision = `0.0093`, F1 = `0.0109`, ROC-AUC = `0.4050`, Accuracy = `0.9934`.
  - **Drought**: ROC-AUC = `0.9998`, PR-AUC = `0.9993` (Master Registry / Notebook). *Confusion matrix metrics (Precision, Recall, F1, Accuracy) are NOT AVAILABLE in saved project artifacts.*
  - **Heatwave**: ROC-AUC = `1.0000`, PR-AUC = `0.9964` (Master Registry / Notebook). *Confusion matrix metrics (Precision, Recall, F1, Accuracy) are NOT AVAILABLE in saved project artifacts.*

## MILP Adaptation Optimization
- **Solver Engine**: `scipy.optimize.milp` using the **HiGHS Mixed-Integer Linear Programming Backend**.
- **Optimization Objective**: Maximize portfolio utility function $F(x) = \sum_{i=1}^N c_i x_i + \sum \text{bonus}_{ij} x_i x_j$ subject to hard portfolio constraints.
- **Optimality Status**: **PROVEN OPTIMAL** across all 38 canonical Tamil Nadu district benchmark instances ($N=14$, $K=5$).
- **MIP Gap**: **0.00%** (0.0 absolute gap, exact agreement with 100% exact enumeration).
- **Feasibility Status**: **100% FEASIBLE** (`constraint_violations = 0`).
- **Solve Time**: **< 5.0 ms** per district instance (< 0.005 seconds).

---

# 2. Risk Prediction Results

### Identified Model Files & Specifications

| Model ID | Hazard | Algorithm | Feature Contract | Training Dataset | Feature Count | Training Samples | Val Samples | Test Samples | Model Path |
|---|---|---|---|---|---|---|---|---|---|
| `MDL-XGB-FLD-001` | Flood | XGBoost (`XGBClassifier`) | `FCT-53-001` (15 meteorol. + 38 district 1-hot) | `DS-HIST-CLIMATE-001` (2010–2021) | 53 | 105,298 | 27,740 | 41,648 | `Models/flood_xgboost.pkl` |
| `MDL-XGB-DRG-001` | Drought | XGBoost (`XGBClassifier`) | `FCT-53-001` (15 meteorol. + 38 district 1-hot) | `DS-HIST-CLIMATE-001` (2010–2021) | 53 | 166,554 | 27,740 | 34,656 | `Models/drought_xgboost.pkl` |
| `MDL-XGB-HTW-001` | Heatwave | XGBoost (`XGBClassifier`) | `FCT-53-001` (15 meteorol. + 38 district 1-hot) | `DS-HIST-CLIMATE-001` (2010–2021) | 53 | 166,554 | 27,740 | 34,656 | `Models/heatwave_xgboost.pkl` |

### Detailed Classification Metrics (Extracted from Notebook Execution Outputs)

#### Flood Risk Classifier (`Models/flood_xgboost.pkl`)
- **Test Set Evaluation (41,648 samples, 151 positive floods)**:
  - **PR-AUC / Average Precision**: `0.0745` (Primary Metric)
  - **Recall (Sensitivity)**: `0.3377` (33.77%)
  - **Precision**: `0.1006` (10.06%)
  - **F1-Score**: `0.1550` (15.50%)
  - **ROC-AUC**: `0.9062`
  - **Accuracy**: `0.9867` (98.67%)
  - **Specificity**: `0.9890` (98.90%)
  - **Brier Score**: `NOT AVAILABLE`
  - **Confusion Matrix**: TP = `51`, TN = `41,041`, FP = `456`, FN = `100`
- **Validation Set Evaluation (27,740 samples, 76 positive floods)**:
  - **PR-AUC**: `0.0026`
  - **Recall**: `0.0132` (1.32%)
  - **Precision**: `0.0093` (0.93%)
  - **F1-Score**: `0.0109` (1.09%)
  - **ROC-AUC**: `0.4050`
  - **Accuracy**: `0.9934` (99.34%)
  - **Confusion Matrix**: TP = `1`, TN = `27,557`, FP = `107`, FN = `75`

> [!WARNING]
> **Accuracy Trap**: Flood exhibits extreme class imbalance (0.36% positive rate in test set). While accuracy is **98.67%**, PR-AUC is only **0.0745** and F1 is **15.50%**. Describing this model as "98.67% successful" without stating PR-AUC and F1 is scientifically misleading.

#### Drought Risk Classifier (`Models/drought_xgboost.pkl`)
- **ROC-AUC**: `0.9998` (Master Registry / Notebook) / `0.8650` (Model Registry v1.0 snapshot)
- **PR-AUC**: `0.9993` (Master Registry / Notebook) / `0.8120` (Model Registry v1.0 snapshot)
- **Accuracy, Precision, Recall, F1, Confusion Matrix**: `NOT AVAILABLE IN CURRENT PROJECT ARTIFACTS`
- **Brier Score**: `NOT AVAILABLE`

#### Heatwave Risk Classifier (`Models/heatwave_xgboost.pkl`)
- **ROC-AUC**: `1.0000` (Master Registry / Notebook) / `0.9100` (Model Registry v1.1 snapshot)
- **PR-AUC**: `0.9964` (Master Registry / Notebook) / `0.8780` (Model Registry v1.1 snapshot)
- **Accuracy, Precision, Recall, F1, Confusion Matrix**: `NOT AVAILABLE IN CURRENT PROJECT ARTIFACTS`
- **Brier Score**: `NOT AVAILABLE`

---

# 3. Risk Model Comparison

In the project artifacts, only **XGBoost Classifier** was experimentally trained and evaluated. No baseline comparisons against Logistic Regression, Random Forest, LightGBM, CatBoost, SVM, KNN, or Deep Learning were saved in the repository artifacts.

- **Flood Selected Model**: XGBoost (`MDL-XGB-FLD-001`), PR-AUC = `0.0745`, F1 = `0.1550`, Leakage = `LEAKAGE-SAFE`.
- **Drought Selected Model**: XGBoost (`MDL-XGB-DRG-001`), PR-AUC = `0.9993`, ROC-AUC = `0.9998`, Leakage = `REPORTED RESULT — LEAKAGE-AFFECTED`.
- **Heatwave Selected Model**: XGBoost (`MDL-XGB-HTW-001`), PR-AUC = `0.9964`, ROC-AUC = `1.0000`, Leakage = `LEAKAGE-SAFE`.

---

# 4. Leakage and Validation Audit

1. **Drought Model Target Proxy Leakage**:
   - Status: `REPORTED RESULT — LEAKAGE-AFFECTED` / `POTENTIAL LEAKAGE`
   - **Finding**: In `ProjectCollab/ClimateRisk.ipynb`, drought ground truth labels were constructed using `SPI_3 <= -1 OR SPI_6 <= -1`. The input feature vector passed to XGBoost included `SPI_3` and `SPI_6` as predictors. The model achieved near-perfect metrics (ROC-AUC 0.9998, PR-AUC 0.9993) because it directly learned the explicit rule defining the target.
   - **Inference Failure**: When SPI values were absent in short-term weather forecasts, setting SPI to `0.0` (normal rainfall) resulted in drought probability $\approx 0.00001$.

2. **Temporal Validation Integrity**:
   - The ML pipeline enforced a strict chronological time-based split:
     - **Train**: 2010-01-01 to 2017-12-31 (105,298 samples for Flood)
     - **Validation**: 2018-01-01 to 2019-12-31 (27,740 samples)
     - **Test**: 2020-01-01 to 2024-01-01 (41,648 samples)
   - No random K-Fold cross-validation leakage was detected across time boundaries.

---

# 5. Calibration Audit

- **Calibration Status**: `UNCALIBRATED RISK SCORE` across all models.
- **Diagnostics**: Model outputs represent raw uncalibrated logistic sigmoid scores.
- Neither Platt Scaling nor Isotonic Regression was applied in existing project artifacts.
- No Brier scores or reliability diagrams are present in stored project artifacts.

---

# 6. MILP Formulation

### Mathematical Model Formulation (`backend/services/optimization/solvers/milp_solver.py`)
- **Decision Variables**: $x_i \in \{0, 1\}$ for candidate strategies $i = 1, \dots, N$ ($N=14$ per district instance).
- **Integrality**: Strict binary integer constraint (`integrality = np.ones(N)`).
- **Objective Direction**: Maximization:
  $$\max_{x} F(x) = \sum_{i=1}^N c_i x_i + \sum_{(i,j) \in \text{Comp}} \text{bonus}_{ij} x_i x_j$$
  where $c_i = 0.35 \cdot \text{hazard\_score}_i + 0.35 \cdot \text{priority\_score}_i + 0.30 \cdot \text{evidence\_score}_i$.
  *Note: `scipy.optimize.milp` minimizes $-c^T x$, returning the exact negated objective value.*
- **Constraints**:
  1. **Portfolio Size Constraint**:
     $$\sum_{i=1}^N x_i \le K \quad (K = 5)$$
  2. **Hard Conflict Constraints**:
     $$x_i + x_j \le 1 \quad \forall (i, j) \in \text{Conflicting Pairs}$$
  3. **Dependency Constraints**:
     $$x_A - x_B \le 0 \quad \forall (A, B) \text{ where Strategy } A \text{ depends on } B$$

---

# 7. MILP Solver Results

Summarized across all 38 Tamil Nadu districts from `38_DISTRICT_QUANTUM_RESEARCH_GATE_V2.csv`:

| District Count | Solver Engine | Mean Objective Value | Min Objective | Max Objective | Solver Status | Optimality | MIP Gap | Mean Solve Time |
|---|---|---|---|---|---|---|---|---|
| **38 Districts** | `scipy.optimize.milp (HiGHS)` | **3.7744** | **3.0517** (Karur) | **4.1311** (Kanniyakumari) | `SUCCESS` | **PROVEN OPTIMAL** | **0.00%** | **< 5.0 ms** |

---

# 8. Constraint Validation

Every MILP solution returned by `scipy.optimize.milp` was validated using `ConstraintService.validate_portfolio_feasibility()`:
- **Binary Integrality**: `100% VALID` ($x_i \in \{0, 1\}$, no continuous values returned).
- **Budget / Portfolio K Limit ($\sum x_i \le 5$)**: `100% SATISFIED` (Max selected $K=5$, Coimbatore $K=4$).
- **Conflict Constraints**: `0 VIOLATIONS` ($x_i + x_j \le 1$ enforced for all conflicting pairs).
- **Dependency Constraints**: `0 VIOLATIONS` ($x_A \le x_B$ enforced for dependent pairs).
- **Total Constraint Violations**: `0` across all 38 districts.

---

# 9. MILP Strategy Selection

Across all 38 Tamil Nadu districts, the MILP solver selected the optimal 5-strategy (or 4-strategy) adaptation portfolio.

### Top Selected Strategies Across 38 Districts:
1. `STR-WTR-001` (Rooftop Rainwater Harvesting): Selected in **38 / 38 districts**
2. `STR-CIN-001` / `STR-CRT-001` (Hospital Backup Power & Water): Selected in **38 / 38 districts**
3. `STR-EWS-001` (IoT River Gauge & Flood Early Warning): Selected in **38 / 38 districts**
4. `STR-HTR-001` / `STR-HTS-001` (Cool Roof Coating & Urban Shade): Selected in **38 / 38 districts**
5. `STR-BLD-002` / `STR-BLT-002` (Permeable Paving & Flood Roads): Selected in **37 / 38 districts** (Excluded in Coimbatore where $K=4$)

---

# 10. MILP vs Other Optimization Methods

Comparison across 38 districts using existing benchmark outputs (`38_DISTRICT_QUANTUM_RESEARCH_GATE_V2.csv`, `EXACT_MILP_QUBO_EQUIVALENCE.csv`):

| Optimization Method | Objective Value (Mean) | Mean Optimality Gap | Feasibility Rate | Solver Engine | Proven Optimal? |
|---|---|---|---|---|---|
| **MILP** | **3.7744** | **0.0000** (0.0%) | **100%** | `scipy.optimize.milp (HiGHS)` | **YES** |
| **Exact Enumeration** | **3.7744** | **0.0000** (0.0%) | **100%** | Brute Force ($2^{14}$ states) | **YES** |
| **Greedy Search** | **3.7744** | **0.0000** (0.0%) | **100%** | Heuristic Greedy | NO |
| **Simulated Annealing** | -152.31 (Undecoded) / ~3.75 | ~0.0050 | **100%** | Classical SA | NO |
| **QAOA (p=2)** | 4.6980 (Penalty uncorrected) | -0.2447 (Anomaly) | ~64.5% | Qiskit Aer Simulator | NO |

> **Optimality Gap Formula**: $\text{gap} = \frac{\text{MILP Objective} - \text{Method Objective}}{\text{MILP Objective}}$ for maximization.

---

# 11. Risk-to-Adaptation Integration

- **Status**: `NOT CURRENTLY INTEGRATED`
- **Detailed Finding**: The ML Risk Prediction outputs ($P(\text{Flood})$, $P(\text{Drought})$, $P(\text{Heatwave})$) operate independently of the MILP solver. In `ObjectiveService.build_objective_coefficients()`, strategy objective coefficients $c_i$ are derived exclusively from static strategy metadata fields in `config/master/strategies.json`. Dynamic ML hazard risks do not currently alter the optimization objective matrix or selection constraints.

---

# 12. Limitations

1. **ML Model Imbalance & Validation Drift**: Flood model exhibits severe validation degradation (Val PR-AUC `0.0026` vs Test PR-AUC `0.0745`) due to low event frequencies.
2. **Drought Target Proxy Leakage**: `SPI_3` and `SPI_6` predictors leakage artificially inflated Drought metrics (`0.9998`).
3. **Uncalibrated Model Scores**: Sigmoid outputs are uncalibrated and cannot be interpreted as calibrated physical probabilities without Platt scaling or Isotonic Regression.
4. **Lack of Risk-MILP Coupling**: Strategy selection is currently uncoupled from real-time ML risk predictions.
