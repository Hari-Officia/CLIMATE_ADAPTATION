# 02 Change Request CR-V3.1-001

**Change Request ID**: CR-V3.1-001  
**Classification**: CLASS 2 Technical / Infrastructure Hardening  
**Requester**: Engineering & Release Management  
**Baseline**: BASE-3.0.0-20260923  
**Target Release**: 3.1.0-rc1  

## Purpose & Scope

Migrate deprecated Pydantic V1 validation patterns (`@validator`, `example=`, `class Config:`, `env=`) to Pydantic V2 `@field_validator`, `@model_validator`, `SettingsConfigDict`, `ConfigDict`, `validation_alias`, and `json_schema_extra`.

**Scientific Impact**: ZERO (All decision formulas, risk calculations, QUBO $P=10.0$, QAOA $Gap=0.4700$, and 53-feature schema remain 100% untouched).
