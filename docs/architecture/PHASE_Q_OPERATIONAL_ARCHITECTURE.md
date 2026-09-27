# Phase Q Operational Architecture Specification

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. End-to-End Operational Pipeline

```
[User Browser / GIS UI]
        │
        ▼
[Frontend React SPA (Nginx / Vite Port 80/3000)]
        │ (Axios REST + Security Headers)
        ▼
[Backend FastAPI Engine (Uvicorn Port 8000)]
        ├── [Auth & Rate Limiter]
        ├── [Pydantic Settings Validator]
        ├── [Master Decision Orchestrator]
        │       ├── [Risk ML Model Service (XGBoost)]
        │       ├── [MCDA Adaptation Priority Engine]
        │       ├── [Classical MILP Solver]
        │       ├── [QUBO Matrix Builder]
        │       ├── [QAOA Simulator (Qiskit p=1..3)]
        │       ├── [ChromaDB Vector Store RAG]
        │       └── [LLM Explanation Generator]
        └── [PostgreSQL + PostGIS Authority Database]
```

---

## 2. Operational Monitoring & Health Probes

- `/api/v1/decision/health/live`: Liveness probe.
- `/api/v1/decision/health/ready`: Readiness probe (verifies DB connection).
- `/api/v1/decision/health`: Full service status breakdown.
