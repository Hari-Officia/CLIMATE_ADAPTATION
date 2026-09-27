# Data Contract — Strategy Candidate Set Contract

## 1. Specification & Scope
This contract defines the output schema of **Phase I Strategy Candidate Generation** (`StrategyCandidateSet`) passed downstream to **Phase J/K Classical Strategy Optimization**.

## 2. Payload Structure
```json
{
  "candidate_set_id": "CNDSET-CHE-20260922-001",
  "district_id": "chennai",
  "priority_id": "PRIO-CHE-FLD-001",
  "hazard_ids": ["HAZ-FLD", "HAZ-HTW"],
  "strategy_ids": ["STR-DRN-001", "STR-DRN-002", "STR-WTR-001", "STR-NBS-001", "STR-BLD-002", "STR-CIN-001", "STR-EWS-001"],
  "excluded_strategy_ids": ["STR-CST-001"],
  "review_required_strategy_ids": ["STR-BLD-001"],
  "insufficient_data_strategy_ids": [],
  "evidence_summary": "7 candidate strategies passed applicability rules and Tier 1-3 evidence verification.",
  "version": "1.0.0",
  "generated_at": "2026-09-22T21:15:00Z"
}
```

## 3. Strict Compliance Rules
1. Candidates entering `strategy_ids` must be strictly `ELIGIBLE` or `CONDITIONALLY_ELIGIBLE`.
2. Quantitative scores, cost estimates, or efficacy metrics MUST NOT be generated inside this contract.
3. No strategy with `INSUFFICIENT_DATA` or `UNVERIFIED` status may enter the optimization pool without human review.
