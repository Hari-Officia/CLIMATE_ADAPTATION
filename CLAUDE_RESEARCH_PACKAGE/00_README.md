# Tamil Nadu Climate Adaptation Knowledge System (`CLAUDE_RESEARCH_PACKAGE`)

This package provides a **traceable, evidence-grounded, Tamil-Nadu-specific climate adaptation knowledge base** covering 38 districts, 10 adaptation domains, climate hazards, GIS applicability conditions, technology dependencies, and RAG chunk metadata.

## Key Package Principles
- **100% Traceable**: Every strategy and claim links directly to registered Tier 1-4 source documents with page numbers.
- **Strict "No Invention" Guardrails**: Unverified numeric metrics are recorded as `NULL` to prevent LLM hallucination.
- **Full Geographic Coverage**: Includes spatial profiles and strategy applicability matrices for all 38 Tamil Nadu districts.
- **All 10 Domains Covered**: Drainage, Water Management, Land Use, Nature-Based, Built Infrastructure, Terrain/GIS, Critical Infrastructure, Early Warning, Heat Resilience, and Coastal Resilience.

## Package Architecture

```
CLAUDE_RESEARCH_PACKAGE/
├── 00_README.md
├── 01_SOURCE_REGISTRY/      (Source CSV/JSON, Hierarchy Policy)
├── 02_DOCUMENTS/            (Manifest, Download Logs, Checksums)
├── 03_STRATEGIES/           (Normalized Strategies, 10 Domains, Mappings)
├── 04_EVIDENCE/             (Evidence Claims CSV/JSONL, Evidence Matrix)
├── 05_DISTRICTS/            (38 District Profiles, Hazards, Applicability)
├── 06_RAG/                  (Processed Documents, Semantic Chunks JSONL, Schema)
├── 07_OPTIMIZATION/         (QUBO Candidate Attributes, Pairwise Interactions)
├── 08_RESEARCH/             (Papers Registry, Literature Matrix, Research Gaps)
├── 09_QA/                   (Conflicts, Human Review Queue, Knowledge Gaps, Audit Report)
└── 10_METHODOLOGY/          (Extraction, Scoring, Source & Provenance Policies)
```
