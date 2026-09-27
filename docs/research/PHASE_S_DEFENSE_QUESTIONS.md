# Phase S — Thesis & Technical Review Defense Guide

Factual preparation for academic thesis defense, technical project review, and peer evaluation of the Quantum Multi-Agent Decision Support System for Climate Adaptation.

---

## 1. System Architecture & Multi-Agent Design

### Q1: Why use a multi-agent architecture for climate adaptation?
**Answer**: Climate adaptation planning requires integrating heterogeneous domain modules (climatology, spatial GIS, socio-economic vulnerability, classical MILP optimization, quantum QUBO formulation, RAG evidence retrieval, and LLM explanation generation). A multi-agent orchestrator (`MasterDecisionOrchestrator`) decouples domain calculations while maintaining a strict deterministic state graph (`DecisionWorkflowState`) with 19-node version context hashing.

### Q2: Why use LangGraph for orchestration?
**Answer**: LangGraph provides explicit, observable state machine transitions, preventing silent branch failures, enabling idempotency caching, and ensuring that stage execution errors fail gracefully into controlled degraded states without crashing the service.

---

## 2. Machine Learning & Risk Modeling

### Q3: How are climate risks predicted?
**Answer**: Risk modeling uses XGBoost classifiers trained on a 53-feature contract (15 continuous climatology/anomaly metrics including SPI-3, SPI-6, and rainfall anomalies, plus 38 one-hot district spatial indicators). Risk scores are mapped into discrete severity classes (`HIGH`, `MEDIUM`, `LOW`, `UNAVAILABLE`) based on centralized backend thresholds.

### Q4: How is data leakage controlled in ML pipelines?
**Answer**: Strict temporal splitting ($Train < Validation < Test$) is enforced. Spatial features are encoded using fixed district indicators rather than target statistics, preventing spatial data leakage across districts.

---

## 3. Classical Optimization vs. QUBO & QAOA

### Q5: Why formulate the strategy optimization as a MILP?
**Answer**: Selecting an optimal portfolio of adaptation strategies under district budget constraints, strategy compatibility rules, and multi-hazard coverage requirements is a NP-hard combinatorial knapsack problem. PuLP MILP solver provides exact deterministic benchmarks.

### Q6: How is the MILP converted into a QUBO?
**Answer**: Binary variables $x_i \in \{0,1\}$ represent strategy selection. Objective benefits $c_i$ are mapped into quadratic diagonal terms $-c_i x_i$. Budget constraints $\sum w_i x_i \le B$ are converted into quadratic penalty terms $P(\sum w_i x_i - B)^2$ with penalty parameter $P=10.0$, forming the symmetric QUBO matrix $Q$.

### Q7: Why test QAOA on a quantum simulator?
**Answer**: QAOA (Quantum Approximate Optimization Algorithm) evaluates how variational quantum algorithms scale for combinatorial climate optimization. Current execution uses Qiskit Aer statevector simulator for $p=1,2,3$ depths with 1024 shots.

### Q8: Is Quantum Advantage proven or claimed?
**Answer**: **NO. Quantum Advantage is NOT ESTABLISHED.** The current QAOA objective gap is $0.4700$ relative to the exact classical MILP benchmark. QAOA remains strictly an experimental research solver.

---

## 4. RAG Evidence Grounding & LLM Explanations

### Q9: How are LLM hallucinations prevented?
**Answer**: LLMs are restricted strictly to explanation generation (`EXPLANATION ONLY`). Explanations must be grounded in vector evidence retrieved from ChromaDB (Tier 1: SAPCC/IPCC, Tier 2: Academic literature, Tier 3: Technical reports). Citations undergo 100% automated validation, and text is explicitly labeled `GENERATED EXPLANATION`.

---

## 5. Provenance, Security & Disaster Recovery

### Q10: How is decision reproducibility guaranteed?
**Answer**: Every decision computes a SHA-256 context hash over the 19 pipeline components (Application, DB, Data, Feature, Model, Risk, Exposure, Vulnerability, Resilience, Priority, Strategy, MILP, QUBO, QAOA, KB, Evidence, Prompt, LLM, Decision). Rerunning the workflow with identical inputs produces the identical provenance context hash.

### Q11: What is the Disaster Recovery SLA?
**Answer**: Automated backup scripts (`scripts/backup_db.py`) ensure an RPO SLA of < 24 hours. Isolated restore testing (`scripts/restore_db.py`) achieves an RTO SLA of < 1 hour.
