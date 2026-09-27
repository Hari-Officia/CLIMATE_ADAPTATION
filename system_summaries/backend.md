# Backend Architecture Summary

## ⚡ Overview
The **Backend Subsystem** is an asynchronous microservice framework built on **FastAPI** and **Python 3.10+**. It serves as the orchestrator connecting external NWP APIs, machine learning inference engines, vector knowledge retrieval databases, PostgreSQL spatial storage, and quantum optimization solvers.

---

## 🏗️ Architecture & Modular Router Blueprint

```
                            +--------------------------+
                            |     FastAPI main.py      |
                            | (CORS, Lifespan, DB Pool)|
                            +------------+-------------+
                                         |
         +-------------------------------+-------------------------------+
         |                               |                               |
         v                               v                               v
+------------------+           +------------------+            +-------------------+
|  api/forecast.py |           |   api/risk.py    |            |   api/qaoa.py     |
| (Open-Meteo REST)|           | (IPCC Engine)    |            | (Qiskit Solvers)  |
+------------------+           +------------------+            +-------------------+
         |                               |                               |
         v                               v                               v
+------------------+           +------------------+            +-------------------+
| ClimateDataAgent |           | FeatureEngService|            |  QUBOBuilder      |
+------------------+           +------------------+            +-------------------+
```

---

## 📡 API Router Registry

| Router Module | Prefix | Responsibility |
|---|---|---|
| `auth.py` | `/api/v1/auth` | User authentication, token issuance, RBAC permissions |
| `forecast.py` | `/api/v1/forecast` | 7-day NWP weather forecast & fallback baselines |
| `districts.py` | `/api/v1/districts` | Catalog of 38 Tamil Nadu districts & metadata |
| `hazards.py` | `/api/v1/hazards` | Multi-hazard XGBoost prediction endpoints |
| `risk.py` | `/api/v1/risk` | Composite IPCC risk calculation & hazard weightings |
| `gis.py` | `/api/v1/gis` | GeoJSON polygon boundaries & spatial lookup |
| `strategies.py` | `/api/v1/strategies` | Adaptation intervention catalog & suitability scores |
| `qubo.py` / `qaoa.py` | `/api/v1/optimization` | Quantum model construction, QUBO hashing, QAOA run |
| `rag.py` | `/api/v1/rag` | ChromaDB vector search & citation evidence cards |
| `system.py` | `/api/v1/system` | System monitoring, database health, task status |

---

## 💻 Minimal Code Example

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import forecast, risk, gis, qaoa, rag, districts

app = FastAPI(
    title="Climate Adaptation & Quantum Optimization API",
    version="1.0.0",
    docs_url="/docs"
)

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular sub-routers
app.include_router(forecast.router, prefix="/api/v1/forecast")
app.include_router(risk.router, prefix="/api/v1/risk")
app.include_router(gis.router, prefix="/api/v1/gis")
app.include_router(qaoa.router, prefix="/api/v1/optimization/qaoa")
app.include_router(rag.router, prefix="/api/v1/rag")
app.include_router(districts.router, prefix="/api/v1/districts")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "climate-backend-v1"}
```
