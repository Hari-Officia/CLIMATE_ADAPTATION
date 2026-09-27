# Knowledge Base (RAG System) Summary

## 📚 Overview
The **Knowledge Base (RAG System)** provides verifiable, evidence-backed domain intelligence for climate adaptation decision-making. Built on **ChromaDB** and semantic embedding models, it indexes peer-reviewed IPCC reports, state action plans, and empirical case studies from `knowledge_base/v1.0.0_verified/`.

---

## 📂 Knowledge Base Structure (`v1.0.0_verified`)

```
knowledge_base/v1.0.0_verified/
├── 01_SOURCE_REGISTRY/    # Bibliographic metadata, DOIs, authority scores
├── 02_DOCUMENTS/          # Raw & cleaned Markdown texts (IPCC AR6, TNSAPCC)
├── 03_STRATEGIES/         # Structured strategy briefs & cost-benefit evidence
├── 04_EVIDENCE/          # Empirical outcome metrics & efficacy records
├── 05_DISTRICTS/         # District-level disaster management profiles
└── 06_RAG/                # Indexed ChromaDB collection files & embeddings
```

---

## 🔍 Hybrid Retrieval Architecture

```
User Query ("Heatwave mitigation in Madurai")
                    │
                    ▼
+---------------------------------------+
|        backend/services/rag           |
+-------------------+-------------------+
                    |
          +---------+---------+
          |                   |
          v                   v
+-------------------+ +-------------------+
|  ChromaDB Vector  | |   Keyword BM25    |
| Semantic Search   | |   Exact Match     |
+---------+---------+ +---------+---------+
          |                   |
          +---------+---------+
                    |
                    v
+---------------------------------------+
|  Reciprocal Rank Fusion (RRF) Re-rank |
+-------------------+-------------------+
                    |
                    v
+---------------------------------------+
| Context Chunks + Citation Cards Output|
+---------------------------------------+
```

---

## 💻 Minimal Code Example

```python
# backend/services/rag/hybrid_retriever.py
from typing import List, Dict, Any

class HybridRetriever:
    def __init__(self, chroma_client=None):
        self.chroma_client = chroma_client

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        district_filter: str = None,
        sector_filter: str = None
    ) -> List[Dict[str, Any]]:
        """Performs hybrid vector search with metadata filtering."""
        metadata_where = {}
        if district_filter:
            metadata_where["district"] = district_filter.lower()
        if sector_filter:
            metadata_where["sector"] = sector_filter.lower()

        # Simulated vector retrieval result matching ChromaDB output format
        results = [
            {
                "chunk_id": "CHK_IPCC_AR6_8492",
                "document_title": "IPCC AR6 WGII - Urban Climate Resilience",
                "text": "Cool roof implementation combined with urban canopy expansion reduces localized surface temperature by up to 2.4C during peak summer months.",
                "relevance_score": 0.912,
                "citation": "IPCC AR6 WGII Chapter 6, Section 6.3"
            }
        ]
        return results[:top_k]
```
