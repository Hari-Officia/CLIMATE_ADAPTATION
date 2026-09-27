# 03 NC-001 Scope & Corrective Action Plan

**Title**: Pydantic V2 Migration Warnings  
**Initial Status**: ACCEPTED_RISK  
**Current Status**: CLOSED_VERIFIED_IN_RC1  
**Target Release**: 3.1.0  

## Corrective Actions Executed

1. Refactored `backend/config.py` to `@field_validator` and `SettingsConfigDict` with `validation_alias`.
2. Refactored `backend/schemas/` (`district.py`, `forecast.py`, `auth.py`) to `model_config = ConfigDict(...)`.
3. Refactored `backend/api/` (`decision.py`, `qubo.py`, `qaoa.py`) from deprecated `example=` keyword arguments to `json_schema_extra={"example": ...}`.
4. Eliminated all `PydanticDeprecatedSince20` warnings across pytest run.
