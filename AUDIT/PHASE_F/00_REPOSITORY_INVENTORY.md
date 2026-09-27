# Phase F — 00 Repository Inventory

**Timestamp**: 2026-09-22T17:08:45+05:30  
**Scope**: Tamil Nadu (38 Districts) — Climate Adaptation Only

## Repository Summary
- **Backend Architecture**: FastAPI, Python 3.10.11, PostgreSQL 18 + PostGIS 3.6, SQLAlchemy 2.0 ORM, Uvicorn server on port 8000.
- **Frontend Architecture**: React 18, TypeScript, Vite dev server on port 3000, TailwindCSS, React-Leaflet GIS engine.
- **Semantic Store**: ChromaDB local `PersistentClient` at `knowledge_base/chroma`.
- **Master Registries**: JSON schemas and master configuration files located in `config/master/` (`districts.json`, `hazards.json`, `domains.json`, `datasets.json`, `models.json`, `feature_contracts.json`).
- **Offline Backup Store**: SQLite database at `backend/data/climate_risk.db`.
- **Verified Frozen Knowledge Base**: `knowledge_base/v1.0.0_verified/`.

## Directory Map & Key Component Locations
| Path | Component Type | Purpose |
|---|---|---|
| `backend/main.py` | FastAPI Application | Main API entry point |
| `backend/db/` | Database Layer | PostgreSQL/PostGIS connection, ORM models, DB init |
| `backend/api/` | API Routers | FastAPI routes for districts, hazards, risk, forecast |
| `backend/hazards/` | Risk Engine | XGBoost models (flood, drought, heatwave) |
| `backend/services/` | Business Logic | Service routines for risk, climate forecast, exposure |
| `config/master/` | Registries | Canonical registries for TN 38 districts & datasets |
| `schemas/` | Contracts | Pydantic & JSON Schemas for validation |
| `docs/contracts/` | Architecture | Human-readable contract specs |
| `tests/` | QA | Test matrix for Phase D, E, and F |
