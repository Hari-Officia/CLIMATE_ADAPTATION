# Phase R — AI & Quantum Governance Policy

## 1. Scope & Objective
Governance guidelines governing Retrieval-Augmented Generation (RAG), LLM Decision Explanations, Prompt Engineering, and Quantum Strategy Optimization.

## 2. RAG & LLM Governance Rules
- **Evidence-Grounded Explanations**: LLM explanations must be strictly grounded in evidence retrieved from ChromaDB (Tier 1: Policy Documents, Tier 2: Academic Literature, Tier 3: Technical Reports).
- **Zero Hallucination Tolerance**: LLMs must not invent strategy recommendations, modify risk scores, or create unverified citations.
- **Explicit Grounding Label**: All LLM text must be explicitly labeled `GENERATED EXPLANATION` in the API and UI to distinguish explanations from underlying scientific calculations.
- **Prompt Versioning**: Prompts are stored as versioned JSON artifacts (`config/prompts/prompts_registry.json`). Live production prompts cannot be edited without a version increment and regression test.

## 3. Quantum Computing Guardrails
- **Experimental Status**: QAOA execution is classified strictly as an experimental solver.
- **Benchmark Parity**: QAOA results must always be presented alongside the exact classical MILP benchmark solution.
- **Mandatory Quantum Label**: Whenever QAOA is displayed, the UI and API must explicitly include: `Quantum Advantage: NOT ESTABLISHED` ($Gap = 0.4700$).
