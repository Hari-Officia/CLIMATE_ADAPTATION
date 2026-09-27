# Phase R — Operational Runbook Index

## Master Runbook Catalog

| Runbook ID | Incident / Trigger Type | Target Component | Immediate Action | Primary Escalation |
| :--- | :--- | :--- | :--- | :--- |
| **RB-DATA-001** | Data Staleness (> 24 hours) | PostGIS / Ingestion | Trigger fallback climatology sync; check external API status | Data Owner |
| **RB-DATA-002** | Schema Drift Detected | Data Pipeline | Quarantine incoming dataset; halt schema migration | Data Owner |
| **RB-ML-001** | Feature Drift (PSI > 0.10) | Risk Engine | Trigger calibration evaluation; initiate retraining review | ML Owner |
| **RB-ML-002** | Model Performance Degradation | ML Models | Trigger fallback baseline model; notify ML Review Board | ML Owner |
| **RB-RAG-001** | Citation Validation Failure | ChromaDB / RAG | Isolate affected document chunk; purge vector cache | Knowledge Owner |
| **RB-RAG-002** | Knowledge Conflict Detected | RAG Engine | Place conflicting documents in QUARANTINED state | Knowledge Owner |
| **RB-LLM-001** | LLM Grounding Failure / Drift | Explanation Engine | Rollback prompt to previous version; verify citation check | Platform Owner |
| **RB-QUANTUM-001** | QUBO Hash Mismatch | QUBO Engine | Re-compute coefficient matrix hash; verify candidate map | Research Owner |
| **RB-QUANTUM-002** | QAOA Regression | QAOA Engine | Verify simulator backend seed; reset circuit parameters | Research Owner |
| **RB-OPS-001** | Database Backup Failure | PostgreSQL | Execute `scripts/backup_db.py`; inspect disk space | Operations Owner |
| **RB-OPS-002** | RPO / RTO SLA Miss | Infrastructure | Trigger standby database restore drill via `scripts/restore_db.py` | Operations Owner |
| **RB-SEC-001** | Secret Leakage Detected | Code Repository | Revoke compromised credential; run `scripts/scan_secrets.py` | Security Owner |
| **RB-SEC-002** | RBAC Authorization Failure | API Gateway | Inspect token claims; revoke expired JWT tokens | Security Owner |
| **RB-PROV-001** | Provenance Lineage Break | Orchestrator | Mark decision state REVIEW_REQUIRED; re-calculate hash | Platform Owner |
