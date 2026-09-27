# PHASE T AUDIT REPORT 00: REPOSITORY RECONSTRUCTION & ARCHITECTURE AUDIT

- **Status**: VERIFIED_PASSED
- **Timestamp**: 2026-09-23T14:45:00Z
- **Scope**: Repository Reconstruction, Architecture Tracing, & Data Flow Isolation Audit
- **Preserved Production Baseline**: Release `3.1.0` / `BASE-3.0.0-20260923` (IMMUTABLE)

---

## 1. Executive Summary & Repository Architecture
The platform is an enterprise-certified climate adaptation decision-intelligence platform for all 38 districts of Tamil Nadu, India. The production system (`3.1.0`) relies exclusively on classical HIGHS MILP for portfolio optimization.

The **Quantum Advantage Research Track** operates completely decoupled under `research/quantum_advantage/`.

---

## 2. Identified Data & Model Flow

```
[Production Strategy & District DB]
            │
            ▼
 [QUBOBuilder / DB Service] ──► CanonicalModelInstance (N=14 candidate strategies, K=5, P=10.0)
                                        │
     ┌──────────────────────────────────┼──────────────────────────────────┐
     ▼                                  ▼                                  ▼
[Exact Enumeration]               [HIGHS MILP]                      [QUBOBuilder]
 (2^14 = 16,384)                (Classical Exact)                   (QUBO Matrix Q)
     │                                  │                                  │
     └──────────────────────────────────┼──────────────────────────────────┘
                                        ▼
                                 [QAOASolver] ──► AerSimulator (Statevector, p=2, 1024 shots)
                                        │
                                        ▼
                           [IndependentEvaluator]
```

---

## 3. Inspected Core Files & Function Registry
- `backend/services/optimization/qubo_builder.py`: Authoritative QUBO Builder (`build_qubo`).
- `backend/services/optimization/solvers/exact_solver.py`: Classical Exact Solver.
- `backend/services/optimization/qaoa/qaoa_solver.py`: Backend QAOA Solver Engine.
- `research/quantum_advantage/instances/instance_generator.py`: Instance Generator (`generate_family_a_district`).
- `research/quantum_advantage/classical/classical_solvers.py`: Classical Benchmarks (MILP, Exact, Greedy, SA).
- `research/quantum_advantage/qaoa/qaoa_experiment_engine.py`: Multi-Seed QAOA Experiment Engine.
- `research/quantum_advantage/statistics/statistical_analyzer.py`: Protocol v2 Statistical Analyzer.
- `research/quantum_advantage/independent_verification/independent_verifier.py`: Decoupled Verifier.
- `scripts/run_quantum_advantage_benchmark.py`: Master Research Benchmark Runner.

---

## 4. Production / Research Isolation Verification
- **Isolation Status**: VERIFIED IMMUTABLE.
- Research track modules in `research/quantum_advantage/` do NOT alter production models, risk engines, 53-feature vectors, or API routes.
