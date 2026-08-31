# Climate Adaptation & Multi-Hazard Risk Intelligence System
## Technical Architecture & Scientific Parameter Reference Guide

---

### Executive Summary

This document provides an exhaustive technical and scientific reference for the **Climate Risk Intelligence & Decision Support System**. It covers the data acquisition agents, feature engineering pipeline, spatial GIS mapping engine, disaster risk thresholds, ML inference models, and central multi-hazard decision support architecture.

---

### 1. Climate Data Acquisition & Forecasting Agent

#### 📍 File Location:
`backend/agents/climate_data_agent.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\agents\climate_data_agent.py`)

#### ⚙️ Technical Implementation:
The `ClimateDataAgent` is an asynchronous data acquisition service that interfaces with external weather APIs, sensor streams, and historical climate archives.

* **7-Day Weather Forecast (`get_forecast`):**
  * **Source:** Open-Meteo NWP API (`https://api.open-meteo.com/v1/forecast`)
  * **Variables Fetched:** Hourly and daily temperature, humidity, dew point, surface pressure, wind speed, wind gusts, soil moisture (0–1cm), precipitation sum, and WMO weather condition codes.
* **180-Day Historical Archive & SPI Fetcher (`get_historical_spi`):**
  * **Source:** Open-Meteo Historical Archive API (`https://archive-api.open-meteo.com/v1/archive`)
  * **Mechanism:** Queries past **180 days** of actual recorded daily rainfall for any target coordinate to calculate exact **SPI-3** (90-day multi-month rainfall anomaly) and **SPI-6** (180-day multi-month rainfall anomaly) without guessing or dummy values.
* **Air Quality & Marine Sensors (`get_air_quality`, `get_marine_data`):**
  * **Air Quality:** Real-time US AQI, PM2.5, PM10, NO2, SO2, CO, and Ozone.
  * **Marine Data:** Wave height, wave period, and swell wave height for coastal districts.
* **Resilient Dual-Layer Caching:**
  * **Memory Cache:** Fast in-memory dictionary caching.
  * **Disk Cache:** Persistent JSON cache (`data/cached_forecasts/`) with a 1-hour Time-To-Live (TTL) ensuring sub-second response times and complete protection against API timeouts.

---

### 2. Feature Engineering Pipeline & Schema

#### 📍 File Locations:
* `backend/services/feature_engineering.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\services\feature_engineering.py`)
* `backend/risk/feature_contract.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\risk/feature_contract.py`)

#### ⚙️ Technical Implementation:
The `FeatureEngineeringService` transforms raw forecast arrays and historical climatology into the **exact 53 continuous features** required by the XGBoost Machine Learning models.

#### 📊 Complete 53-Feature Dictionary Breakdown:

| Index | Feature Name | Description & Derivation Formula | Unit |
| :--- | :--- | :--- | :--- |
| 1 | `temp_max` | Maximum 24-hour daily temperature | °C |
| 2 | `temp_min` | Minimum 24-hour daily temperature | °C |
| 3 | `temp_mean` | $(T_{\text{max}} + T_{\text{min}}) / 2$ | °C |
| 4 | `temp_range` | $T_{\text{max}} - T_{\text{min}}$ | °C |
| 5 | `humidity` | Mean 24-hour relative humidity | % |
| 6 | `wind_speed` | Maximum 10m wind speed | m/s |
| 7 | `rainfall` | Total 24-hour precipitation accumulation | mm |
| 8 | `soil_wetness` | Soil moisture fraction (0–1cm depth) | 0.0 - 1.0 |
| 9 | `rainfall_3d` | 3-day rolling precipitation accumulation | mm |
| 10 | `rainfall_7d` | 7-day total forecast precipitation sum | mm |
| 11 | `rainfall_30d` | Cumulative 30-day precipitation window | mm |
| 12 | `temp_anomaly` | $T_{\text{max}} - T_{\text{climatology\_baseline\_mean}}$ | °C |
| 13 | `rainfall_anomaly` | $\text{Rainfall}_{\text{daily}} - \text{Rainfall}_{\text{climatology\_baseline\_mean}}$ | mm |
| 14 | `SPI_3` | Standardized 90-day precipitation index: $(\text{Rain}_{90d} - \mu_{90d}) / \sigma_{90d}$ | Index |
| 15 | `SPI_6` | Standardized 180-day precipitation index: $(\text{Rain}_{180d} - \mu_{180d}) / \sigma_{180d}$ | Index |
| 16-53 | `district_Ariyalur` to `district_Virudhunagar` | One-Hot categorical boolean encoding for all **38 Tamil Nadu districts** in exact alphabetical order. | 0 or 1 |

---

### 3. Interactive GIS Map & Spatial Analysis Engine

#### 📍 File Locations:
* **Frontend Map Page:** `frontend/src/pages/RiskMap.jsx` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\frontend\src\pages\RiskMap.jsx`)
* **Backend GIS API:** `backend/api/gis.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\api\gis.py`)
* **Point-in-Polygon Engine:** `backend/services/geocoding_service.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\services\geocoding_service.py`)

#### ⚙️ Technical Implementation:
* **Watermark-Free Basemap:** Integrates **Esri Dark Gray Canvas** tiles (`https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}`), eliminating third-party API key watermarks while providing a sleek dark theme.
* **Dynamic 38-District Choropleth Overlay (`/gis/risk-overlay`):** Reads [`data/geojson/tamil_nadu_districts.geojson`](file:///c:/Users/haris/OneDrive/Desktop/PROJECT_DATA/data/geojson/tamil_nadu_districts.geojson) and dynamically color-codes all 38 districts based on selected hazard probabilities:
  * 🔴 **High / Severe Risk ($\ge 70\%$):** Rose fill (`#f43f5e`)
  * 🟡 **Medium Risk ($40\% - 69\%$):** Amber fill (`#f59e0b`)
  * 🟢 **Low Risk ($< 40\%$):** Emerald fill (`#10b981`)
