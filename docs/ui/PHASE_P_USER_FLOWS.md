# Phase P Master User Flow & Interaction Specification

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. Master User Flow Sequence

```
[1. Open Platform Landing / Dashboard]
                  │
                  ▼
[2. Search / Select District (e.g. TN-001 Chennai)]
                  │
                  ▼
[3. GIS Tamil Nadu Master Map Focuses District]
                  │
                  ▼
[4. Inspect Hazard Risk (Flood, Drought, Heatwave)]
                  │
                  ▼
[5. Inspect Exposure, Vulnerability & Resilience]
                  │
                  ▼
[6. Inspect Adaptation Priority & Priority Drivers]
                  │
                  ▼
[7. Inspect Strategy Candidates Matrix (14 Canonical)]
                  │
                  ▼
[8. Run / Inspect Classical MILP Portfolio Optimization]
                  │
                  ▼
[9. Inspect QAOA Quantum Experiment & Benchmark (Gap=0.4700)]
                  │
                  ▼
[10. Inspect RAG Evidence & Clickable Document Citations]
                  │
                  ▼
[11. Read Grounded Decision Explanation & LLM Disclaimer]
                  │
                  ▼
[12. Inspect Decision Provenance Graph & Export Audit Payload]
```

---

## 2. Detailed Navigation Routes & Tabs

- `/dashboard`: Overall Tamil Nadu 38-District GIS Overview, active workflow status, system health.
- `/risk-map`: Interactive spatial layer controls for Flood, Drought, Heatwave, Exposure, Resilience.
- `/district/:districtId`: District Profile deep-dive with tabs:
  - `Overview` | `Risk` | `Exposure` | `Vulnerability` | `Resilience` | `Priority` | `Strategies` | `Optimization` | `QAOA` | `Evidence` | `Explanation` | `Provenance`
- `/decision/:decisionId`: Shareable decision audit view with full provenance download.
- `/methodology`: Scientific methodology disclosure (Risk vs Priority vs Strategy vs Quantum Benchmark).
- `/sources`: Interactive evidence source index & document browser.
