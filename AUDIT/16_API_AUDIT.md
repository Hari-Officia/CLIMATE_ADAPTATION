# 16: FastAPI Service Audit Report

## Service Endpoints & Status

| Endpoint | Method | Operational Role | Audit Status |
|---|---|---|---|
| `/auth/login` | `POST` | User authentication & JWT issuance | VERIFIED |
| `/auth/me` | `GET` | Current user token validation | VERIFIED |
| `/districts/{id}` | `GET` | District baseline profile query | VERIFIED |
| `/locations/search` | `GET` | Geocoding & landmark lookup | VERIFIED |
| `/risk/district/{id}` | `GET` | Multi-hazard risk prediction | VERIFIED |
| `/system/status` | `GET` | Database & system health check | VERIFIED |
