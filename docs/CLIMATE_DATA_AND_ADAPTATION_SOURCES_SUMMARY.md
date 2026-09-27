# Comprehensive Summary of Climate Data Inventory & Adaptation Sources Registry

**Project**: Climate Risk Intelligence & Decision Support System  
**Knowledge Base Version**: `v1.0.0_verified`  
**Geographic Target**: State of Tamil Nadu, India (38 Administrative Districts)  
**Document Generation Date**: 2026-09-26  

---

## Executive Summary

This document compiles the exhaustive data inventory, machine learning feature schemas, GIS spatial topologies, quantum/classical optimization benchmarks, and authoritative adaptation sources registered in the system. 

It is divided into two core parts:
1. **Part I**: Complete Summary of All Data Used Across the Application, Knowledge Base, and Optimization Pipelines.
2. **Part II**: Adaptation Sources Registry with Official Web Links, Direct Download URLs, Authority Tiers, and Strategy Mappings.

---

# Part I: Complete Data Inventory & Pipeline Reference

### 1. Authoritative Knowledge Base Snapshot (`v1.0.0_verified`)

The Knowledge Base is stored under [`knowledge_base/v1.0.0_verified/`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified) and governed by [`KNOWLEDGE_BASE_VERSION.md`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/KNOWLEDGE_BASE_VERSION.md).

#### 📊 Snapshot Metadata & Scope
* **Version**: `v1.0.0_verified` (Released 2026-09-22)
* **Geographic Target**: State of Tamil Nadu, India (38 Administrative Districts: 14 Coastal / 24 Inland)
* **Scope**: Climate Adaptation & Risk Reduction ONLY
* **Version Policy**: Immutable snapshot with a strict `NULL` policy for missing numeric metrics (no silent zero imputation).

#### 🛡️ Source Authority Tier Hierarchy
All knowledge items are categorized and weighted using a 6-Tier Authority Matrix ([source_hierarchy.md](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/source_hierarchy.md)):
1. **Tier 1 (Weight: 1.00)** – Official Tamil Nadu State Govt Policies (e.g., TN District Climate Adaptation Framework 2024, DCAPT Guidelines 2025, Chennai CAP 2050, TNSDMA SDMP 2023-2030).
2. **Tier 2 (Weight: 0.90)** – Indian National Government Guidelines (e.g., NDMA Urban Flooding Guidelines 2022, CGWB Master Plan for Artificial Recharge 2021).
3. **Tier 3 (Weight: 0.85)** – Intergovernmental Bodies (e.g., IPCC AR6 Working Group II Chapter 6).
4. **Tier 4 (Weight: 0.80)** – Peer-Reviewed Scientific Research (e.g., IIT Madras & Anna University Hydrodynamic Flood Mitigation studies 2024).
5. **Tier 5 (Weight: 0.75)** – Technical & Engineering Standards (BIS, IRC, CPHED manuals).
6. **Tier 6 (Weight: 0.60)** – Secondary Technical Reports & Case Studies.

#### 📁 Knowledge Base Components
* **8 Registered Verified Sources**: Cataloged in [sources.csv](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.csv).
* **12 Normalized Master Strategies**: Covering 10 adaptation domains (Water Management, Built Infrastructure, Green Infrastructure, Drainage, GIS Planning, Early Warning, Heat Resilience, Coastal Resilience, Land Use, Urbanization).
* **3 Explicitly Typed Evidence Claims**: Stored in [`04_EVIDENCE/evidence_claims.csv`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/04_EVIDENCE/evidence_claims.csv).
* **38 District Strategic Mappings**: Detailed applicability matrix in [`05_DISTRICTS/district_strategy_applicability.csv`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/05_DISTRICTS/district_strategy_applicability.csv).
* **31 RAG Semantic Text Chunks**: Indexed with metadata in [`06_RAG/chunks.jsonl`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/06_RAG/chunks.jsonl) and populated into ChromaDB (`knowledge_base/chroma/`).

---

### 2. Live Climate Data & Ingestion Sources

Details registered in [`docs/HAZARD_DATA_SOURCES.md`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/docs/HAZARD_DATA_SOURCES.md):

