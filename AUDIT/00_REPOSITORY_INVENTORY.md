# 00: Repository Forensic Inventory Report

**Date of Audit**: 2026-09-22
**Total Tracked Files**: 16050
**Scope**: Climate Adaptation System ONLY (Tamil Nadu, India)

## Inventory Summary by Component

| Path / Directory | Tracked Files | Total Bytes | Operational Role | Risk / Note |
|---|---|---|---|---|
| `CLAUDE_RESEARCH_PACKAGE/` | 37 | 126433 | Traceable Adaptation Knowledge System | VERIFIED |
| `backend/` | 44 | 318575 | FastAPI, Agents, SQLAlchemy DB | VERIFIED |
| `data/` | 50 | 2709636 | GeoJSON Boundaries & District Profiles | VERIFIED |
| `docs/` | 18 | 70030 | Architecture & Methods Docs | VERIFIED |
| `scripts/` | 11 | 118633 | Pipeline & Verification Utilities | VERIFIED |
| `tests/` | 10 | 19927 | Test Suite | VERIFIED |

## Detailed File Registry (First 50 Files)

| File Path | Type | Size (Bytes) | Purpose | Audit Status |
|---|---|---|---|---|
| `.env` | `no_ext` | 234 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.gitignore` | `no_ext` | 417 | Root Configuration / File | `VERIFIED_PRESENT` |
| `docker-compose.yml` | `.yml` | 309 | Root Configuration / File | `VERIFIED_PRESENT` |
| `pytest.ini` | `.ini` | 62 | Root Configuration / File | `VERIFIED_PRESENT` |
| `requirements.txt` | `.txt` | 131 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.claude\settings.local.json` | `.json` | 308 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.pytest_cache\.gitignore` | `no_ext` | 39 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.pytest_cache\CACHEDIR.TAG` | `.tag` | 191 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.pytest_cache\README.md` | `.md` | 310 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.pytest_cache\v\cache\lastfailed` | `no_ext` | 2 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.pytest_cache\v\cache\nodeids` | `no_ext` | 2252 | Root Configuration / File | `VERIFIED_PRESENT` |
| `.pytest_cache\v\cache\stepwise` | `no_ext` | 2 | Root Configuration / File | `VERIFIED_PRESENT` |
| `backend\main.py` | `.py` | 2247 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\agents\climate_agent.py` | `.py` | 876 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\agents\climate_data_agent.py` | `.py` | 16071 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\agents\risk_agent.py` | `.py` | 9136 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\auth.py` | `.py` | 4894 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\db_schema.py` | `.py` | 953 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\districts.py` | `.py` | 1498 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\forecast.py` | `.py` | 1838 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\gis.py` | `.py` | 7108 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\hazards.py` | `.py` | 9215 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\locations.py` | `.py` | 980 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\risk.py` | `.py` | 4308 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\api\system.py` | `.py` | 3081 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\data\climate_risk.db` | `.db` | 147456 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\db\config.py` | `.py` | 866 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\db\database.py` | `.py` | 2022 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\db\init_db.py` | `.py` | 7610 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\db\models.py` | `.py` | 5995 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\air_quality.py` | `.py` | 3270 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\base.py` | `.py` | 2967 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\coastal.py` | `.py` | 4349 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\cyclone.py` | `.py` | 3146 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\drought.py` | `.py` | 7286 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\extreme_rain.py` | `.py` | 3766 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\extreme_wind.py` | `.py` | 3334 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\flood.py` | `.py` | 5462 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\heatwave.py` | `.py` | 5149 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\heat_stress.py` | `.py` | 4486 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\registry.py` | `.py` | 2891 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\risk_engine.py` | `.py` | 4170 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\hazards\thunderstorm.py` | `.py` | 3215 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\risk\feature_contract.py` | `.py` | 9592 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\risk\thresholds.py` | `.py` | 687 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\schemas\auth.py` | `.py` | 559 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\schemas\district.py` | `.py` | 808 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\schemas\forecast.py` | `.py` | 1101 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\schemas\location.py` | `.py` | 426 | Backend Services & Database Models | `VERIFIED_PRESENT` |
| `backend\schemas\risk.py` | `.py` | 1238 | Backend Services & Database Models | `VERIFIED_PRESENT` |
