# Phase H — 01 Repository Inventory

**Timestamp**: 2026-09-22T17:47:20+05:30  
**Scope**: Tamil Nadu (38 Districts) — Climate Adaptation Only

## Core Repository Architecture
- **Backend Architecture**: FastAPI, Python 3.10.11, PostgreSQL 18 + PostGIS 3.6, SQLAlchemy 2.0 ORM, Uvicorn server on port 8000.
- **Frontend Architecture**: React 18, TypeScript, Vite dev server on port 3000, TailwindCSS, React-Leaflet GIS engine.
- **Risk Engine (Phase E)**: XGBoost classifiers for Flood, Drought, Heatwave (`FCT-53-001` 53-feature contract).
- **Exposure Engine (Phase F)**: PostGIS spatial overlay (`ExposureService`), 150 infrastructure assets, 38 district population profiles.
- **Semantic Store**: ChromaDB local `PersistentClient` at `knowledge_base/chroma`.
- **Master Registries**: JSON schemas and master configuration files located in `config/master/`.
