# Adaptation Dataset Data Dictionary

**Version**: `v1.0.0_verified`  
**Geographic Scope**: Tamil Nadu, India (38 Districts)  
**System Role**: Authoritative Climate Adaptation Strategy Data Model  

---

## 1. Overview & Data Architecture

This Data Dictionary defines the schemas, data types, value constraints, and relational integrity rules for the canonical Climate Adaptation Strategy Knowledge Base. The dataset serves as the immutable upstream truth consumed by downstream modules including the **Adaptation Applicability Engine**, **Rule Engine**, **RAG Pipeline**, **Classical Optimization (MILP)**, **QUBO/QAOA Quantum Solvers**, **LLM Explanation Engine**, and **GIS Map Visualization**.

---

## 2. Table Schemas & Field Definitions

### 2.1 Canonical Strategies Table (`adaptation_strategies.csv` / `strategies`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `strategy_id` | VARCHAR(32) | Primary Key (`STR-XXX-###`) | Unique canonical identifier for each adaptation strategy. |
| `strategy_name` | VARCHAR(256) | UNIQUE, NOT NULL | Standard public title of the strategy. |
| `strategy_domain` | VARCHAR(128) | FK to `strategy_categories` | One of 10 canonical adaptation domains. |
| `strategy_type` | VARCHAR(64) | NOT NULL | Action mechanism (e.g., `ENGINEERING`, `NATURE_BASED`, `STRUCTURAL`, `POLICY_POLICY`, `PLANNING`, `TECHNOLOGY`, `BUILDING_NBS`). |
| `description` | TEXT | NOT NULL | Detailed narrative description of physical or policy mechanism. |
| `primary_hazards` | TEXT | NOT NULL (Semicolon-delimited) | Primary hazards addressed strictly from Hazard Taxonomy. |
| `secondary_hazards` | TEXT | Semicolon-delimited | Secondary co-mitigated hazards. |
| `adaptation_objective` | TEXT | NOT NULL | Explicit adaptation goal (e.g., attenuation, exposure reduction, recharge). |
| `target_exposure` | TEXT | NOT NULL | Target physical or socio-economic assets exposed to hazard. |
| `target_vulnerability` | TEXT | NOT NULL | Target system vulnerability or sensitivity dimension. |
| `target_resilience_dimension` | VARCHAR(128) | NOT NULL | System dimension improved (`Physical Infrastructure`, `Water Resource Supply`, `Ecosystem & Natural Capital`, `Policy & Governance`, `Social & Human Capital`, `Human Health & Thermal Comfort`). |
| `urban_rural` | VARCHAR(16) | `URBAN`, `RURAL`, `BOTH` | Urban vs rural operational applicability setting. |
| `coastal_inland` | VARCHAR(16) | `COASTAL`, `INLAND`, `BOTH` | Hydro-geomorphic landscape zone. |
| `geographic_scope` | VARCHAR(64) | NOT NULL | Spatial applicability scale category (`ALL_TAMIL_NADU`, `COASTAL_DISTRICTS`, `URBAN_DISTRICTS`, `RURAL_DISTRICTS`). |
| `required_conditions` | TEXT | NOT NULL | High-level textual condition overview. |
| `applicability_rules` | TEXT | NOT NULL | Machine-readable boolean expression evaluated by rule engine. |
| `implementation_scale` | VARCHAR(64) | NOT NULL | Granularity of deployment (`Municipal`, `Building / Household`, `District / Watershed`, `State / District`, `Municipal / Neighborhood`, `Facility`, `District`, `District / City`, `Household / Neighborhood`, `Coastal Zone`). |
| `implementation_horizon` | VARCHAR(32) | `SHORT_TERM`, `MEDIUM_TERM`, `LONG_TERM` | Expected execution timeline. |
| `implementation_complexity` | VARCHAR(16) | `LOW`, `MEDIUM`, `HIGH` | Operational & technical execution complexity. |
| `land_requirement` | VARCHAR(16) | `NONE`, `LOW`, `MEDIUM`, `HIGH` | Physical footprint land requirement. |
| `water_requirement` | VARCHAR(16) | `NONE`, `LOW`, `MEDIUM`, `HIGH` | Operational water consumption requirement. |
| `energy_requirement` | VARCHAR(16) | `NONE`, `LOW`, `MEDIUM`, `HIGH` | Power & fuel requirement during operation. |
| `maintenance_requirement` | VARCHAR(16) | `LOW`, `MEDIUM`, `HIGH` | Post-implementation maintenance requirement. |
| `technical_requirements` | TEXT | NOT NULL | Required engineering tools, machinery, or technical skills. |
| `institutional_requirements` | TEXT | NOT NULL | Nodal government department or municipal agency responsible. |
| `cost_level` | VARCHAR(16) | `LOW`, `MEDIUM`, `HIGH` | Qualitative budget intensity scale. |
| `cost_basis` | VARCHAR(64) | `QUALITATIVE_ONLY`, `NOT_AVAILABLE` | Evidence basis for cost figure. Strictly enforced non-invented metric rule. |
| `effectiveness` | VARCHAR(64) | `QUALITATIVE_ONLY`, `NOT_AVAILABLE` | Evidence basis for risk reduction. Strictly enforced non-invented metric rule. |
| `effectiveness_basis` | TEXT | NOT NULL | Source citation basis for qualitative effectiveness claims. |
| `co_benefits` | TEXT | Semicolon-delimited | Secondary positive social, environmental, or economic outcomes. |
| `tradeoffs` | TEXT | Semicolon-delimited | Operational compromises or negative friction points. |
| `negative_impacts` | TEXT | Semicolon-delimited | Potential adverse environmental or social externalities. |
| `dependencies` | TEXT | Semicolon-delimited | Mandatory prerequisite strategy IDs (`STR-XXX-###`). |
| `conflicts` | TEXT | Semicolon-delimited | Incompatible strategy IDs (`STR-XXX-###`). |
| `complementary_strategies` | TEXT | Semicolon-delimited | Synergistic strategy IDs (`STR-XXX-###`). |
| `failure_conditions` | TEXT | NOT NULL | Environmental or operational thresholds causing strategy failure. |
| `implementation_constraints` | TEXT | NOT NULL | Institutional, spatial, or legal bottlenecks. |
| `monitoring_indicators` | TEXT | Semicolon-delimited | Measurable empirical indicators for monitoring progress. |
| `success_metrics` | TEXT | NOT NULL | Target qualitative outcome evaluation criterion. |
| `optimization_eligible` | BOOLEAN | `TRUE`, `FALSE` | Flag indicating eligibility for QUBO / MILP decision modeling. |
| `evidence_strength` | VARCHAR(16) | `VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW` | Scientific and policy evidence confidence grade. |

