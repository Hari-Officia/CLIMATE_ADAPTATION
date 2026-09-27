# Phase S — Limitation Matrix

## Canonical System Limitations & Residual Risk Register

| Limitation ID | Domain | Description / Evidence | Operational Impact | Mitigation | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LIM-001** | Scope & Geography | Scope strictly limited to Climate Adaptation ONLY for Tamil Nadu 38 districts | Mitigation strategies and non-TN geographies are outside production scope | Clear UI/API scope labeling | ACTIVE |
| **LIM-002** | Quantum Computing | QAOA Objective Gap = 0.4700 vs MILP exact solution | QAOA cannot replace classical MILP for production decision generation | Quantum Advantage labeled NOT ESTABLISHED | ACTIVE |
| **LIM-003** | Data Ingestion | Outcome labels for climate adaptation strategies carry 1-3 year empirical delay | Real-time ML calibration relies on surrogate indicators | Drift monitoring and temporal validation | ACTIVE |
| **LIM-004** | Spatial Downscaling | Coastal extreme-surge 1km grid downscaling uncertainty is approximately +/- 12% | Coastal vulnerability scores retain confidence intervals | Display uncertainty bounds in GIS UI | ACTIVE |
| **LIM-005** | Infrastructure | Single-node PostgreSQL deployment in staging environment | Multi-node streaming HA failover deferred | Automated 24h backup and <1h restore SLA | ACKNOWLEDGED |
