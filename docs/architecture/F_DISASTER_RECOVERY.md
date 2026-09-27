# Phase F — Disaster Recovery & Backup Verification

## Backup & Restore Plan
- **Recovery Point Objective (RPO)**: 24 Hours
- **Recovery Time Objective (RTO)**: 1 Hour
- **Primary Store**: PostgreSQL 18 `climate_platform` database
- **Offline Backup Store**: SQLite database `backend/data/climate_risk.db`
- **Restore Test Verification**: Database restore tested cleanly from backup SQL dump script `scripts/verify_infra.py`.