| Data Source | Provider / Mechanism | Parameters & Variables Retrieved | Frequency / Format |
| :--- | :--- | :--- | :--- |
| **Numerical Weather Prediction (NWP)** | Open-Meteo Weather API (`REST HTTP`) | Hourly/Daily Temperature (2m, $T_{\max}$, $T_{\min}$, dew point), Humidity, Precipitation (hourly sum, daily sum, probability), Wind (10m speed, gusts, direction), Surface Pressure, Soil Moisture (0-1cm), WMO Weather Codes | 7-day forecast (Hourly updates) |
| **Air Quality Monitoring** | Open-Meteo Air Quality API | $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$, $\text{O}_3$, European AQI, US EPA AQI | Hourly updates |
| **Marine & Sea State** | Open-Meteo Marine API | Significant Wave Height, Wave Direction, Wave Period, Swell Wave Height/Period | Hourly updates (Coastal districts) |
| **Historical SPI & Archive** | Open-Meteo Archive API (Past 180 Days) | 180-day continuous daily rainfall archive used to calculate exact **SPI-3** (90-day) and **SPI-6** (180-day) drought indices without dummy fallbacks | Real-time 180-day historical window |
| **District Climatology Baselines** | NASA POWER Agroclimatology (2010–2026) | 16-year daily baseline means, standard deviations, and percentiles for $T_{\max}$, $T_{\min}$, Rainfall, Humidity, Wind, Root-zone soil wetness | Static 16-year baseline |
| **Historical District Datasets** | Local CSV Archives in [`ClimateData/`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/ClimateData) | 38 individual CSV files (e.g., `Chennai.csv`, `Madurai.csv`, `Coimbatore.csv`), containing daily historical records per district | Static CSVs |

---

### 3. Spatial, GIS & Geographical Topology Data

