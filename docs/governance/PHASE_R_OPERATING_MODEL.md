# Phase R — Enterprise Operating Model & Ownership Structure

## 1. Governance Operating Model
The platform operates under a strict role-based governance model separating Development, Research, Staging, Production, and Operations.

## 2. Role-Based Ownership Registry
| Role Title | Governance Scope | Responsibilities | Target Runbook |
| :--- | :--- | :--- | :--- |
| **Platform Owner** | Orchestration & APIs | Platform availability, SLO enforcement, API stability | `RB-PLATFORM-001` |
| **Data Owner** | PostGIS & Data Pipelines | Data freshness, 38-district completeness, schema drift | `RB-DATA-001` |
| **ML Owner** | ML Models & Risk Engine | Feature drift, model performance, calibration review | `RB-ML-001` |
| **Knowledge Owner** | ChromaDB & RAG | Document chunking, citation validation, KB releases | `RB-RAG-001` |
| **Security Owner** | Auth, RBAC, Secrets | Key rotation, vulnerability management, zero leakage | `RB-SEC-001` |
| **Operations Owner** | Docker, DB, Backups | RPO/RTO SLAs, disaster recovery drills, resource bounds | `RB-OPS-001` |
| **Research Owner** | QUBO & QAOA Engines | Quantum benchmarking, MILP parity, negative results | `RB-QUANTUM-001` |

## 3. Escalation Matrix
- **L1 (Operator / Automation)**: Automated alerts, health check probes, data ingestion retry.
- **L2 (Technical Owner)**: Service degradation, slow error budget burn, minor drift alerts.
- **L3 (Platform Architect)**: Fast error budget burn, security incidents, backup failure.
- **Scientific Review Board**: Model drift > 0.25 PSI, strategy applicability rule change, QUBO formulation updates.
- **Security Review Board**: API token compromise, unauthorized model promotion attempt, secret leakage detection.
