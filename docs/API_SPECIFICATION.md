# REST API Specification — Review II

## Base URL
All API endpoints are served at `http://localhost:8000`. Swagger documentation is available interactively at `/docs`.

---

## 1. Authentication Endpoints

### `POST /auth/login`
Authenticates a user and issues an HMAC-SHA256 JWT access token.
- **Request Body**: JSON or Form Data with `username` and `password`.
- **Response** (`200 OK`):
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer",
  "role": "USER",
  "username": "harish",
  "full_name": "Harish Kumar"
}
```

### `GET /auth/me`
Returns current authenticated user details.
- **Headers**: `Authorization: Bearer <token>`
- **Response** (`200 OK`):
```json
{
  "id": 2,
  "username": "harish",
  "role": "USER",
  "full_name": "Harish Kumar",
  "email": "harish@climaterisk.tn.gov.in"
}
```

---

## 2. District & Geographic Endpoints

### `GET /districts`
Returns a list of all 38 Tamil Nadu administrative districts.

### `GET /districts/{district_id}`
Returns details for a specific district (e.g., `chennai`, `coimbatore`).

### `GET /districts/{district_id}/profile`
Returns demographic and vulnerability data:
```json
{
  "population": 7088403,
  "area_km2": 426.0,
  "population_density": 16639.4,
  "urban_percentage": 100.0,
  "coastal": true,
  "elevation_m": 6.0,
  "source": "Census of India & Tamil Nadu DES",
  "source_year": 2021
}
```

---

## 3. Location Search & Point-in-Polygon

### `GET /locations/search?q={query}&limit=8`
Debounced search resolving arbitrary landmarks, towns, and district centers to coordinates and containing districts.

### `GET /locations/reverse?lat={lat}&lon={lon}`
Returns containing Tamil Nadu district for arbitrary coordinates via Shapely point-in-polygon.

---

## 4. Climate Forecast Endpoints

### `GET /forecast/coordinates?lat={lat}&lon={lon}`
Returns normalized current, hourly (24h), and daily (7d) weather forecast from Open-Meteo.

### `GET /forecast/{district_id}`
Returns forecast for the centroid coordinates of the district.

---

## 5. Multi-Hazard Risk Assessment Endpoints

### `GET /risk/district/{district_id}?day={0-6}`
Returns ML ensemble risk predictions for a district and forecast day:
```json
{
  "district_id": "chennai",
  "district_name": "Chennai",
  "date": "2026-08-31",
  "spatial_resolution": "District-level (Administrative ADM2)",
  "model_status": "Verified XGBoost Ensemble (53 features)",
  "assessment": {
    "date": "2026-08-31",
    "flood": {
      "probability": 0.0821,
      "risk_level": "LOW",
      "threshold_applied": 0.0,
      "confidence_note": "High rare-event uncertainty. Cross-checked with rolling rainfall accumulation."
    },
    "heatwave": {
      "probability": 0.0412,
      "risk_level": "LOW",
      "threshold_applied": 0.0,
      "confidence_note": "Reflects daytime temperature departure from historical baseline."
    },
    "drought": {
      "probability": 0.1250,
      "risk_level": "LOW",
      "threshold_applied": 0.0,
      "confidence_note": "Reflects slow-onset multi-month moisture and precipitation deficit."
    },
    "overall_hazard_level": "LOW"
  }
}
```

### `GET /risk/timeline/{district_id}`
Returns 7-day multi-hazard risk timeline for the district.

---

## 6. GIS & Choropleth Endpoints

### `GET /gis/districts-geojson`
Returns GeoJSON FeatureCollection with all 38 districts and demographic properties.

### `GET /gis/risk-overlay?hazard={flood|heatwave|drought|overall}&day={0-6}`
Returns GeoJSON FeatureCollection enriched with live ML hazard probabilities and risk levels for instant client-side rendering.

---

## 7. System Monitoring & Administration

### `GET /system/status`
Returns live health check of all components (API, DB, GeoJSON, Models, Agents).

### `POST /system/admin/refresh-forecast`
Purges forecast caches (requires `ADMIN` role).
