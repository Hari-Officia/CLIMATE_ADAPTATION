# Review II Live Demonstration Script & Walkthrough

## Overview
This document outlines the step-by-step procedure for demonstrating the **Quantum Multi-Agent Decision Support System for Climate Adaptation and Mitigation Strategy Planning (Review II)** to project reviewers and faculty evaluators.

---

## Step 1: User Authentication & Role-Based Access Control
1. Open the application in your browser at `http://localhost:5173`.
2. Observe the climate-themed login screen with dark aesthetic and quick preset login buttons.
3. Click **"Login as Harish (USER)"**:
   - Authenticates via `POST /auth/login` using JWT and Bcrypt.
   - Shows badge: `Harish Kumar` with `USER` role.
4. Verify restricted admin controls:
   - Notice that administrative cache purge actions are protected with `403 Forbidden` for standard users.
5. Log out and click **"Login as Admin (ADMIN)"**:
   - Displays `System Administrator` with `ADMIN` badge, granting access to system management and cache purge actions.

---

## Step 2: Executive Dashboard (`/dashboard`)
1. Navigate to `/dashboard`.
2. Inspect the **Current Climate Risk Overview** banner showing real-time atmospheric metrics for the selected district.
3. Inspect the three **Multi-Hazard Risk Cards**:
   - **Flood Risk**: Shows probability meter, calibrated status (`LOW`/`MEDIUM`/`HIGH`), and rare-event uncertainty flag.
   - **Heatwave Risk**: Displays diurnal temperature departure.
   - **Drought Risk**: Displays multi-month precipitation balance and SPI status.
4. Review the **7-Day Risk Trend Chart** visualizing multi-hazard risk trajectory across the forecast horizon.
5. Review the **Multi-Agent System Activity Stream** detailing real-time agent coordination.

---

## Step 3: Weather Experience (`/weather`)
1. Navigate to `/weather`.
2. Experience the ambient weather background reacting to prevailing conditions (rain droplets, sun shimmer, clouds).
3. View the **Current Atmospheric Status**: large temperature display, condition description, feels-like, wind speed, and humidity.
4. Scroll the **24-Hour Hourly Forecast Slider** to view temperature and precipitation progression.
5. Review the **7-Day Forecast Grid** with high/low temperature range bars.
6. Inspect detailed atmospheric metric cards: Surface Pressure, Soil Moisture, Wind Speed, and Precipitation accumulation.

---

## Step 4: Interactive GIS Risk Map (`/risk-map`)
1. Navigate to `/risk-map`.
2. Verify all **38 Tamil Nadu district polygons** rendered with Leaflet.
3. Switch Hazard Layers:
   - Click **[Flood Risk]**: districts update to emerald (Low), amber (Medium), or crimson (High).
   - Click **[Heatwave Risk]** and **[Drought Risk]** to observe hazard choropleth shifts.
4. Adjust the **Date Timeline Slider** from Day 0 (Today) through Day 6 (Day 7) to inspect temporal hazard progression.
5. Test Search & Geocoding:
   - Type `"Marina Beach"` in the search bar and select the suggestion.
   - The map animates to Marina Beach, places a marker, and the analytical panel highlights `Chennai` as the containing district.
   - Type `"Coimbatore Airport"` or `"Avadi"` to verify boundary containment.
6. Click anywhere inside Tamil Nadu to drop a custom pin:
   - The side/bottom drawer immediately updates with the exact coordinates, containing district, point weather, ML hazard probabilities, and demographic exposure (population, density, coastal tag).

---

## Step 5: System Status & Model Verification (`/system-status`)
1. Navigate to `/system-status`.
2. Inspect the **Live Health Grid**:
   - API Gateway: `ONLINE`
   - Database Engine: `SQLite Fallback / PostgreSQL`
   - District GeoJSON: `38/38 Verified`
   - Climate Data Acquisition Agent: `ONLINE`
   - Multi-Hazard Risk Agent: `ONLINE`
3. Inspect the **Model Registry Table**:
   - `flood_xgboost.pkl`: 53 features, ROC-AUC 0.906, PR-AUC 0.074.
   - `drought_xgboost.pkl`: 53 features, ROC-AUC 0.9998, PR-AUC 0.9993.
   - `heatwave_xgboost.pkl`: 53 features, ROC-AUC 1.0000, PR-AUC 0.9964.
4. Click **"Inspect Feature Schema"** to view all 53 expected input features in exact sequence (15 continuous variables + 38 district one-hot columns).

---

## Step 6: Automated Verification
Run the comprehensive test suite directly:
```bash
python scripts/run_all_tests.py
```
Demonstrates 15 passing automated tests across all 6 core submodules with zero failures.
