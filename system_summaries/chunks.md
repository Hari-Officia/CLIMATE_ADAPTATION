# Text Chunking Pipeline Summary

## 🧩 Overview
The **Text Chunking Pipeline** is responsible for transforming raw IPCC documents, Tamil Nadu Action Plans, and strategy reports into standardized, semantically coherent text chunks. Implemented in `backend/services/rag/chunker.py`, it ensures high precision during vector embedding and RAG retrieval.

---

## ⚙️ Chunking Strategy & Specifications

| Parameter | Value | Rationale |
|---|---|---|
| **Target Chunk Size** | `400 - 600` tokens (~1500 chars) | Optimal context size for transformer embedding models |
| **Chunk Overlap** | `50 - 80` tokens (~250 chars) | Retains context across boundaries for complex policy statements |
| **Boundary Rule** | Sentence Boundary (`.`, `\n\n`) | Prevents mid-sentence truncation |
| **Metadata Tagging** | Source ID, Section Title, Sector, District | Enables SQL/Chroma pre-filtering before semantic vector distance calculation |

---

## 🔄 Chunk Creation & Ingestion Pipeline

```
Raw Document Text (.md / .txt)
               │
               ▼
+-----------------------------------+
|     DocumentExtractor.py          | --> Cleans markdown, strips headers
+-----------------------------------+
               │
               ▼
+-----------------------------------+
|         Chunker.py                | --> Sliding window sentence-aware splitter
+-----------------------------------+
               │
               ▼
+-----------------------------------+
|      Metadata Attachment          | --> Attaches doc_id, sector, citation
+-----------------------------------+
               │
               ▼
+-----------------------------------+
|  ChromaDB Vector Store Ingestion  | --> Generates embeddings & stores
+-----------------------------------+
```

---

## 💻 Minimal Code Example

```python
# backend/services/rag/chunker.py
import re
from typing import List, Dict, Any

class SentenceAwareChunker:
    def __init__(self, target_chunk_size: int = 1500, overlap_size: int = 250):
        self.target_chunk_size = target_chunk_size
        self.overlap_size = overlap_size

    def chunk_document(self, text: str, doc_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Splits document text into overlapping sentence-aware chunks."""
        # Split into individual sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        
        current_chunk = []
        current_length = 0
        chunk_idx = 0

        for sentence in sentences:
            sentence_len = len(sentence)
            if current_length + sentence_len > self.target_chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "chunk_id": f"{doc_metadata.get('doc_id', 'doc')}_chk_{chunk_idx}",
                    "text": chunk_text,
                    "char_length": len(chunk_text),
                    **doc_metadata
                })
                chunk_idx += 1
                
                # Maintain overlap by retaining last sentence
                current_chunk = [current_chunk[-1]] if len(current_chunk) > 1 else []
                current_length = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_length += sentence_len

        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "chunk_id": f"{doc_metadata.get('doc_id', 'doc')}_chk_{chunk_idx}",
                "text": chunk_text,
                "char_length": len(chunk_text),
                **doc_metadata
            })

        return chunks
```
