# Disaster Recovery & Continuity Plan

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. RPO & RTO Operational Metrics

| Metric | Target Standard | Infrastructure Status | Operational Recovery Procedure |
| :--- | :--- | :--- | :--- |
| **Recovery Point Objective (RPO)** | 24 Hours | **ESTABLISHED** | Daily automated JSON/pg_dump snapshots of PostgreSQL & ChromaDB. |
| **Recovery Time Objective (RTO)** | 1 Hour | **ESTABLISHED** | Automated container restart via Docker Compose / `scripts/restore_db.py`. |

---

## 2. Recovery Procedures by Failure Scenario

1. **PostgreSQL Database Corruption / Crash:**
   - Execute `python scripts/restore_db.py` using latest verified backup in `scratch/backups/`.
   - Rerun `python scripts/run_phase_p_38_district_ui.py` smoke test.
2. **ChromaDB Vector Store Corruption:**
   - Re-execute `python scripts/build_adaptation_knowledge.py` to rebuild embeddings from `knowledge_base/` source PDFs.
3. **QAOA Quantum Simulator Service Outage:**
   - System automatically degrades gracefully to **Classical MILP Solver** mode and sets `qaoa_status = UNAVAILABLE` without crashing decision API.