* **Ray-Casting Spatial Pin Inspection:** Clicking anywhere on the interactive map triggers Point-in-Polygon spatial lookup via `GeocodingService` to resolve the containing administrative district, fetch localized point weather, and open the Spatial Risk Assessment drawer.

---

### 4. Registered Climate Hazards & Disaster Parameters

#### 📍 File Locations:
* `backend/hazards/registry.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\hazards\registry.py`)
* `backend/hazards/` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\hazards/`)

#### ⚙️ Detailed Module Breakdown:

| Hazard Module | Type | Parameters & Threshold Criteria | Output Unit |
| :--- | :--- | :--- | :--- |
| **Flood Risk** | `Type A (ML)` | 500-tree XGBoost model assessing 53 features (rainfall_3d, rainfall_7d, soil_wetness). | % Probability |
| **Drought Risk** | `Type A (ML)` | 500-tree XGBoost model assessing 180-day real historical SPI-3, SPI-6 & soil moisture deficits. | % Probability |
| **Heatwave Risk** | `Type A (ML)` | 500-tree XGBoost model assessing daytime temp max departures from historical baselines. | % Probability |
| **Extreme Rainfall** | `Type B (Rule)` | IMD Thresholds: $>64.5\text{ mm}$ (Heavy), $>115.5\text{ mm}$ (Very Heavy), $>204.4\text{ mm}$ (Extremely Heavy). | mm / 24h |
| **Extreme Wind** | `Type B (Rule)` | WMO Beaufort Scale: $\ge 17.2\text{ m/s}$ (Gale), $\ge 24.5\text{ m/s}$ (Storm), $\ge 32.7\text{ m/s}$ (Hurricane). | m/s |
| **Heat Stress** | `Type B (Rule)` | Steadman Heat Index combining air temperature and relative humidity ($>41^\circ\text{C}$ Danger). | °C Heat Index |
| **Thunderstorm** | `Type B (Rule)` | Convective stability indices, dew point threshold ($>20^\circ\text{C}$), & rain intensity. | Severity Level |
| **Coastal Wave/Swell** | `Type C (API/Rule)`| Open-Meteo Marine API evaluating wave heights ($>2.5\text{ m}$ High Sea) for coastal zone districts. | Meters (m) |
| **Air Quality (AQI)** | `Type C (API/Rule)`| US EPA AQI scale: $>100$ Unhealthy for Sensitive Groups, $>150$ Unhealthy. | AQI Index |
| **Cyclone Tracker** | `Type B (Rule)` | Atmospheric pressure drops ($<1000\text{ hPa}$) & sustained wind velocity. | Category |

---

### 5. Risk Agent & Central Multi-Hazard Engine

#### 📍 File Locations:
* **ML Risk Agent:** `backend/agents/risk_agent.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\agents\risk_agent.py`)
* **Multi-Hazard Decision Engine:** `backend/hazards/risk_engine.py` (`c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\hazards\risk_engine.py`)

#### ⚙️ Technical Implementation:
* **XGBoost Inference Engine:** Loads pre-trained XGBoost classifiers (`Models/flood_xgboost.pkl`, `Models/drought_xgboost.pkl`, `Models/heatwave_xgboost.pkl`).
* **Complete Failure Isolation:** In `RiskEngine.calculate_all()`, each hazard module executes inside an isolated `try-except` block. If any single model or sensor feed encounters missing data or an exception, it returns `UNAVAILABLE` without breaking remaining hazard evaluations.
* **Calibrated Threat Classification:**
  * **HIGH:** Probability $\ge 0.70$
  * **MEDIUM:** Probability $0.40 - 0.69$
  * **LOW:** Probability $< 0.40$
* **7-Day Risk Trajectory:** Calculates continuous daily multi-hazard probabilities across all 7 forecast days to render real-time risk charts.

---

### 📁 Summary of All Project Files & Locations

| Component | Absolute File Path |
| :--- | :--- |
| **Git Configuration** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\.gitignore` |
| **Climate Agent** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\agents\climate_data_agent.py` |
| **Feature Engineering** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\services\feature_engineering.py` |
| **Feature Contracts** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\risk\feature_contract.py` |
| **Risk Agent** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\agents\risk_agent.py` |
| **Risk Engine** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\hazards\risk_engine.py` |
| **Drought Module** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\hazards\drought.py` |
| **GIS API** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\api\gis.py` |
| **Geocoding Service** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\backend\services\geocoding_service.py` |
| **Risk Map UI** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\frontend\src\pages\RiskMap.jsx` |
| **Dashboard UI** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\frontend\src\pages\Dashboard.jsx` |
| **Test Suite Runner** | `c:\Users\haris\OneDrive\Desktop\PROJECT_DATA\scripts\run_all_tests.py` |
