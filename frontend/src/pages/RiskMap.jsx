import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  Marker,
  Popup,
  useMap,
  useMapEvents
} from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {
  ShieldAlert,
  Search,
  Calendar,
  Layers,
  MapPin,
  Info,
  Users,
  Building2,
  Anchor,
  X,
  Flame,
  CloudRain,
  Droplets,
  Wind,
  Zap,
  Activity,
  Shield
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

// Custom Pin Icon for Leaflet
const customPinIcon = new L.DivIcon({
  className: 'custom-pin',
  html: `
    <div style="
      background: #06b6d4;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border: 3px solid #ffffff;
      box-shadow: 0 0 12px rgba(6, 182, 212, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
    ">
      <div style="background: white; width: 6px; height: 6px; border-radius: 50%;"></div>
    </div>
  `,
  iconSize: [24, 24],
  iconAnchor: [12, 12]
});

// Map Controller helper
function MapController({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom || 9, { duration: 1.2 });
    }
  }, [center, zoom, map]);
  return null;
}

// Map Click Listener
function MapClickListener({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick(e.latlng.lat, e.latlng.lng);
    }
  });
  return null;
}

export default function RiskMap() {
  const [hazard, setHazard] = useState('flood');
  const [dayIndex, setDayIndex] = useState(0);
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Selected Pin / Location Data
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [selectedDetails, setSelectedDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [mapCenter, setMapCenter] = useState([11.1271, 78.6569]); // Center of Tamil Nadu
  const [mapZoom, setMapZoom] = useState(7);

  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [showSearchDropdown, setShowSearchDropdown] = useState(false);

  // Load GeoJSON Overlay
  const loadRiskOverlay = async () => {
    setLoading(true);
    try {
      const resp = await axios.get(`${API_BASE}/gis/risk-overlay?hazard=${hazard}&day=${dayIndex}`);
      setGeoJsonData(resp.data);
    } catch (err) {
      console.error('Failed to load risk overlay:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRiskOverlay();
  }, [hazard, dayIndex]);

  // Debounced search
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      setShowSearchDropdown(false);
      return;
    }

    const timer = setTimeout(async () => {
      setSearching(true);
      try {
        const resp = await axios.get(`${API_BASE}/locations/search?q=${encodeURIComponent(searchQuery)}`);
        setSearchResults(resp.data || []);
        setShowSearchDropdown(true);
      } catch (err) {
        console.error('Location search failed:', err);
      } finally {
        setSearching(false);
      }
    }, 280);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Handle map click
  const handleMapClick = async (lat, lon) => {
    setSelectedPoint({ lat, lon });
    setDetailsLoading(true);
    try {
      // Find district via reverse geocode
      const revRes = await axios.get(`${API_BASE}/locations/reverse?lat=${lat}&lon=${lon}`);
      const districtId = revRes.data.district_id;

      if (!districtId) {
        setSelectedDetails({ error: 'Location outside Tamil Nadu operational domain.' });
        return;
      }

      const [hazardRes, forecastRes] = await Promise.all([
        axios.get(`${API_BASE}/risk/${districtId}/hazards?day=${dayIndex}`),
        axios.get(`${API_BASE}/forecast/${districtId}`)
      ]);

      setSelectedDetails({
        districtName: revRes.data.district_name,
        districtId: districtId,
        hazards: hazardRes.data.hazards,
        exposure: hazardRes.data.demographic_exposure,
        forecast: forecastRes.data
      });
    } catch (err) {
      console.warn('Coordinates lookup failed:', err);
      setSelectedDetails({ error: 'Selected point outside model domain.' });
    } finally {
      setDetailsLoading(false);
    }
  };

  const handleSelectSearchResult = (item) => {
    setSearchQuery(item.name);
    setShowSearchDropdown(false);
    setMapCenter([item.latitude, item.longitude]);
    setMapZoom(11);
    handleMapClick(item.latitude, item.longitude);
  };

  // Styling logic for GeoJSON polygons
  const getFeatureStyle = (feature) => {
    const props = feature.properties || {};
    const riskLevel = props.risk_level || 'LOW';

    let fillColor = '#10b981'; // LOW = emerald
    let fillOpacity = 0.40;

    if (riskLevel === 'SEVERE' || riskLevel === 'HIGH') {
      fillColor = '#f43f5e'; // HIGH / SEVERE = rose
      fillOpacity = 0.65;
    } else if (riskLevel === 'MEDIUM') {
      fillColor = '#f59e0b'; // MEDIUM = amber
      fillOpacity = 0.55;
    }

    return {
      fillColor,
      weight: 1.5,
      opacity: 0.9,
      color: '#334155',
      dashArray: '',
      fillOpacity
    };
  };

  const onEachFeature = (feature, layer) => {
    const props = feature.properties || {};
    const name = props.district_name || 'District';
    const prob = (props.probability !== undefined) ? (props.probability * 100).toFixed(1) : '0.0';
    const level = props.risk_level || 'LOW';

    layer.bindTooltip(`
      <div style="font-family: sans-serif; padding: 4px;">
        <strong style="color: #fff; font-size: 13px;">${name}</strong><br/>
        <span style="font-size: 11px; color: #94a3b8;">${hazard.toUpperCase()} Risk:</span>
        <strong style="color: ${level === 'HIGH' || level === 'SEVERE' ? '#f43f5e' : level === 'MEDIUM' ? '#f59e0b' : '#10b981'}; font-size: 12px;">
          ${level} (${prob}%)
        </strong>
      </div>
    `, { sticky: true, className: 'leaflet-tooltip-dark' });

    layer.on({
      mouseover: (e) => {
        const l = e.target;
        l.setStyle({
          weight: 3,
          color: '#38bdf8',
          fillOpacity: 0.8
        });
        l.bringToFront();
      },
      mouseout: (e) => {
        const l = e.target;
        l.setStyle(getFeatureStyle(feature));
      },
      click: (e) => {
        const lat = props.latitude || e.latlng.lat;
        const lon = props.longitude || e.latlng.lng;
        setMapCenter([lat, lon]);
        handleMapClick(lat, lon);
      }
    });
  };

  return (
    <div className="relative w-full h-[calc(100vh)] flex flex-col bg-slate-950 overflow-hidden select-none">
      {/* Top Floating Control Bar */}
      <div className="absolute top-4 left-4 right-4 z-20 flex flex-col md:flex-row items-center justify-between gap-3 pointer-events-none">
        {/* Search Bar */}
        <div className="relative w-full md:w-80 pointer-events-auto">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <Search className="w-4 h-4" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search landmark (Marina Beach, Avadi...)"
              className="w-full pl-9 pr-4 py-2.5 bg-slate-900/90 backdrop-blur-md border border-slate-700/80 rounded-xl text-xs text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 shadow-xl"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-white"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Autocomplete Dropdown */}
          {showSearchDropdown && searchResults.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1.5 bg-slate-900/95 backdrop-blur-xl border border-slate-700 rounded-xl shadow-2xl overflow-hidden z-50 max-h-60 overflow-y-auto">
              {searchResults.map((item, i) => (
                <div
                  key={i}
                  onClick={() => handleSelectSearchResult(item)}
                  className="p-2.5 hover:bg-slate-800/80 cursor-pointer border-b border-slate-800/60 last:border-0 flex items-center justify-between text-xs"
                >
                  <div>
                    <p className="font-semibold text-white">{item.name}</p>
                    <p className="text-[10px] text-slate-400">District: {item.district_name}</p>
                  </div>
                  <span className="text-[9px] bg-slate-800 text-cyan-400 px-1.5 py-0.5 rounded border border-slate-700">
                    {item.category}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Hazard Switcher & Day Timeline */}
        <div className="flex flex-wrap items-center gap-2 pointer-events-auto bg-slate-900/90 backdrop-blur-md p-1.5 rounded-2xl border border-slate-800/80 shadow-xl">
          {/* Hazard Buttons */}
          <div className="flex items-center space-x-1 pr-2 border-r border-slate-800">
            {[
              { key: 'flood', label: 'Flood' },
              { key: 'heatwave', label: 'Heatwave' },
              { key: 'drought', label: 'Drought' },
              { key: 'overall', label: 'Combined' }
            ].map((item) => (
              <button
                key={item.key}
                onClick={() => setHazard(item.key)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
                  hazard === item.key
                    ? 'bg-cyan-500 text-white shadow-md shadow-cyan-500/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>

          {/* Day Timeline */}
          <div className="flex items-center space-x-1 pl-1">
            {[0, 1, 2, 3, 4, 5, 6].map((day) => (
              <button
                key={day}
                onClick={() => setDayIndex(day)}
                className={`w-7 h-7 rounded-lg text-xs font-bold transition flex items-center justify-center ${
                  dayIndex === day
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
                title={`Day ${day === 0 ? 'Today' : day}`}
              >
                {day === 0 ? 'D0' : `D${day}`}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Map Container */}
      <div className="flex-1 w-full h-full relative z-0">
        <MapContainer
          center={mapCenter}
          zoom={mapZoom}
          className="w-full h-full"
          zoomControl={true}
          minZoom={6}
          maxZoom={14}
        >
          <MapController center={mapCenter} zoom={mapZoom} />
          <MapClickListener onMapClick={handleMapClick} />

          {/* CartoDB Dark Matter Base */}
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://carto.com/">CARTO</a>'
          />

          {/* Tamil Nadu 38 District Choropleth Polygons */}
          {geoJsonData && (
            <GeoJSON
              key={`${hazard}_${dayIndex}_${geoJsonData.features?.length}`}
              data={geoJsonData}
              style={getFeatureStyle}
              onEachFeature={onEachFeature}
            />
          )}

          {/* Selected Marker */}
          {selectedPoint && (
            <Marker position={[selectedPoint.lat, selectedPoint.lon]} icon={customPinIcon}>
              <Popup className="leaflet-popup-dark">
                <div className="p-1 text-xs">
                  <p className="font-bold text-white">Selected Coordinate</p>
                  <p className="text-cyan-400 text-[10px]">
                    {selectedPoint.lat.toFixed(4)}, {selectedPoint.lon.toFixed(4)}
                  </p>
                </div>
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </div>

      {/* Legend Card */}
      <div className="absolute bottom-6 left-6 z-20 pointer-events-auto bg-slate-900/90 backdrop-blur-md p-3.5 rounded-xl border border-slate-800 shadow-xl text-xs space-y-2 max-w-[200px]">
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Hazard Risk Scale
        </span>
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2">
            <span className="w-3.5 h-3.5 rounded bg-rose-500 opacity-80"></span>
            <span className="text-slate-300 text-[11px]">High / Severe Risk (≥ 70%)</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-3.5 h-3.5 rounded bg-amber-500 opacity-80"></span>
            <span className="text-slate-300 text-[11px]">Medium Risk (40-69%)</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-3.5 h-3.5 rounded bg-emerald-500 opacity-80"></span>
            <span className="text-slate-300 text-[11px]">Low Risk (&lt; 40%)</span>
          </div>
        </div>
      </div>

      {/* Multi-Hazard Spatial Analytics Drawer */}
      {selectedPoint && (
        <div className="absolute bottom-6 right-6 z-20 pointer-events-auto w-[400px] max-h-[85vh] overflow-y-auto glass-card p-5 border-slate-700/80 shadow-2xl space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-200">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center space-x-2">
              <MapPin className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white">Spatial Risk Assessment</h3>
            </div>
            <button
              onClick={() => setSelectedPoint(null)}
              className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {detailsLoading ? (
            <div className="py-12 flex flex-col items-center justify-center space-y-2 text-xs text-slate-400">
              <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
              <span>Resolving containing polygon & multi-hazard portfolio...</span>
            </div>
          ) : selectedDetails?.error ? (
            <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-xs text-rose-300">
              {selectedDetails.error}
            </div>
          ) : (
            <div className="space-y-4 text-xs">
              {/* Containing District Match */}
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-[11px]">Containing District:</span>
                  <span className="font-bold text-white text-sm">
                    {selectedDetails?.districtName}
                  </span>
                </div>
                <p className="text-[10px] text-cyan-400/90 mt-1">
                  Coordinates: {selectedPoint.lat.toFixed(4)}°N, {selectedPoint.lon.toFixed(4)}°E
                </p>
              </div>

              {/* Point Weather Snippet */}
              {selectedDetails?.forecast?.current && (
                <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800/80">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">
                    Localized Coordinates Weather
                  </span>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-2xl font-extrabold text-white">
                      {selectedDetails.forecast.current.temperature_c}°C
                    </span>
                    <span className="text-slate-300 font-medium">
                      {selectedDetails.forecast.current.condition}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-1">
                    Humidity: {selectedDetails.forecast.current.humidity_pct}% • Wind: {selectedDetails.forecast.current.wind_speed_ms} m/s
                  </p>
                </div>
              )}

              {/* Multi-Hazard Grid in Drawer */}
              {selectedDetails?.hazards && (
                <div className="space-y-2">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">
                    Registered Hazards Portfolio (Day {dayIndex})
                  </span>

                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(selectedDetails.hazards).map(([hid, h]) => (
                      <div key={hid} className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] text-slate-400 font-medium truncate max-w-[100px]">{h.hazard_name}</span>
                          <span className={`text-[8px] font-bold px-1.5 py-0.2 rounded border ${
                            h.status === 'NOT_APPLICABLE' ? 'bg-slate-800 text-slate-400 border-slate-700' :
                            h.risk_level === 'HIGH' || h.risk_level === 'SEVERE' ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' :
                            h.risk_level === 'MEDIUM' ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' :
                            'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                          }`}>
                            {h.status === 'UNAVAILABLE' ? 'UNAVAILABLE' : h.status === 'NOT_APPLICABLE' ? 'N/A' : h.risk_level}
                          </span>
                        </div>
                        <span className="font-bold text-white text-xs block mt-1">
                          {h.display_value}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Exposure Context */}
              {selectedDetails?.exposure && (
                <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-[11px] space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Population:</span>
                    <span className="text-white font-semibold">
                      {selectedDetails.exposure.population?.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Coastal Zone:</span>
                    <span className="text-white font-semibold">
                      {selectedDetails.exposure.coastal ? 'Yes (Maritime Hazard Applicable)' : 'No (Inland)'}
                    </span>
                  </div>
                </div>
              )}

              {/* Scientific Resolution Disclaimer */}
              <div className="pt-2 border-t border-slate-800 text-[10px] text-slate-400 flex items-start space-x-1.5">
                <Info className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0 mt-0.5" />
                <span>
                  Multi-hazard decision support framework combining ML classifiers, IMD/WMO rules, and real-time sensor streams.
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
