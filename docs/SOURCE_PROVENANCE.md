# Source Provenance & Scientific Evidence Audit Trail

**Version**: `v1.0.0_verified`  
**System Domain**: Climate Adaptation Knowledge Engineering  

---

## 1. Source Hierarchy & Evidence Policy

To guarantee zero hallucination and strict authority compliance, all climate adaptation strategies, applicability conditions, and evidence claims in this knowledge base adhere to a strict four-tiered source hierarchy:

```
+-------------------------------------------------------------------------+
| TIER 1: Tamil Nadu Official State Policies, Frameworks & Missions       |
| (TNCCM, TN State Action Plan, TNSDMA, GCC, WRD, Wetlands Mission, etc.) |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| TIER 2: National Indian Technical Guidelines & Authorities              |
| (NDMA, CGWB, IMD, CWC, MoEFCC, MoHUA, BIS)                              |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| TIER 3: International Intergovernmental Consensus Assessment Reports    |
| (IPCC AR6 WGII, UNDRR, WMO, WHO, UN-Habitat, World Bank)                |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| TIER 4: Peer-Reviewed Empirical Scientific Literature                   |
| (IIT Madras, Anna University, High-Impact Journal Research)             |
+-------------------------------------------------------------------------+
```

---

## 2. Authoritative Source Master Registry

| Source ID | Document Title | Institution / Agency | Tier Grade | Geographic Scope | Verified Document URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TN-ADAPT-001` | Tamil Nadu District Climate Change Risk Reduction & Adaptation Framework | Dept of Environment & Climate Change, Govt of TN | Tier 1 | State (38 Districts) | `https://www.tn.gov.in/environment/tnccdap` |
| `TN-DCAPT-002` | District Climate Action Prioritisation Tool (DCAPT) User Guide | Tamil Nadu Climate Change Mission (TNCCM) | Tier 1 | District Level | `https://tnclimate.tn.gov.in/dcapt` |
| `TN-CAP-003` | Chennai Climate Action Plan (CCAP) 2050 | Greater Chennai Corporation & C40 Cities | Tier 1 | Chennai Metropolitan | `https://chennaicorporation.gov.in/ccap` |
| `TN-SDMP-004` | Tamil Nadu State Disaster Management Plan 2023-2030 | TN State Disaster Management Authority (TNSDMA) | Tier 1 | State (38 Districts) | `https://tnsdma.tn.gov.in/sdmp` |
| `NAT-NDMA-001` | NDMA National Guidelines for Management of Urban Flooding | National Disaster Management Authority (NDMA) | Tier 2 | National (India) | `https://ndma.gov.in/guidelines/urban-flooding` |
| `NAT-CGWB-002` | Master Plan for Artificial Recharge to Groundwater in India | Central Ground Water Board (CGWB) | Tier 2 | National (India) | `https://cgwb.gov.in/master_plan_recharge.html` |
| `IPCC-AR6-001` | IPCC AR6 WGII Chapter 6: Cities, Settlements & Infrastructure | Intergovernmental Panel on Climate Change | Tier 3 | Global Urban | `https://www.ipcc.ch/report/ar6/wg2/chapter/chapter-6/` |
| `RES-TN-001` | Evaluating Blue-Green Infrastructure for Coastal Cities of TN | IIT Madras & Anna University | Tier 4 | Coastal Tamil Nadu | `https://doi.org/10.1016/j.jenvman.2024.119850` |

---

## 3. Strict Non-Invented Numerical Metric Policy

Per system safety and scientific integrity guidelines:
- **Cost Figures**: Cost values are categorized qualitatively (`LOW`, `MEDIUM`, `HIGH`). The cost basis is explicitly flagged as `QUALITATIVE_ONLY`. No invented numeric monetary figures are introduced unless backed by an explicit statutory government budget line.
- **Effectiveness Metrics**: Overall effectiveness is logged as `QUALITATIVE_ONLY` with textually traceable evidence in `evidence_claims.csv`. Numerical risk reduction percentages are recorded as `NOT_AVAILABLE` or `NULL` where quantitative field monitoring is absent.
- **Resource Quantities**: Water, energy, and land requirements are expressed as qualitative categorical levels (`NONE`, `LOW`, `MEDIUM`, `HIGH`).

---

## 4. RAG Evidence Traceability Audit Trail

Every canonical strategy is linked to at least one verified claim in `evidence_claims.csv`:
- `STR-DRN-001` -> `EVD-0001` (Source: `TN-CAP-003`, Section 4.2)
- `STR-DRN-002` -> `EVD-0002` (Source: `NAT-NDMA-001`, Chapter 5)
- `STR-WTR-001` -> `EVD-0003` (Source: `TN-ADAPT-001`, Section 3.2)
- `STR-WTR-002` -> `EVD-0004` (Source: `TN-DCAPT-002`, Module 2)
- `STR-LND-001` -> `EVD-0005` (Source: `TN-ADAPT-001`, Section 5.1)
- `STR-LND-002` -> `EVD-0006` (Source: `TN-CAP-003`, Section 3.1)
- `STR-NBS-001` -> `EVD-0007` (Source: `RES-TN-001`, Section 3.3)
- `STR-NBS-002` -> `EVD-0008` (Source: `TN-ADAPT-001`, Section 4.4)
- `STR-BLT-001` -> `EVD-0009` (Source: `TN-SDMP-004`, Chapter 7)
- `STR-BLT-002` -> `EVD-0010` (Source: `NAT-NDMA-001`, Section 6.4)
- `STR-GIS-001` -> `EVD-0011` (Source: `RES-TN-001`, Section 2.1)
- `STR-CRT-001` -> `EVD-0012` (Source: `TN-SDMP-004`, Section 8.2)
- `STR-EWS-001` -> `EVD-0013` (Source: `TN-SDMP-004`, Chapter 4)
- `STR-HTS-001` -> `EVD-0014` (Source: `IPCC-AR6-001`, Chapter 6.3.2)
- `STR-CST-001` -> `EVD-0015` (Source: `RES-TN-001`, Section 4.1)
- `STR-CST-002` -> `EVD-0016` (Source: `TN-SDMP-004`, Section 9.3)
