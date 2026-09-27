# Phase P Frontend Architecture Specification

**Project:** Quantum Multi-Agent Decision Support System for Climate Adaptation and Mitigation Strategy Planning  
**Phase:** Phase P — Enterprise GIS Decision Intelligence Interface & UI  
**Geography:** Tamil Nadu, India (All 38 Districts)  

---

## 1. System Design & Architectural Overview

The Phase P Frontend Architecture is built as a single-page application (SPA) using React 19, Vite, Tailwind CSS, Leaflet, and Axios. It functions strictly as a presentation and spatial interaction layer for the Phase O FastAPI Decision Intelligence Backend (`http://127.0.0.1:8000`).

### Master Architecture Principle
```
+------------------------------------------------------------------------+
|                            USER INTERFACE                              |
|   Master GIS Map | District Search | Deep-Dive Tabs | Portfolio Views   |
+------------------------------------------------------------------------+
                                   |
                         Axios Central API Client
                                   |
                                   v
+------------------------------------------------------------------------+
|                          FASTAPI BACKEND                               |
|   /api/v1/decision/analyze | /gis/districts | /risk | /qaoa | /rag     |
+------------------------------------------------------------------------+
                                   |
                                   v
+------------------------------------------------------------------------+
|                      POSTGIS / DATABASE / ENGINES                      |
|   Spatial Geometry | Risk ML | MILP Solver | QAOA | RAG Knowledge Base  |
+------------------------------------------------------------------------+
```

---

## 2. Directory Layout & Modular Structure

- `frontend/src/api/`: Centralized HTTP endpoints (`client.js`, `decision.js`, `gis.js`, `evidence.js`, `workflow.js`).
- `frontend/src/components/`: Modular React components (`TamilNaduMap.jsx`, `DistrictSearchSelector.jsx`, `RiskCard.jsx`, `PortfolioCard.jsx`, `QAOAPanel.jsx`, `EvidenceViewer.jsx`, `ExplanationPanel.jsx`, `ProvenanceGraph.jsx`, `WorkflowTracker.jsx`, `Sidebar.jsx`).
- `frontend/src/pages/`: Page views (`Dashboard.jsx`, `DistrictDetail.jsx`, `RiskMapPage.jsx`, `OptimizationPage.jsx`, `EvidencePage.jsx`, `MethodologyPage.jsx`, `SourcesPage.jsx`, `SystemStatusPage.jsx`).
- `frontend/src/context/`: Context state managers (`AuthContext.jsx`, `DistrictContext.jsx`).
- `frontend/src/schemas/`: Client-side JSON schema validators for presentation data.
- `frontend/src/utils/`: Formatting, color mapping, and coordinate bounds helpers.

---

## 3. Strict Non-Recalculation Contract

The frontend enforces strict read-only consumption of backend calculations:
1. **Risk Scores:** Rendered exactly as returned by `/risk` or `/decision`.
2. **Adaptation Priority:** Displayed using backend horizon labels (`IMMEDIATE`, `SHORT_TERM`, `MEDIUM_TERM`, `LONG_TERM`).
3. **MILP Portfolio:** Selected strategies are rendered from backend binary decision vectors $x \in \{0,1\}^N$.
4. **QAOA Benchmarks:** Gap ($0.4700$) and feasibility metrics rendered without recalculation.
5. **Citations & RAG Claims:** Displayed with immutable citation badges referencing primary document metadata.
