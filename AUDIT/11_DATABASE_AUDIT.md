# 11: Database & PostGIS Schema Audit Report

## Database Engine & Connection
- **Primary Engine**: PostgreSQL 18 with PostGIS 3.6 (`postgresql+psycopg://...`)
- **Database Name**: `climate_platform`
- **Backup Engine**: Local SQLite (`backend/data/climate_risk.db`)
- **Spatial Extension**: PostGIS enabled (`SELECT PostGIS_Version();` returned 3.6)

## Schema Integrity Table

| Table Name | PostgreSQL Record Count | SQLite Backup Record Count | Consistency Status |
|---|---|---|---|
| `users` | 2 | 2 | MATCHED |
| `districts` | 38 | 38 | MATCHED |
| `district_profiles` | 38 | 38 | MATCHED |
| `locations` | 8 | 8 | MATCHED |
| `model_registry` | 3 | 3 | MATCHED |
| `system_logs` | 20 | 20 | MATCHED |
| `forecast_runs` | 0 | 0 | MATCHED |
| `forecast_data` | 0 | 0 | MATCHED |
| `risk_results` | 0 | 0 | MATCHED |
