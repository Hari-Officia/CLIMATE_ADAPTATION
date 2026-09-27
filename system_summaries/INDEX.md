# Project Architecture & Subsystem Summaries

Welcome to the central documentation index for the **Climate Adaptation & Quantum Portfolio Optimization Platform**. This directory contains comprehensive, module-by-module summaries covering the full stack architecture, data pipelines, machine learning feature engineering, risk diagnosis engines, GIS spatial resolution, vector knowledge base RAG retrieval, and quantum-classical hybrid optimization flows.

---

## 📚 Document Index

| # | Topic | File Link | Description |
|---|---|---|---|
| 01 | **Forecast API** | [forecast_api.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/forecast_api.md) | Open-Meteo REST API integration, 7-day daily & hourly climate forecasts, baseline fallback mechanism, and FastAPI route handlers. |
| 02 | **ML Models** | [models.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/models.md) | Multi-hazard XGBoost classification models for Heatwave, Flood, Drought, and Cyclone prediction across Tamil Nadu. |
| 03 | **Risk Diagnosis Engine** | [risk.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/risk.md) | IPCC Risk Framework ($R = H \times E \times V$), hazard severity scoring, exposure metrics, and baseline vs. projected climate risk index. |
| 04 | **GIS & Spatial Engine** | [gis.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/gis.md) | GeoBoundaries IND-ADM2 spatial engine, GeoJSON polygon boundary resolution, point-in-polygon spatial join, and API endpoints. |
| 05 | **Frontend Architecture** | [frontend.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/frontend.md) | React + Vite + TailwindCSS SPA, interactive Leaflet climate hazard map, state management, and real-time dashboard visualization. |
| 06 | **Backend Architecture** | [backend.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/backend.md) | FastAPI asynchronous application pipeline, middleware CORS/Auth, service orchestration, dependency injection, and API routing. |
| 07 | **PostgreSQL & PostGIS Database** | [postgres.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/postgres.md) | Relational schema design, SQLAlchemy ORM models (`District`, `HazardRecord`, `AdaptationStrategy`, `QUBOModelRecord`), spatial geometries, and DB contexts. |
| 08 | **Adaptation Strategy Framework** | [adaptation.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/adaptation.md) | Climate adaptation strategy catalog, suitability matching engine, sector classification, cost-benefit ratio (CBR), and priority scoring. |
| 09 | **Knowledge Base (RAG)** | [knowledge_base.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/knowledge_base.md) | ChromaDB vector store (`v1.0.0_verified`), document ingestion (IPCC AR6, TN action plans), metadata filtering, and hybrid vector-keyword retrieval. |
| 10 | **Text Chunking Pipeline** | [chunks.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/chunks.md) | Semantic sentence-aware sliding window chunker (`chunker.py`), token limits, overlap control, document extraction, and vector index generation. |
| 11 | **District Data Catalog** | [district_data.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/district_data.md) | 38 Tamil Nadu districts dataset, climatology baselines (`district_climatology.json`), geographic centroids, vulnerability index, and verification CSV benchmarks. |
| 12 | **Quantum Optimization Flow** | [quantum_flow.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/quantum_flow.md) | Complete classical MILP $\rightarrow$ QUBO $\rightarrow$ QAOA circuit setup $\rightarrow$ Qiskit/IBM Quantum execution $\rightarrow$ Bitstring decoding flow with minimal clean code. |
| 13 | **ML Features Specification** | [ml_features.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/ml_features.md) | Strict 53-feature vector definition (15 climate/hydrological indicators + 38 one-hot district encodings) and feature generation service. |
| 14 | **Adaptation Features Specification** | [adaptation_features.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/system_summaries/adaptation_features.md) | Mathematical parameters governing strategy evaluation: risk reduction ($\Delta R$), co-benefits ($B$), cost ($C$), lead time ($T$), synergy/conflict matrix ($S_{ij}$), and budget constraints. |

---

## 🏗️ System Architecture Overview

```
                          +-----------------------------------+
                          |     React / Vite Frontend SPA     |
                          | (Leaflet Map, Dashboard, QAOAResearch)|
                          +-----------------+-----------------+
                                            | REST API
                                            v
                          +-----------------------------------+
                          |         FastAPI Backend           |
                          |  (Async Routers, CORS, Auth)      |
                          +--------+---------------+----------+
                                   |               |
         +-------------------------+               +--------------------------+
         |                                                                    |
         v                                                                    v
+------------------+     +-------------------+     +------------------+     +--------------------+
| Climate Forecast |     | ML Risk Engine    |     | RAG Vector Store |     | Quantum QAOA Engine|
| (Open-Meteo REST |     | (XGBoost 53-Feat  |     | (ChromaDB Vector |     | (MILP -> QUBO ->   |
|  & Baselines)    |     |  Multi-Hazard)    |     |  Hybrid Retrieval)|     |  Qiskit Circuit)   |
+------------------+     +-------------------+     +------------------+     +--------------------+
         |                         |                        |                         |
         +-------------------------+--------+---------------+-------------------------+
                                            |
                                            v
                                 +--------------------+
                                 | PostgreSQL/PostGIS |
                                 | DB & Spatial Engine|
                                 +--------------------+
```

---
*Generated for the Climate Adaptation & Portfolio Optimization System.*
