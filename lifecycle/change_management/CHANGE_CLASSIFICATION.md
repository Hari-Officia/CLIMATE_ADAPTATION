# Change Classification Framework

| Class ID | Classification Title | Scope / Description | Approval Level | Required Validation |
| :--- | :--- | :--- | :--- | :--- |
| **CLASS_0** | Documentation Only | Non-functional Markdown or docstring fixes | Developer | Syntax & Markdown verification |
| **CLASS_1** | Non-Scientific Patch | Bug fixes without scientific logic changes | Technical Owner | Unit + Integration tests |
| **CLASS_2** | Operational Change | Monitoring, logging, runbook, or container configs | Operations Owner | Deployment smoke test |
| **CLASS_3** | Data Refresh / Change | Climatology dataset updates or new census indicators | Data Owner | Data quality & drift checks |
| **CLASS_4** | Model Replacement | XGBoost / SPI risk model retraining or weight updates | ML Owner | Model validation & calibration review |
| **CLASS_5** | Knowledge Base Change | ChromaDB document additions or chunking updates | Knowledge Owner | Citation validation & RAG regression |
| **CLASS_6** | Scientific Change | Risk formula, vulnerability weights, or hazard metrics | Scientific Review Board | 38-district regression & sensitivity audit |
| **CLASS_7** | Mathematical Change | MILP constraints, QUBO matrix penalty $P$, or QAOA params | Scientific Review Board | Mathematical equivalence & exact benchmark |
| **CLASS_8** | Security Change | Auth rules, key rotation, RBAC, or dependency patch | Security Owner | Security scan & RBAC regression |
| **CLASS_9** | Infrastructure Change | Database migration, PostGIS upgrades, multi-node HA | Operations Owner | DB backup/restore drill & failover test |
| **CLASS_10** | API Contract Change | REST endpoint additions, schema changes, or deprecation | Platform Owner | OpenAPI diff & client compatibility test |
