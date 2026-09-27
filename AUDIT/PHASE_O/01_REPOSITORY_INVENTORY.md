# Phase O Repository Forensic Inventory

**Project:** Quantum Multi-Agent Decision Support System for Climate Adaptation and Mitigation Strategy Planning  
**Geography:** Tamil Nadu, India — All 38 Districts  
**Scope:** Climate Adaptation ONLY  
**Phase:** Phase O — Enterprise Decision Intelligence API & Multi-Agent Orchestration  

---

## 1. Repository Directory Structure & Module Dependency Graph

```text
PROJECT_DATA/
├── AUDIT/                       # Audit markdown and CSV reports for Phases D through O
├── backend/                     # Python FastAPI Backend Architecture
│   ├── agents/                  # Specialized Domain Agents (Climate, Risk, Data)
│   ├── api/                     # REST API Routers (Auth, Districts, Risk, Priority, Optimization, QUBO, QAOA, RAG, Explanation, Decision)
│   ├── db/                      # PostgreSQL / SQLAlchemy Engine, Session, Migrations, ORM Models
│   ├── hazards/                 # Hazard Engines (Flood, Drought, Heatwave, Cyclone, Coastal, Risk Engine)
│   ├── risk/                    # 53-Feature Contract & Risk Threshold Definitions
│   ├── schemas/                 # Pydantic Schemas for API Requests & Responses
│   ├── services/                # Core Deterministic Services (Exposure, Priority, Applicability, Optimization, QUBO, QAOA, RAG, Explanation, Orchestration)
│   └── main.py                  # FastAPI Application Entrypoint & Router Registry
├── config/                      # System Configurations & Versioning Registries
│   ├── llm/                     # LLM Model Configs & Prompts
│   ├── master/                  # Master System & Evidence Version Registries
│   ├── rag/                     # RAG Defaults & Embedding Configuration
│   ├── system/                  # System Defaults, Workflow Policies, Timeouts, Rate Limits, Feature Flags
│   └── workflows/               # Decision Workflow Pipeline Definitions
├── docs/                        # Technical Specifications, Contracts, Runbooks, Architecture Documents
│   ├── architecture/            # System Architecture, Agent Architecture, Workflow Architecture, Observability
│   ├── contracts/               # Data Handoff Contracts (RAG-to-LLM, LLM-to-UI, System Decision Contract, Phase O-to-P Contract)
│   └── operations/              # Operational Runbooks, Deployment Guides, Backup/Recovery Procedures
├── knowledge_base/              # ChromaDB SQLite Vector DB & Ingested Document Catalogs
├── schemas/                     # Master JSON Schemas for Requests, Results, Workflows, Provenance
├── scripts/                     # 38-District Batch Execution & Verification Scripts
└── tests/                       # Pytest Automated Test Suite (Phases D through O)
```

---

## 2. Component Inventory Table

| CATEGORY | PATH / SERVICE | RESPONSIBILITY | AUTHORITATIVE STORE |
|---|---|---|---|
| **Data Context** | `backend/agents/climate_data_agent.py` | Climate observations, historical rainfall & temperature | PostgreSQL `forecast_data` |
| **Risk Engine** | `backend/hazards/risk_engine.py` | 53-Feature ML Risk prediction across climate hazards | PostgreSQL `risk_results` |
| **Exposure Engine** | `backend/services/exposure_service.py` | Population, built environment & infrastructure exposure | PostgreSQL `exposure_records` |
| **Vulnerability & Resilience**| `backend/services/priority_service.py` | Socio-economic sensitivity, adaptive capacity, resilience | PostgreSQL `priority_profiles` |
| **Adaptation Priority** | `backend/services/priority_service.py` | Multi-Criteria Decision Analysis (MCDA) priority score | PostgreSQL `priority_profiles` |
| **Strategy Applicability** | `backend/services/strategy_applicability_service.py` | District eligibility filtering & constraint evaluation | PostgreSQL `strategy_district_applicability` |
| **Classical Optimization** | `backend/services/optimization/solvers/milp_solver.py` | Exact MILP portfolio optimization under constraints | PostgreSQL `adaptation_portfolios` |
| **QUBO Formulation** | `backend/services/optimization/qubo_builder.py` | Matrix encoding & constraint penalty construction | PostgreSQL `qubo_models` |
| **QAOA Optimization** | `backend/services/optimization/qaoa/qaoa_solver.py` | Quantum simulator benchmarking & circuit construction | PostgreSQL `qaoa_experiments` |
| **RAG Evidence Retrieval** | `backend/services/rag/hybrid_retriever.py` | Hybrid vector + BM25 search with metadata filtering | ChromaDB `climate_adaptation_evidence_v1` |
| **LLM Decision Explanation** | `backend/services/explanation/llm_explanation_engine.py` | Grounded explanation generation & citation enforcement | PostgreSQL `explanation_records` |
| **Multi-Agent Orchestrator**| `backend/services/orchestration/workflow_engine.py` | Multi-stage workflow coordination & provenance tracking | PostgreSQL `decision_workflows` |
| **Enterprise Decision API** | `backend/api/decision.py` | Canonical REST decision endpoints | FastAPI Router |
