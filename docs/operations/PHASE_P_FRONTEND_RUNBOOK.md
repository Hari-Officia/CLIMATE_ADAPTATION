# Phase P Frontend Runbook & Operational Procedures

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. Local Development & Server Startup

1. **Backend Server (FastAPI):**
   ```bash
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```
2. **Frontend Dev Server (Vite):**
   ```bash
   cd frontend
   npm run dev -- --host 127.0.0.1 --port 3000
   ```

---

## 2. Production Build & Static Asset Generation

```bash
cd frontend
npm run build
```
Build output artifacts are stored in `frontend/dist/`.

---

## 3. Frontend Error Recovery & Health Checks

- If backend API goes down: App automatically renders a global **Degraded Mode Banner** ("Backend service unavailable. Displaying static geometry and offline cache where available.").
- System Health endpoint is monitored via `/system/health` every 30 seconds.
