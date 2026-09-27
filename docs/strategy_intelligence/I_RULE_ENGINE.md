# Phase I Documentation — Rule Engine Architecture

## 1. Engine Structure
`StrategyApplicabilityService` reads conditions from `config/master/strategy_conditions.json` and evaluates district profile features dynamically.

## 2. Hard vs Soft Conditions
- **HARD**: Failure directly sets `eligibility_status = INELIGIBLE`.
- **SOFT**: Failure logs advisory warning without excluding candidate.
