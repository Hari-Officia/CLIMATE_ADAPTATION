# 00 Repository Reconstruction & Audit Inventory

**Baseline**: BASE-3.0.0-20260923  
**Target Release**: 3.1.0-rc1  
**Status**: COMPLETE  

## Workspace Reconstruction Inventory

1. **Backend**: FastAPI REST services (`/api/v1/decision`, `/api/v1/hazards`, `/api/v1/qubo`, `/api/v1/qaoa`, `/api/v1/rag`, `/api/v1/auth`, etc.)
2. **Frontend**: React + Vite + Tailwind CSS + MapLibre GIS Dashboard
3. **Database**: PostgreSQL 15 + PostGIS extension + SQLAlchemy ORM models
4. **Models**: XGBoost model artifacts (`flood_xgboost.pkl`, `drought_xgboost.pkl`, `heatwave_xgboost.pkl`)
5. **Feature Pipelines**: 53-feature vector preprocessing engine (`backend/services/feature_engineering.py`)
6. **GIS Engine**: 38 Tamil Nadu district geometries + EPSG:4326 point-in-polygon spatial join (`backend/services/geocoding_pip.py`)
7. **Optimization**: HIGHS MILP solver + exact brute force solver + greedy baseline (`backend/services/optimization/`)
8. **QUBO Bridge**: Quadratic Unconstrained Binary Optimization formulation with $P=10.0$ penalty (`backend/services/optimization/qubo_builder.py`)
9. **QAOA Simulator**: Qiskit Aer $p=1,2,3,4$ circuit simulator ($Gap = 0.4700$, Quantum Advantage NOT ESTABLISHED)
10. **RAG Evidence**: Chroma vector store + hybrid BM25/vector retriever + Tamil Nadu source hierarchy (`backend/services/rag/`)
11. **LLM Explanations**: Read-only structured decision explanation formatter (`backend/services/llm/`)
12. **Governance**: Quarterly review, NC tracking (NC-001, NC-002), change management, baseline protection, and independent verification.
