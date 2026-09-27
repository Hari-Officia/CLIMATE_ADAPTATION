# Quantum Multi-Agent Decision Support System for Climate Adaptation

**Scope**: Climate Adaptation ONLY  
**Geography**: Tamil Nadu, India — All 38 Districts  
**Certification State**: `PHASE_S_PASS` | `GO` | `CONDITIONALLY_CERTIFIED` | `RESEARCH_READY_WITH_LIMITATIONS`  

---

## System Overview
An enterprise decision-intelligence platform combining machine learning risk modeling, PostGIS spatial analysis, classical MILP strategy optimization, QUBO formulations, QAOA quantum experimentation, ChromaDB RAG evidence grounding, and LLM explanations for climate adaptation planning across Tamil Nadu.

## Key Features
- **38-District Coverage**: 100% coverage of Tamil Nadu districts (TN-001 to TN-038).
- **Backend Scientific Authority**: Python backend is the sole scientific authority.
- **Quantum Advantage Guardrail**: QAOA is experimental. Quantum Advantage: **NOT ESTABLISHED** ($Gap = 0.4700$).
- **19-Node Lineage Provenance**: Complete version graph hashing across all pipeline components.
- **Continuous Monitoring & Governance**: Drift engine, policy compliance, and 24h RPO / 1h RTO DR SLAs.

---

## Installation & Running Locally

### Backend
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 3000
```

### Verification & Testing
```bash
pytest tests/
python scripts/run_phase_s_verification.py
```
