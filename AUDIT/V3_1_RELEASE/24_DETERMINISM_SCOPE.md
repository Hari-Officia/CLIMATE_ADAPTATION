# 24 Determinism Scope & Terminology Report

**Scope Distinctions**:
1. **DETERMINISTIC_DECISION_RECONSTRUCTION**: Composite risk, priority scores, MILP portfolios, and decision hashes reproduce 100% deterministically under fixed inputs & seeds (`seed=42`).
2. **STOCHASTIC_QAOA_EXPERIMENT**: QAOA Aer simulator statevector sampling with finite shot counts (`shots=1000`) is stochastic. Classical MILP remains authoritative.
