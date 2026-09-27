# PHASE Q ENVIRONMENT & DEPLOYMENT GOVERNANCE AUDIT

**Date:** 2026-09-23  
**Phase:** Phase Q — Enterprise Deployment, MLOps, Lifecycle & Governance  

---

## 1. Environment Segregation Matrix

| Environment | Scope | Database Target | Debug Mode | CORS Scope | Auth Strictness |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Development** | Local Dev | `climate_risk_db` / `climate_platform` | `True` | `*` (Wildcard allowed) | Warning mode |
| **Testing** | CI / Automated Pytest | SQLite / Test PostgreSQL | `False` | Restricted localhost | Mock token support |
| **Staging** | Pre-Production QA | Staging PostgreSQL | `False` | `https://staging.climate.tn.gov.in` | Enforced JWT |
| **Production** | Live Operations | Production PostgreSQL + PostGIS | `False` | `https://climate.tn.gov.in` | Enforced JWT + Rate Limits |

---

## 2. Configuration Contracts & Validation Rules

- **Typed Configuration Engine:** `backend/config.py` using Pydantic Settings / BaseSettings.
- **Fail-Fast Validation:**
  - `DATABASE_URL` missing -> Immediate Startup Exception.
  - `SECRET_KEY` length < 32 characters in production -> Startup Exception.
  - `DEBUG=True` in production environment -> Startup Exception.
  - Wildcard CORS in production -> Startup Exception.
