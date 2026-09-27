# Phase N Repository Forensic Inventory

**Project:** Quantum Multi-Agent Decision Support System for Climate Adaptation and Mitigation Strategy Planning  
**Geography:** Tamil Nadu, India — All 38 Districts  
**Scope:** Climate Adaptation ONLY  
**Phase:** Phase N — Enterprise RAG & LLM Decision Explanation  

---

## 1. Directory & File Inventory

The complete codebase and repository state for Phase N was audited. Below is the inventory of authoritative directory trees, services, schemas, and database components.

### 1.1 Knowledge Base & Vector Index
- `knowledge_base/chroma/chroma.sqlite3`: ChromaDB SQLite vector store database storing semantic embeddings.
- `knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/`:
  - `sources.csv`, `sources.json`: 8 Tier-ranked source records (TNGCC, CCAP 2050, SDMP 2023-2030, NDMA, IPCC AR6).
  - `source_hierarchy.md`: Tiers 1 through 6 authoritative source ordering rules.
- `knowledge_base/v1.0.0_verified/02_DOCUMENTS/`: `download_log.csv`, `manifest.csv`.
- `knowledge_base/v1.0.0_verified/03_STRATEGIES/`: Canonical strategy definitions, conditions, hazard mappings, and sector links.
- `knowledge_base/v1.0.0_verified/04_EVIDENCE/`:
  - `evidence_claims.csv`, `evidence_claims.jsonl`: Extracted evidence claim objects with claim IDs, page numbers, sections, units, and strength.
  - `evidence_matrix.csv`: Strategy-to-claim mapping matrix.
- `knowledge_base/v1.0.0_verified/06_RAG/`:
  - `documents.json`: Document provenance records with document IDs, file hashes, titles, and publication years.
  - `chunks.jsonl`: Metadata-aware chunks with chunk IDs, source tiers, page numbers, sections, and tags.
  - `metadata_schema.json`: JSON schema for RAG chunk metadata validation.

### 1.2 Backend Architecture & Services (`backend/`)
- `backend/db/database.py`: SQLAlchemy engine, session maker, and PostgreSQL connection pool.
- `backend/db/models.py`: PostgreSQL ORM schemas for districts, risk, exposure, vulnerability, priority, strategies, QUBO models, QAOA experiments, evidence claims, citations, and explanations.
- `backend/services/rag/`:
  - `document_extractor.py`: PDF/TXT/HTML document text extractor preserving pages and sections with SHA-256 hashing.
  - `chunker.py`: Metadata-aware semantic chunker preserving headings, paragraphs, and tables.
  - `hybrid_retriever.py`: Multi-stage hybrid retriever (vector search + BM25 keyword matching + metadata filtering + reranking).
  - `evidence_linker.py`: Strategy-evidence linker and conflict detection manager.
- `backend/services/explanation/`:
  - `context_assembler.py`: Assembles structured context packet (district, risk, priority, candidate strategies, selected portfolio, QAOA metrics, evidence packet) with SHA-256 context packet hash.
  - `llm_explanation_engine.py`: Evidence-grounded explanation engine enforcing strict system prompts.
  - `output_validator.py`: Post-generation output validator enforcing JSON schema, numeric consistency, entity consistency, and unsupported claim detection.
  - `citation_enforcer.py`: Citation ID validator enforcing backend citation traceability and rejecting fabricated citations.
  - `staleness_checker.py`: Detects context hash mismatches (`STALE_CONTEXT`) on data/knowledge-base updates.
- `backend/api/`:
  - `rag.py`: RAG search, document, source, claim, and strategy evidence API endpoints.
  - `explanation.py`: Decision explanation generation, validation, and citation detail endpoints.
  - `main.py`: FastAPI application entrypoint with RBAC middleware and router registrations.

### 1.3 Configuration & Schemas (`config/`, `schemas/`, `docs/contracts/`)
- `config/rag/rag_defaults.json`: Default RAG parameters (embedding model, top_k, BM25 weights, reranker thresholds).
- `config/llm/models.json`: LLM provider, model version, temperature, top_p, token budget configuration.
- `config/llm/prompts.json`: System prompt templates and explanation prompt specifications.
- `schemas/`: JSON schemas for `document`, `evidence_claim`, `evidence_link`, `evidence_conflict`, `citation`, `rag_query`, `rag_result`, `explanation`, `explanation_claim`, `human_review`, `knowledge_base_version`.
- `docs/contracts/`:
  - `rag_to_llm_contract.md`: Handoff schema between RAG context assembler and LLM engine.
  - `llm_to_ui_contract.md`: Handoff schema between LLM engine and frontend decision UI.
  - `phase_n_to_phase_o_contract.md`: Contract between Phase N decision explanation system and Phase O orchestration API.

---

## 2. Forensic Inventory Summary Table

| COMPONENT | PATH | PURPOSE | STATUS |
|---|---|---|---|
| **ChromaDB Vector DB** | `knowledge_base/chroma/chroma.sqlite3` | Vector indexing for semantic retrieval | Active |
| **Source Registry** | `knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY` | Authoritative source metadata & hierarchy | Active |
| **Document Store** | `knowledge_base/v1.0.0_verified/02_DOCUMENTS` | Ingested PDF/TXT documents & manifests | Active |
| **Evidence Claims** | `knowledge_base/v1.0.0_verified/04_EVIDENCE` | Granular factual & quantitative evidence claims | Active |
| **RAG Chunks** | `knowledge_base/v1.0.0_verified/06_RAG/chunks.jsonl` | Chunked text with source provenance | Active |
| **RAG Service** | `backend/services/rag/` | Text extraction, chunking, retrieval, linking | Active |
| **LLM Service** | `backend/services/explanation/` | Grounded decision context explanation engine | Active |
| **PostgreSQL Models** | `backend/db/models.py` | Authoritative DB records for claims, citations, explanations | Active |
| **API Endpoints** | `backend/api/rag.py`, `backend/api/explanation.py` | FastAPI REST endpoints for RAG & explanation | Active |
