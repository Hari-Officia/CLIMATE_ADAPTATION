# Production Operational Runbooks

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## Runbook 1: API Outage Recovery
1. Check process liveness: `curl http://localhost:8000/api/v1/decision/health/live`
2. Inspect log file for exceptions: `tail -n 100 logs/app.log`
3. Restart FastAPI Uvicorn process: `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`

---

## Runbook 2: Model Rollback
1. Inspect active model version in `config/models/model_registry.json`.
2. Update `status` flag of active version to `DEPRECATED` and revert target artifact path to `v1.0`.
3. Restart backend service to load fallback model artifact.
