# Quantum Multi-Agent Decision Support System for Climate Adaptation

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-3.0.0-green.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.2.8-blue.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.2.2-purple.svg)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4.17-38bdf8.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise decision-intelligence platform combining machine learning risk modeling, PostGIS spatial analysis, classical MILP strategy optimization, QUBO formulations, QAOA quantum experimentation, ChromaDB RAG evidence grounding, and LLM explanations for climate adaptation planning across Tamil Nadu.

---

## Key Highlights

- **Full 38-District Coverage**: 100% coverage of Tamil Nadu districts (TN-001 to TN-038) across multi-hazard exposure, vulnerability, and resilience dimensions.
- **Backend Scientific Authority**: High-performance Python/FastAPI backend acts as the single source of truth for all calculations, scoring, and optimization.
- **Multi-Hazard ML Engines**: Calibrated XGBoost models for **Drought** (SPI-3/SPI-6, soil moisture), **Flood** (elevation, rainfall intensity, drainage), and **Heatwave** (temperature thresholds, humidity).
- **Exact MILP & QAOA Quantum Solvers**: Classical Mixed Integer Linear Programming (CBC / PuLP) paired with Quadratic Unconstrained Binary Optimization (QUBO) and Quantum Approximate Optimization Algorithm (QAOA) via Qiskit.
- **Explainable AI & RAG Evidence Center**: SHAP feature importance, rule-based decision trees, and ChromaDB-grounded literature references.
- **Interactive GIS Map & Strategy Registry**: Leaflet-powered GIS district choropleths, portfolio explorers, and actionable adaptation action matrices.

---

## Architecture Overview

```
                                  +----------------------------+
                                  |   Vite + React Frontend    |
                                  |   (Leaflet GIS, Recharts)  |
                                  +--------------+-------------+
                                                 | HTTP / REST
                                                 v
                                  +----------------------------+
                                  |   FastAPI Backend Core     |
                                  |   (Port 8000, 20+ Routers) |
                                  +--------------+-------------+
                                                 |
         +-----------------------+---------------+-----------------------+
         |                       |                               |
         v                       v                               v
+-----------------+     +-----------------+             +-----------------+
| Hazard & Risk   |     | Strategy Engine |             | Optimization    |
| ML Models       |     | & Applicability |             | (MILP / QUBO /  |
| (XGBoost / SPI) |     | (38 Districts)  |             |  QAOA Qiskit)   |
+-----------------+     +-----------------+             +-----------------+
         |                       |                               |
         +-----------------------+---------------+---------------+
                                                 |
                                                 v
                                  +----------------------------+
                                  |  Spatial & Data Tier       |
                                  |  (SQLite, GeoJSON, Caches) |
                                  +----------------------------+
```

---

## Repository Structure

```
├── backend/                  # FastAPI Application Core
│   ├── agents/               # Multi-agent decision logic
│   ├── api/                  # REST endpoints (hazards, risk, optimization, etc.)
│   ├── db/                   # Database models & seeding scripts
│   ├── hazards/              # ML hazard engines (drought, flood, heatwave)
│   ├── schemas/              # Pydantic schemas & validation
│   ├── services/             # Optimization, spatial, & model services
│   └── main.py               # Application entrypoint
├── frontend/                 # Vite + React Modern Web Application
│   ├── src/                  # Components, Pages, Context, Hooks
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite build & dev config
├── Models/                   # Pre-trained ML model artifacts
├── config/                   # Master strategy taxonomies & schemas
├── data/                     # District data, cached forecasts, & GeoJSON layers
├── database/                 # SQL schemas, constraints, and seed scripts
├── docs/                     # Architectural, risk diagnosis, & rule documentation
├── scripts/                  # Data pipelines, GIS processing, & validation
└── tests/                    # Backend test suites & pytest config
```

---

## Quickstart Guide

### Prerequisites

- **Python**: Version `3.10` or higher
- **Node.js**: Version `18.0` or higher (Node 20+ recommended)
- **Git**

---

### 1. Backend Setup

1. **Navigate to project root and create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API Server**:
   ```bash
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```

   The backend will automatically initialize and seed the database on startup.
   - API Root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Interactive Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 2. Frontend Setup

1. **Open a new terminal and navigate to `frontend`**:
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev -- --host 127.0.0.1 --port 3000
   ```

4. **Access the application**:
   - Open your browser at [http://127.0.0.1:3000](http://127.0.0.1:3000)

---

### 3. Production Build

To build the frontend for production deployment:
```bash
cd frontend
npm run build
npm run preview
```

---

## Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | System health check & metadata |
| `GET` | `/districts` | List all 38 Tamil Nadu districts |
| `GET` | `/hazards/{hazard_type}` | Hazard risk evaluation (`drought`, `flood`, `heatwave`) |
| `GET` | `/risk/district/{district_id}` | Comprehensive district risk scoring & breakdown |
| `GET` | `/gis/districts` | GeoJSON polygons for Tamil Nadu districts |
| `POST` | `/api/v1/optimization/solve` | Execute classical MILP adaptation optimization |
| `POST` | `/api/v1/qaoa/solve` | Execute QAOA quantum optimization circuit |
| `GET` | `/system/status` | Operational status of all system components |

---

## Verification & Testing

Run unit and integration test suites:
```bash
pytest tests/
python scripts/test_hazards_api.py
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
