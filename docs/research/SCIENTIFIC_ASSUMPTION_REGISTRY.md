# Enterprise Scientific Assumption Registry

This registry records all foundational scientific, mathematical, spatial, temporal, and methodological assumptions supporting the **Quantum Multi-Agent Decision Support System for Climate Adaptation** (Tamil Nadu — 38 Districts).

---

## Assumptions Register

### ASSUMP-001: Historical Climate Distribution Stationarity
- **Description**: Historical climate distributions (1981–2020 ERA5 reanalysis & IMD observations) remain valid baseline representations for downscaling feature engineering.
- **Origin**: Meteorological Feature Engineering Pipeline (`SC-FORM-001`).
- **Evidence**: IMD gridded daily dataset (0.25° resolution) & ERA5 reanalysis validation.
- **Scope**: All 38 districts of Tamil Nadu.
- **Risk if False**: Shift in baseline climate stationarity may underestimate localized extreme precipitation or drought frequencies.
- **Validation Method**: Annual Kolmogorov-Smirnov distribution comparison against new IMD observations.
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: ANNUAL
- **Status**: `SUPPORTED`

---

### ASSUMP-002: Coastal Surge Downscaling Uncertainty Bound ($\pm 12\%$)
- **Description**: Downscaled coastal storm surge hydrodynamic models for Tamil Nadu coastal districts (TN-001, TN-002, TN-003, TN-004, TN-005, TN-006, TN-007, TN-008, TN-009, TN-010, TN-011, TN-012, TN-013) carry a non-reducible spatial downscaling uncertainty of $\pm 12\%$.
- **Origin**: Coastal Hydrodynamic Downscaling Study (Phase F Exposure).
- **Evidence**: INCOIS coastal wave rider buoy validation & Bathymetry grid resolution (100m).
- **Scope**: 13 Coastal Districts of Tamil Nadu.
- **Risk if False**: Underestimating coastal surge height during severe cyclonic events.
- **Validation Method**: Post-event tide gauge & satellite altimetry validation.
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: QUARTERLY
- **Status**: `SUPPORTED`

---

### ASSUMP-003: Ground-Truth Adaptation Label Latency (1–3 Years)
- **Description**: Real-world physical climate adaptation outcomes (e.g., flood reduction, crop yield resilience, groundwater recharge) require 1 to 3 years post-implementation to observe ground-truth effectiveness labels.
- **Origin**: Empirical Adaptation Evaluation Framework (`SC-MOD-001`).
- **Evidence**: State Disaster Management Authority (SDMA) project implementation timelines.
- **Scope**: All 38 districts of Tamil Nadu.
- **Risk if False**: Early model retraining based on incomplete outcome labels causes label noise and model degradation.
- **Validation Method**: Multi-year longitudinal field survey & remote sensing index evaluation.
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: SEMI_ANNUAL
- **Status**: `SUPPORTED`

---

### ASSUMP-004: District Spatial Weighting Equality
- **Description**: All 38 districts of Tamil Nadu are evaluated using unified, standardized feature contracts (53 features) without arbitrary spatial weight manipulation.
- **Origin**: Feature Engineering Contract (`SC-FEAT-001`).
- **Evidence**: Spatial PIP spatial join completeness across Tamil Nadu boundary GeoJSON.
- **Scope**: All 38 districts of Tamil Nadu.
- **Risk if False**: Spatial bias favoring data-dense districts over data-poor inland districts.
- **Validation Method**: Spatial cross-validation & spatial bias audit (`district_model_validation.csv`).
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: QUARTERLY
- **Status**: `SUPPORTED`

---

### ASSUMP-005: MILP Optimal Reference Authority
- **Description**: The Mixed-Integer Linear Programming (MILP) classical solver output serves as the authoritative, exact mathematical reference for portfolio optimization benchmarking.
- **Origin**: Classical Solver Specification (`SC-OPT-001`).
- **Evidence**: Mathematical proof of branch-and-bound global optimality for binary Knapsack formulations.
- **Scope**: Portfolio Optimization Engine.
- **Risk if False**: Invalid classical reference invalidates QUBO parity checks and QAOA gap calculations.
- **Validation Method**: Exact candidate set enumeration comparison for candidate sets $N \le 20$.
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: QUARTERLY
- **Status**: `SUPPORTED`

---

### ASSUMP-006: QAOA Experimental Non-Quantum-Advantage ($Gap = 0.4700$)
- **Description**: QAOA on current noisy simulator/NISQ hardware with depth $p=1$ does NOT achieve quantum advantage over classical MILP solvers ($Gap = 0.4700$).
- **Origin**: Quantum Experimentation & Benchmarking Phase M (`SC-QAOA-001`).
- **Evidence**: 38-district experimental benchmark matrix (`AUDIT/PHASE_M/QAOA_38_DISTRICT_BENCHMARK_MATRIX.csv`).
- **Scope**: Quantum Optimization Subsystem.
- **Risk if False**: Prematurely claiming quantum advantage violates scientific integrity policies.
- **Validation Method**: Full simulator execution with noise-model comparisons across $p \in \{1, 2, 3\}$.
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: QUARTERLY
- **Status**: `SUPPORTED`

---

### ASSUMP-007: RAG Source Tier Hierarchy Superiority
- **Description**: Tier 1 (Tamil Nadu State Official Policy Documents) evidence strictly overrides Tier 2 (National), Tier 3 (International), Tier 4 (Academic Research), and Tier 5 (Other) during retrieval grounding.
- **Origin**: RAG Citation Enforcement Contract (`SC-RAG-001`).
- **Evidence**: State Climate Change Cell (TNSCCC) statutory authority.
- **Scope**: RAG Evidence Retrieval & Grounding.
- **Risk if False**: Non-authoritative external recommendations overriding state adaptation priority mandates.
- **Validation Method**: Golden set RAG retrieval & source hierarchy validation suite.
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: MONTHLY
- **Status**: `SUPPORTED`

---

### ASSUMP-008: Read-Only LLM Explanation Constraint
- **Description**: Large Language Models function strictly as read-only explanation interfaces and cannot alter numeric risk scores, portfolio selections, or mathematical optimization outputs.
- **Origin**: LLM Grounding Contract (`SC-LLM-001`).
- **Evidence**: Context-grounded system prompt enforcement and zero-mutation validation tests.
- **Scope**: LLM Explanation API.
- **Risk if False**: LLM hallucination altering scientific decision outputs or policy priority horizons.
- **Validation Method**: Adversarial prompt injection & numeric integrity test suite.
- **Last Reviewed**: 2026-09-23
- **Review Frequency**: MONTHLY
- **Status**: `SUPPORTED`
