# Phase F — Enterprise Data Architecture

**Scope**: Tamil Nadu (38 Districts) — Climate Adaptation Only  
**Authoritative Runtime Store**: PostgreSQL 18 + PostGIS 3.6 (`climate_platform`)  
**Semantic Store**: ChromaDB (`knowledge_base/chroma`)

## Data Layer Hierarchy
```
DATA SOURCES (IMD, TNDMA, Census, WorldPop, OSM)
      ↓
INGESTION & RAW METADATA REGISTRATION
      ↓
VALIDATION & DATA QUALITY CHECKS
      ↓
POSTGIS AUTHORITATIVE STORE (core, provenance, exposure, spatial, infrastructure, audit)
      ↓
EXPOSURE PROCESSING ENGINE (Spatial PIP & Overlay)
      ↓
RISK-EXPOSURE INTEGRATION PROFILE (FastAPI REST Services)
```

## Logical Database Schemas
- **provenance**: `sources`, `datasets`, `dataset_versions`, `lineage`
- **quality**: `data_quality_checks`, `data_quality_issues`
- **spatial**: `spatial_layers`, `layer_versions`
- **infrastructure**: `assets`
- **exposure**: `population_exposure`, `built_environment_exposure`, `infrastructure_exposure`, `exposure_records`
- **audit**: `data_conflicts`, `processing_runs`