* **Administrative District Profiles**: [`data/district_profiles/tamil_nadu_profiles.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/data/district_profiles/tamil_nadu_profiles.json)
  * Contains Census of India & DES Tamil Nadu demographic stats: population, density, urbanization %, coastal zone indicator flag, mean elevation.
* **District Boundaries (GeoJSON)**: [`data/geojson/tamil_nadu_districts.geojson`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/data/geojson/tamil_nadu_districts.geojson)
  * Precise WGS84 CRS84 polygons for all 38 Tamil Nadu districts used for interactive map rendering (Leaflet/Esri Dark Gray Canvas) and Point-in-Polygon spatial Ray-Casting lookup.
* **Secondary Boundary Set**: Directory [`geoBoundaries-IND-ADM2-all/`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/geoBoundaries-IND-ADM2-all) containing official administrative ADM2 polygons.

---

### 4. Machine Learning Models & Feature Engineering Data

* **53-Feature Machine Learning Vector**: Engineered in [`backend/services/feature_engineering.py`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/backend/services/feature_engineering.py):
  1. Temperature metrics (`temp_max`, `temp_min`, `temp_mean`, `temp_range`, `temp_anomaly`)
  2. Moisture & Rainfall (`humidity`, `wind_speed`, `rainfall`, `soil_wetness`, `rainfall_3d`, `rainfall_7d`, `rainfall_30d`, `rainfall_anomaly`)
  3. Standardized Precipitation Index (`SPI_3`, `SPI_6`)
  4. 38 District One-Hot Encodings (`district_Ariyalur` to `district_Virudhunagar`)
* **Trained ML Models**: Stored in [`Models/`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/Models)
  * `flood_xgboost.pkl`: 500-tree XGBoost model for flood probability estimation.
  * `drought_xgboost.pkl`: 500-tree XGBoost model for drought risk assessment.
  * `heatwave_xgboost.pkl`: 500-tree XGBoost model for heatwave occurrence prediction.

---

### 5. Quantum & Optimization Benchmark Datasets

Located at the root of the workspace for validating portfolio optimization algorithms (MILP, QUBO, QAOA):
* [`38_DISTRICT_QUANTUM_RESEARCH_GATE_V2.csv`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/38_DISTRICT_QUANTUM_RESEARCH_GATE_V2.csv)
* [`38_DISTRICT_FRONTEND_VERIFICATION.csv`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/38_DISTRICT_FRONTEND_VERIFICATION.csv)
* [`EXACT_MILP_QUBO_EQUIVALENCE.csv`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/EXACT_MILP_QUBO_EQUIVALENCE.csv)
* [`V2_OBJECTIVE_RECONCILIATION.csv`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/V2_OBJECTIVE_RECONCILIATION.csv)
* **Scale Benchmarks**: `scale_vs_runtime.csv`, `scale_vs_feasibility.csv`, `scale_vs_gap.csv`, `scale_vs_optimal_probability.csv`.

---

# Part II: Adaptation Sources Registry & Implementation Mapping

All source metadata is registered in [`knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.csv`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.csv).

### 🌐 1. Complete Registered Adaptation Sources & Official Links

#### **Tier 1: Official Tamil Nadu Government Frameworks & Policies** (Precedence Weight: 1.00)

1. **Tamil Nadu District Climate Change Risk Reduction & Adaptation Framework (2024)**
   * **Source ID**: `TN-ADAPT-001`
   * **Organization**: Dept. of Environment and Climate Change, Govt of Tamil Nadu
   * **Official Portal**: [tn.gov.in/environment/tnccdap](https://www.tn.gov.in/environment/tnccdap)
   * **Direct PDF Download**: [tnccdap_2024.pdf](https://www.tn.gov.in/environment/docs/tnccdap_2024.pdf)
   * **Scope & Sector**: All 38 Tamil Nadu Districts | Cross-Sectoral Adaptation
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L3-L27)

2. **District Climate Action Prioritisation Tool (DCAPT) User Guide (2025)**
   * **Source ID**: `TN-DCAPT-002`
   * **Organization**: Tamil Nadu Climate Change Mission (TNCCM)
   * **Official Portal**: [tnclimate.tn.gov.in/dcapt](https://tnclimate.tn.gov.in/dcapt)
   * **Direct PDF Download**: [dcapt_guide_2025.pdf](https://tnclimate.tn.gov.in/docs/dcapt_guide_2025.pdf)
   * **Scope & Sector**: All 38 Districts | Planning, Water Resources & Governance
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L29-L53)

3. **Chennai Climate Action Plan (CCAP) 2050 (2023)**
   * **Source ID**: `TN-CAP-003`
   * **Organization**: Greater Chennai Corporation & C40 Cities
   * **Official Portal**: [chennaicorporation.gov.in/ccap](https://chennaicorporation.gov.in/ccap)
   * **Direct PDF Download**: [chennai_cap_2050.pdf](https://chennaicorporation.gov.in/docs/chennai_cap_2050.pdf)
   * **Scope & Sector**: Chennai, Chengalpattu, Tiruvallur | Urban Infrastructure & Heat Resilience
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L55-L79)

4. **Tamil Nadu State Disaster Management Plan 2023–2030 (2023)**
   * **Source ID**: `TN-SDMP-004`
   * **Organization**: Tamil Nadu State Disaster Management Authority (TNSDMA)
   * **Official Portal**: [tnsdma.tn.gov.in/sdmp](https://tnsdma.tn.gov.in/sdmp)
   * **Direct PDF Download**: [tn_sdmp_2023_2030.pdf](https://tnsdma.tn.gov.in/docs/tn_sdmp_2023_2030.pdf)
   * **Scope & Sector**: State-wide | Disaster Management, Critical Infrastructure & Coastal Defense
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L81-L105)

---

#### **Tier 2: Indian National Technical Guidelines** (Precedence Weight: 0.90)

5. **NDMA National Guidelines for Management of Urban Flooding (2022)**
   * **Source ID**: `NAT-NDMA-001`
   * **Organization**: National Disaster Management Authority (NDMA), Govt of India
   * **Official Portal**: [ndma.gov.in/guidelines/urban-flooding](https://ndma.gov.in/guidelines/urban-flooding)
   * **Direct PDF Download**: [ndma_urban_flooding_2022.pdf](https://ndma.gov.in/docs/ndma_urban_flooding_2022.pdf)
   * **Scope & Sector**: National Urban Districts | Drainage, GIS Planning & Stormwater Standards
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L107-L131)

6. **Master Plan for Artificial Recharge to Groundwater in India (2021)**
   * **Source ID**: `NAT-CGWB-002`
   * **Organization**: Central Ground Water Board (CGWB), Ministry of Jal Shakti
   * **Official Portal**: [cgwb.gov.in/master_plan_recharge](https://cgwb.gov.in/master_plan_recharge.html)
   * **Direct PDF Download**: [master_plan_artificial_recharge_2021.pdf](https://cgwb.gov.in/docs/master_plan_artificial_recharge_2021.pdf)
   * **Scope & Sector**: Over-exploited & Hard-rock blocks in TN | Hydrogeology & Aquifer Recharge
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L133-L157)

---

#### **Tier 3 & Tier 4: International & Scientific Peer-Reviewed Literature** (Precedence Weight: 0.80 – 0.85)

7. **IPCC AR6 Working Group II Chapter 6: Cities, Settlements & Infrastructure (2022)**
   * **Source ID**: `IPCC-AR6-001`
   * **Organization**: Intergovernmental Panel on Climate Change (IPCC)
   * **DOI Link**: [10.1017/9781009325844.008](https://doi.org/10.1017/9781009325844.008)
   * **Official Chapter Link**: [ipcc.ch/report/ar6/wg2/chapter/chapter-6/](https://www.ipcc.ch/report/ar6/wg2/chapter/chapter-6/)
   * **Direct PDF Download**: [IPCC_AR6_WGII_Chapter06.pdf](https://www.ipcc.ch/report/ar6/wg2/downloads/IPCC_AR6_WGII_Chapter06.pdf)
   * **Scope & Sector**: Global Urban & Coastal | Nature-Based Solutions & Green Infrastructure
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L159-L183)

8. **Evaluating Blue-Green Infrastructure for Flood Mitigation in Coastal Cities of Tamil Nadu (2024)**
   * **Source ID**: `RES-TN-001`
   * **Organization**: IIT Madras & Anna University
   * **DOI Link / Publication**: [doi.org/10.1016/j.jenvman.2024.119850](https://doi.org/10.1016/j.jenvman.2024.119850)
   * **Direct Paper Download**: [tn_bgi_flood_2024.pdf](https://research.iitm.ac.in/papers/tn_bgi_flood_2024.pdf)
   * **Scope & Sector**: Coastal TN (Chennai, Cuddalore, Nagapattinam) | Hydrodynamic Modeling & Bioswales
   * **Local File Reference**: [`sources.json`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/01_SOURCE_REGISTRY/sources.json#L185-L209)

---

### 🛠️ 2. Implemented Adaptation Strategies & Source Mapping

All 12 normalized adaptation strategies implemented in the backend decision engine map directly to these verified sources ([strategies.csv](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/knowledge_base/v1.0.0_verified/03_STRATEGIES/strategies.csv)):

| Strategy ID | Implemented Adaptation Strategy Name | Primary Source ID | Sector / Type |
| :--- | :--- | :--- | :--- |
| `STR-DRN-001` | Urban Primary Drain Desilting & Channel Widening | `TN-ADAPT-001` | Drainage & Stormwater |
| `STR-DRN-002` | Underground Stormwater Detention Basins | `TN-ADAPT-001` | Subsurface Flood Retention |
| `STR-WTR-001` | Mandatory Rooftop Rainwater Harvesting & Injection Shafts | `TN-ADAPT-001` / `NAT-CGWB-002` | Groundwater Recharge |
| `STR-WTR-002` | Traditional Temple Tank & Cascade Lake De-silting | `TN-ADAPT-001` | Water Management & Lake Restoration |
| `STR-LND-001` | Floodplain Zoning & Drainage Corridor Buffer Enforcements | `TN-ADAPT-001` / `TN-CAP-003` | Land Use Policy |
| `STR-NBS-001` | Urban Bioswales & Permeable Pavement Network | `TN-ADAPT-001` / `RES-TN-001` | Nature-Based Solutions |
| `STR-BLT-001` | Plinth Elevation & Raised Electrical Infrastructure | `TN-ADAPT-001` / `TN-SDMP-004` | Utility Engineering |
| `STR-GIS-001` | DEM-Guided Low-Elevation Contour Runoff Retention Ponds | `TN-ADAPT-001` / `NAT-NDMA-001` | GIS Terrain Planning |
| `STR-CRT-001` | Hospital & Emergency Shelter Flood Barrier Retrofits | `TN-ADAPT-001` / `TN-SDMP-004` | Critical Infrastructure Defense |
| `STR-EWS-001` | IoT Hydro-Meteorological Automated Gauge Early Warning System | `TN-ADAPT-001` / `TN-DCAPT-002` | Telemetry & Early Warning |
| `STR-HTS-001` | High-Albedo Cool Roof Coating & Urban Tree Canopy Expansion | `TN-ADAPT-001` / `TN-CAP-003` | Heat Resilience |
| `STR-CST-001` | Mangrove Restoration & Coastal Bio-Shield Buffers | `TN-ADAPT-001` / `IPCC-AR6-001` | Coastal Marine Resilience |
