# Phase R — Technical Debt Register

## Active Technical Debt Inventory

| Debt ID | Component | Description | Risk | Impact | Owner Role | Target Resolution | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TD-001** | Infrastructure | Single-node PostgreSQL instance without active multi-region streaming replication | LOW | Non-HA DB deployment in staging | Operations Owner | Phase S | ACKNOWLEDGED |
| **TD-002** | RAG Engine | Local ChromaDB instance vector index size optimization for >100,000 chunks | LOW | Latency impact at extreme KB scale | Knowledge Owner | Phase S | ACKNOWLEDGED |
| **TD-003** | QAOA Engine | Quantum simulator backend limited to $p=1,2$ for 14-variable QUBO | MEDIUM | Simulator execution time for $p > 2$ | Research Owner | Phase S | ACKNOWLEDGED |
| **TD-004** | Data Ingestion | Fallback to historical climatology averages when IMD live API times out | LOW | Temporary data staleness during external API outage | Data Owner | Phase S | ACKNOWLEDGED |
| **TD-005** | API Router | Open-source Pydantic V1 field deprecation warnings during serialization | LOW | Developer noise in test output | Platform Owner | Phase S | ACKNOWLEDGED |
