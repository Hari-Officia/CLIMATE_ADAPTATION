# Forecast API Summary

## 🌐 Overview
The **Forecast API** subsystem serves as the primary gateway for acquiring real-time and 7-day numerical weather prediction (NWP) forecasts for all 38 districts of Tamil Nadu. It integrates the external Open-Meteo REST API with a local 30-year climatological baseline fallback mechanism, ensuring 100% service availability even during external API downtime.

---

## 🚀 Key Endpoints

| Method | Endpoint | Description | Query/Path Params | Response Model |
|---|---|---|---|---|
| `GET` | `/api/v1/forecast/coordinates` | Get forecast by geographic coordinates | `lat` (float, -90 to 90), `lon` (float, -180 to 180) | `ForecastResponse` |
| `GET` | `/api/v1/forecast/{district_id}` | Get 7-day forecast by district ID or name | `district_id` (string e.g. `"chennai"`, `"madurai"`) | `ForecastResponse` |

---

## 📊 Data Pipeline & Variables

The Forecast API fetches both **daily** and **hourly** climate variables required for feature engineering:
* **Daily Variables**: `temperature_2m_max`, `temperature_2m_min`, `precipitation_sum`, `wind_speed_10m_max`.
* **Hourly Variables**: `relative_humidity_2m`, `soil_moisture_0_to_1cm`.

### Resiliency & Fallback Strategy
1. **Open-Meteo Query**: Async HTTP GET request with a 5-second timeout.
2. **Reverse Geocoding**: Coordinates are dynamically resolved to one of the 38 Tamil Nadu district IDs using `GeocodingService`.
3. **Climatological Fallback**: If Open-Meteo request times out or fails, `FeatureEngineeringService.get_district_baseline()` injects historical 30-year monthly averages.

---

## 💻 Minimal Code Example

```python
# backend/api/forecast.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District
from backend.agents.climate_data_agent import ClimateDataAgent
from backend.schemas.forecast import ForecastResponse

router = APIRouter(prefix="/api/v1/forecast", tags=["Climate Forecast"])

@router.get("/{district_id}", response_model=ForecastResponse)
async def get_forecast_by_district(district_id: str, db: Session = Depends(get_db)):
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()

    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    # Fetch 7-day forecast via agent with automatic fallback
    forecast_data = await ClimateDataAgent.get_forecast(
        lat=district.latitude,
        lon=district.longitude,
        district_id=district.district_id
    )

    return {
        **forecast_data,
        "district_id": district.district_id,
        "district_name": district.district_name
    }
```
