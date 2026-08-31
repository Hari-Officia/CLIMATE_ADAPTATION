# Climate Hazard Data Sources & Provenance

## 1. Primary Ingestion Sources

| Data Source | Provider | Ingestion Protocol | Parameters Retrieved | Update Frequency |
|---|---|---|---|---|
| **Numerical Weather Prediction (NWP)** | Open-Meteo Weather API | REST HTTP / JSON | Temperature (2m, max, min, apparent, dew point), Precipitation (hourly sum, daily sum, probability), Wind (10m speed, gusts, direction), Surface Pressure, Soil Moisture, Weather Codes | Hourly / 7-day forecast |
| **Air Quality Monitoring** | Open-Meteo Air Quality API | REST HTTP / JSON | $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$, $\text{O}_3$, European AQI, US EPA AQI | Hourly updates |
| **Marine & Sea State** | Open-Meteo Marine API | REST HTTP / JSON | Significant Wave Height, Wave Direction, Wave Period, Swell Wave Height, Swell Wave Period | Hourly updates |
| **Historical Climatology Baseline** | NASA POWER Agroclimatology (2010–2026) | Static JSON baseline (`district_climatology.json`) | 16-year daily means, standard deviations, and percentiles for $T_{\max}$, $T_{\min}$, Precipitation, Relative Humidity, Wind Speed, Root-zone Soil Wetness | Static 16-year baseline |
| **Demographic & Geographical Exposure** | Census of India & DES Tamil Nadu | Static JSON profile (`tamil_nadu_profiles.json`) | District population, population density, urbanization %, coastal zone indicator, mean elevation | Official administrative statistics |
| **Spatial Polygon Topologies** | Survey of India / District GIS | GeoJSON CRS84 (`tamil_nadu_districts.geojson`) | 38 WGS84 administrative district boundaries | Static administrative geometry |

---

## 2. Ingestion & Quality Control Principles

1. **Explicit Data Identification**: Every risk evaluation payload records the data provenance (e.g. `Open-Meteo NWP`, `NASA POWER`, `Open-Meteo Marine API`).
2. **Deterministic Caching**: All external API payloads are cached on disk (`data/cached_forecasts/`) and in-memory with a 3600-second TTL to guarantee reproducible assessments and avoid API rate throttling.
3. **No Silent Zero Imputation**: When an external variable or antecedent observation is missing, the system emits an explicit data quality warning or sets the status to `UNAVAILABLE` rather than defaulting to `0.0`.
