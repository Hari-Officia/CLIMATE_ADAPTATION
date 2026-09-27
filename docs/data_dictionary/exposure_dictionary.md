# Data Dictionary — Phase F Exposure Engine

| Field Name | Data Type | Unit | Allowed Values | Null Semantics | Source | Description |
|---|---|---|---|---|---|---|
| `district_id` | String | None | Canonical ID (e.g., `chennai`) | NOT NULL | `districts.json` | Unique canonical district identifier |
| `total_population` | Integer | Persons | >= 0 | NULL if unverified | Census 2011 / WorldPop | Total resident population of district |
| `urban_population` | Integer | Persons | >= 0 | NULL if unverified | Census 2011 | Population residing in urban localities |
| `rural_population` | Integer | Persons | >= 0 | NULL if unverified | Census 2011 | Population residing in rural areas |
| `vulnerable_age_group` | Integer | Persons | >= 0 | NULL if unverified | Census 2011 | Estimated population under 5 and over 65 |
| `total_area_km2` | Float | km² | > 0 | NOT NULL | TNDMA | Geographic area of district |
| `built_up_area_km2` | Float | km² | >= 0 | NULL if unverified | TNDMA Land Cover | Built-up urban land area |
| `impervious_surface_fraction` | Float | Ratio | 0.0 – 1.0 | NULL if unverified | ISRO LULC | Fraction of impervious surface area |
| `urban_density_category` | String | Class | `HIGH`, `MEDIUM`, `LOW` | NULL if unknown | Derived | Urban settlement density level |
| `asset_count` | Integer | Count | >= 0 | 0 if no assets registered | OSM 2024 | Total registered critical infrastructure assets |
