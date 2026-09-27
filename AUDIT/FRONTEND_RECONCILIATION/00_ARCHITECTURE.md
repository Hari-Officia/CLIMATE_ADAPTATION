# Frontend-Backend Architecture Mapping

## Flow Architecture
BACKEND SCIENTIFIC AUTHORITY
        ↓
API CONTRACT (FastAPI OpenAPI)
        ↓
TYPED FRONTEND DATA MODEL (TypeScript / React)
        ↓
UI (Presentation / Interaction Layer)
        ↓
USER

## Reconciled Capability Mapping
- Risk Analysis: Backend `/risk/{district_id}/hazards` -> React `RiskCard` & `DistrictDetail`
- Priority Score: Backend `/districts/{district_id}/priority` -> React `DistrictDetail`
- 14 Canonical Strategies: Backend `/api/v1/strategies` -> React `StrategyRegistry`
- Classical Optimization: Backend `/api/v1/districts/{district_id}/optimize` -> React `OptimizationOverview` (HIGHS MILP)
- QUBO Parity: Backend `/api/v1/qubo/build` -> React `OptimizationOverview` (P=10.0)
- QAOA Quantum Simulator: Backend `/api/v1/qaoa/benchmark` -> React `QAOAResearch` (Experimental, Gap 0.4700)
- RAG Evidence Base: Backend `/api/v1/rag/search` -> React `EvidenceCenter`
- LLM Explanation: Backend `/api/v1/explanation/{district_id}` -> React `DistrictDetail`
- Decision Lineage: Backend `/api/v1/decision/{id}/provenance` -> React `DistrictDetail`
- GIS Mapping: Backend `/gis/districts-geojson` -> React `RiskMap`
