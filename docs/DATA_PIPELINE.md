# Climate Data Pipeline — Review II

## 1. Overview
The Climate Data Pipeline ingests multi-source meteorological data, harmonizes temporal and spatial resolutions, normalizes physical units, and generates validated data structures for feature engineering and downstream risk assessment.

---

## 2. Ingestion Sources

### A. Historical Climatology (NASA POWER)
- **Source**: NASA Prediction of Worldwide Energy Resources (POWER) Daily Gridded Meteorology (MERRA-2).
- **Time Horizon**: January 1, 2010 through June 30, 2026.
- **Coverage**: All 38 Tamil Nadu districts.
- **Variables**: `T2M_MAX`, `T2M_MIN`, `T2M_RANGE`, `RH2M`, `WS2M`, `GWETROOT`, `PRECTOTCORR`.
- **Precomputed Baseline**: Saved to `data/feature_mappings/district_climatology.json` with monthly and annual means and standard deviations.

### B. Operational Forecast (Open-Meteo API)
- **Source**: Open-Meteo Numerical Weather Prediction (NWP) API.
- **Spatial Resolution**: Variable (interpolated to request coordinates).
- **Temporal Resolution**: Hourly for 24–72 hours, daily aggregated for 7 days.
- **Variables**: 2m Temperature, Relative Humidity, 10m Wind Speed, Surface Pressure, Precipitation, Root-zone Soil Moisture, WMO Weather Code.

---

## 3. Normalization Standards

| Variable | Raw Unit | Target Pipeline Unit | Normalization Function |
|---|---|---|---|
| Temperature | °C | °C | Direct |
| Relative Humidity | % | % | Clamped to $[0, 100]$ |
| Wind Speed | km/h or m/s | m/s | Normalized to m/s |
| Precipitation | mm/h or mm/day | mm/day | Summed over daily 24h window |
| Soil Moisture | $m^3/m^3$ or fraction | Fraction ($0.0 - 1.0$) | Clamped to $[0.0, 1.0]$ |

---

## 4. Caching & Resilience Strategy

1. **In-Memory Cache**: Python dictionary keyed by coordinate grid (`{lat}_{lon}`) with 1-hour TTL.
2. **Persistent Disk Cache**: JSON payloads stored in `data/cached_forecasts/` to survive process restarts.
3. **Synthetic Climatological Fallback**: If network or Open-Meteo API experiences downtime, the system automatically serves the latest cached forecast or generates seasonal synthetic observations from historical district normals, ensuring zero system outages.
