# Phase F — Data Lineage & Traceability

## Lineage Chain Representation
```
SOURCE (e.g. SRC-CENSUS-2011)
  ↓
RAW DATASET (e.g. DS-POP-TN-001)
  ↓
INGESTION & SHA-256 CHECKSUM REGISTRATION
  ↓
POSTGIS SPATIAL OVERLAY / PIP AGGREGATION
  ↓
EXPOSURE PROFILE RECORD
  ↓
API OUTPUT CONTRACT (/api/v1/districts/{id}/risk-exposure)
```

Every derived exposure value records `source_id`, `dataset_id`, `spatial_method`, and `lineage_id` to guarantee 100% auditability without relying on LLM outputs.
