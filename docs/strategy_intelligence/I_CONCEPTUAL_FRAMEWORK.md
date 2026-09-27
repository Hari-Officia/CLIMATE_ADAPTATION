# Phase I Documentation — Conceptual Framework

## 1. Overview & Architecture
Phase I establishes the **Adaptation Strategy Intelligence System** for Tamil Nadu's 38 administrative districts. It consumes upstream context from Phase E (Risk), Phase F (Exposure), Phase G (Vulnerability/Resilience), and Phase H (Adaptation Priority) to evaluate strategy applicability and construct optimization-ready candidate sets (`StrategyCandidateSet`).

```
PHASE E (Risk) + PHASE F (Exposure) + PHASE G (Vulnerability) + PHASE H (Priority)
                                 ↓
                    Strategy Applicability Engine
                                 ↓
                     Strategy Candidate Generator
                                 ↓
            StrategyCandidateSet Payload (Optimization-Ready)
```

## 2. Core Principles
1. **Provenance-First**: All strategy claims link to Tier 1-3 official sources.
2. **Deterministic Applicability**: Rules-based eligibility calculation; no LLM invention.
3. **No Arbitrary Efficacy Metrics**: Efficacy metrics remain `NULL` unless empirically verified.
