# System Monitoring & Logging Specification — Review II

## 1. Overview
The system monitoring architecture tracks multi-agent performance, model availability, network latency, database health, and operational error rates.

---

## 2. Monitored Components

| Component | Check Frequency | Healthy State Criteria | Fallback Behavior |
|---|---|---|---|
| **API Gateway** | Continuous | HTTP 200 on `/system/status` | Process restart via supervisor |
| **Database Engine** | Per request | Active connection pool | Automatic SQLite fallback |
| **GeoJSON Topology** | Startup & on demand | 38 valid polygons, CRS84 | Fallback to cached boundary geometries |
| **Climate Acquisition Agent** | Hourly / Per request | Open-Meteo response $\le 3\text{s}$ | Disk cache / Climatological synthetic normal |
| **Risk Agent** | Per request | 3 active XGBoost models, 53 features | Safe default risk probability flags |

---

## 3. Logging Architecture

Operational logs are persisted to the database in table `system_logs`:
- `timestamp`: UTC ISO-8601 timestamp.
- `level`: `INFO`, `WARN`, `ERROR`.
- `component`: Source identifier (e.g., `ClimateAgent`, `RiskAgent`, `Auth`, `Admin`).
- `message`: Diagnostic description.
- `details_json`: Optional contextual parameters or payload summary.
