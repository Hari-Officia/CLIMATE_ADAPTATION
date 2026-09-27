# Frontend Architecture Summary

## 💻 Overview
The **Frontend Application** is a responsive single-page web interface built with **React 18**, **Vite**, and **TailwindCSS**. It provides an interactive visual control center for climate hazard monitoring, district risk analysis, vector-search evidence retrieval, and quantum portfolio optimization control.

---

## 🎨 UI Pages & Components

| Page Component | Path / Route | Core Functionality |
|---|---|---|
| `RiskMap.jsx` | `/` | Leaflet choropleth map displaying 38 TN district risk levels and active hazard overlays |
| `Dashboard.jsx` | `/dashboard` | Executive summary widgets, state-wide risk distribution, top priority interventions |
| `DistrictDetail.jsx` | `/district/:id` | 7-day climate forecast chart, SVI breakdown, localized strategy recommendations |
| `OptimizationOverview.jsx` | `/optimization` | Portfolio budget sliders, sector constraint toggles, solver selector (MILP vs QAOA) |
| `QAOAResearch.jsx` | `/quantum` | Quantum circuit parameters, bitstring measurement histogram, gap analysis |
| `EvidenceCenter.jsx` | `/evidence` | RAG natural language search interface with IPCC citation verification cards |
| `SystemStatus.jsx` | `/status` | Real-time service health, PostgreSQL connection pool, Open-Meteo latency monitoring |

---

## 🔌 API Service Integration Layer

The frontend communicates with FastAPI endpoints via centralized service wrappers:
* `apiService.js`: Unified fetch client with bearer token authentication headers.
* `forecastService.js`: Weather & NWP forecast query hook.
* `optimizationService.js`: Triggers QUBO generation and QAOA quantum execution.

---

## 💻 Minimal Code Example

```jsx
// frontend/src/components/RiskChoroplethMap.jsx
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';

export default function RiskChoroplethMap({ districtRisks, onSelectDistrict }) {
  const [geoJsonData, setGeoJsonData] = useState(null);

  useEffect(() => {
    fetch('/api/v1/gis/districts')
      .then(res => res.json())
      .then(data => setGeoJsonData(data));
  }, []);

  const getDistrictStyle = (feature) => {
    const districtId = feature.properties.shapeName.toLowerCase().replace(" ", "_");
    const riskScore = districtRisks[districtId] || 0.0;
    
    return {
      fillColor: riskScore > 0.75 ? '#ef4444' : riskScore > 0.50 ? '#f97316' : '#22c55e',
      weight: 1.5,
      opacity: 1,
      color: '#ffffff',
      fillOpacity: 0.7
    };
  };

  return (
    <div className="h-[600px] w-full rounded-xl overflow-hidden shadow-lg">
      <MapContainer center={[11.1271, 78.6569]} zoom={7} className="h-full w-full">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {geoJsonData && (
          <GeoJSON 
            data={geoJsonData} 
            style={getDistrictStyle} 
            onEachFeature={(feat, layer) => {
              layer.on('click', () => onSelectDistrict(feat.properties.shapeName));
            }}
          />
        )}
      </MapContainer>
    </div>
  );
}
```