---

### 2.2 Strategy Hazard Mapping (`strategy_hazards.csv` / `strategy_hazards`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `strategy_id` | VARCHAR(32) | FK to `strategies` | Strategy identifier. |
| `hazard_id` | VARCHAR(32) | Check Hazard Taxonomy | Enum: `FLOOD`, `DROUGHT`, `HEATWAVE`, `COASTAL_FLOOD`, `COASTAL_EROSION`, `WATER_SCARCITY`, `URBAN_HEAT`. |
| `hazard_relationship_type` | VARCHAR(16) | `PRIMARY`, `SECONDARY` | Primary target vs secondary co-benefit hazard. |

---

### 2.3 Machine-Readable Conditions (`strategy_conditions.csv` / `strategy_conditions`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `condition_id` | VARCHAR(32) | Primary Key (`CND-###`) | Condition record identifier. |
| `strategy_id` | VARCHAR(32) | FK to `strategies` | Strategy identifier. |
| `hazard_context` | VARCHAR(32) | Hazard Enum | Applicable hazard context for condition. |
| `condition_expression` | TEXT | Boolean Logic Expression | Parsable expression (e.g., `urban_flood_risk >= MEDIUM AND impervious_surface >= 0.70`). |
| `parameters_required` | TEXT | Semicolon-delimited | List of district GIS/feature parameters evaluated in rule engine. |
| `evaluation_operator` | VARCHAR(16) | `AND`, `OR`, `NOT` | Logical operator combining parameters. |

---

### 2.4 District Applicability Table (`strategy_district.csv` / `strategy_district`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `strategy_id` | VARCHAR(32) | FK to `strategies` | Strategy identifier. |
| `district_name` | VARCHAR(64) | TN District Name / Special Category | Specific Tamil Nadu district or `ALL_TAMIL_NADU`. |
| `applicability_category` | VARCHAR(32) | District Enum | Enum: `ALL_TAMIL_NADU`, `COASTAL_DISTRICTS`, `URBAN_DISTRICTS`, `RURAL_DISTRICTS`, `DISTRICT_SPECIFIC`, `NOT_ENOUGH_EVIDENCE`. |
| `eligibility_status` | VARCHAR(32) | `ELIGIBLE`, `CONDITIONALLY_ELIGIBLE`, `INELIGIBLE` | Decision eligibility status for optimization solver. |
| `evidence_rationale` | TEXT | NOT NULL | Official state framework or empirical evidence supporting assignment. |

