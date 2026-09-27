# Phase I Documentation — Candidate Set Generation

## 1. Candidate Generation Workflow
`StrategyCandidateService` integrates evaluations across 14 canonical strategies and generates immutable candidate set records (`StrategyCandidateSet`).

```
District Context → StrategyApplicabilityService → Strategy Candidate Generator → Database Store (strategy_candidate_sets)
```

## 2. Immuntability & Traceability
Every generated candidate set receives a unique UUID (`CNDSET-{DISTRICT}-{HASH}`) and is stored in PostgreSQL table `strategy_candidate_sets` for auditability.