---

### 2.5 Strategy Interactions (`strategy_interactions.csv` / `strategy_interactions`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `strategy_a` | VARCHAR(32) | FK to `strategies` | Source strategy ID. |
| `strategy_b` | VARCHAR(32) | FK to `strategies` | Target strategy ID. |
| `relationship` | VARCHAR(32) | `COMPLEMENTARY`, `CONFLICTING`, `DEPENDENT`, `NEUTRAL` | Pair-wise interaction relationship. |
| `reason` | TEXT | NOT NULL | Mechanistic rationale for relationship. |
| `evidence_id` | VARCHAR(32) | FK to `evidence_claims` | Traceable evidence ID. |

---

### 2.6 Optimization Attributes (`strategy_optimization.csv` / `strategy_optimization_attributes`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `strategy_id` | VARCHAR(32) | FK to `strategies` | Strategy identifier. |
| `benefit_vector` | TEXT | Key-value string (`key:val;...`) | Vector of normalized relative benefit weights across objective dimensions. |
| `resource_vector` | TEXT | Key-value string (`key:val;...`) | Qualitative resource consumption intensity vector. |
| `constraint_vector` | TEXT | Key-value string (`key:val;...`) | Upper bound constraint requirements. |
| `compatibility_group` | VARCHAR(64) | Group Code | Co-selection synergy group. |
| `conflict_group` | VARCHAR(64) | Group Code | Mutually exclusive exclusion group ($x_i + x_j \le 1$). |
| `dependency_group` | VARCHAR(64) | Group Code | Prerequisite selection constraint group ($x_A \le x_B$). |
| `optimization_eligible` | BOOLEAN | `TRUE`, `FALSE` | Flag for QUBO binary decision variable generator. |

---

### 2.7 Evidence Claims Table (`evidence_claims.csv` / `evidence_claims`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `claim_id` | VARCHAR(32) | Primary Key (`EVD-###`) | Unique evidence claim identifier. |
| `strategy_id` | VARCHAR(32) | FK to `strategies` | Strategy identifier. |
| `claim_text` | TEXT | NOT NULL | Verbatim or synthesized authoritative claim. |
| `claim_type` | VARCHAR(32) | Claim Type Enum | `APPLICABILITY`, `EFFECTIVENESS`, `IMPLEMENTATION`, `CONSTRAINT`, `TRADEOFF`, `CO_BENEFIT`, `TECHNICAL_REQUIREMENT`. |
| `source_id` | VARCHAR(32) | FK to `sources` | Authoritative source ID. |
| `source_title` | VARCHAR(512) | NOT NULL | Title of source document. |
| `organization` | VARCHAR(256) | NOT NULL | Publishing organization. |
| `year` | INT | Year | Publication year. |
| `url` | TEXT | Valid HTTP URL | Source web location. |
| `page_or_section` | VARCHAR(128) | NOT NULL | Precise section or page reference in document. |
| `evidence_strength` | VARCHAR(16) | `VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW` | Assigned confidence grade. |

---

### 2.8 Source Registry Table (`sources.csv` / `sources`)

| Field Name | Data Type | Constraint / Enum | Description |
| :--- | :--- | :--- | :--- |
| `source_id` | VARCHAR(32) | Primary Key (`TN-...` / `NAT-...` / `IPCC-...` / `RES-...`) | Authoritative source identifier. |
| `title` | VARCHAR(512) | NOT NULL | Full document title. |
| `organization` | VARCHAR(256) | NOT NULL | Publishing institution. |
| `publication_year` | INT | Year | Year published. |
| `source_tier` | VARCHAR(16) | `Tier 1`, `Tier 2`, `Tier 3`, `Tier 4` | Provenance tier grade per Source Hierarchy. |
| `source_type` | VARCHAR(64) | NOT NULL | Document category (e.g., `Government Framework`, `Disaster Plan`, `Assessment Report`). |
| `hazards` | TEXT | Semicolon-delimited | Hazards covered by source. |
| `adaptation_domains` | TEXT | Semicolon-delimited | Adaptation domains covered by source. |
| `geographic_scope` | VARCHAR(64) | NOT NULL | Geographic coverage area. |
| `url` | TEXT | Valid URL | Source access web link. |
| `evidence_strength` | VARCHAR(16) | `VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW` | Overall source reliability grade. |
| `status` | VARCHAR(16) | `CURRENT`, `SUPERSEDED` | Document status. |
