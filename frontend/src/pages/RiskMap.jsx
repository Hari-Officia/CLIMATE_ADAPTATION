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
  Search,
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
  Shield,
  Activity,
  Compass,
  CheckCircle,
  AlertTriangle,
  Clock,
  ExternalLink
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

// Professional Google-Maps style pin icon
const customLocationPin = new L.DivIcon({
  className: 'gmaps-pin',
  html: `
    <div style="
      position: relative;
      width: 28px;
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: center;
    ">
      <svg width="28" height="38" viewBox="0 0 24 34" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 0C5.37 0 0 5.37 0 12C0 21 12 34 12 34C12 34 24 21 24 12C24 5.37 18.63 0 12 0Z" fill="#EA4335" stroke="#FFFFFF" stroke-width="1.5"/>
        <circle cx="12" cy="11" r="5" fill="#FFFFFF"/>
      </svg>
    </div>
  `,
  iconSize: [28, 38],
  iconAnchor: [14, 38],
  popupAnchor: [0, -36]
});

// Map Controller for smooth flyTo
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
  const [loadingOverlay, setLoadingOverlay] = useState(true);

  // Selected Pin / Location Data
  const [selectedPoint, setSelectedPoint] = useState({ lat: 13.0827, lon: 80.2707 }); // Default Chennai
  const [selectedDetails, setSelectedDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [mapCenter, setMapCenter] = useState([11.1271, 78.6569]); // Center of Tamil Nadu
  const [mapZoom, setMapZoom] = useState(7);

  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [showSearchDropdown, setShowSearchDropdown] = useState(false);

  // Layer control state
  const [showBoundaries, setShowBoundaries] = useState(true);
  const [showRiskOverlay, setShowRiskOverlay] = useState(true);
  const [activeBasemap, setActiveBasemap] = useState('road'); // 'road' | 'light' | 'dark'

  // Load GeoJSON Overlay from authoritative API
  const loadRiskOverlay = async () => {
    setLoadingOverlay(true);
    try {
      const resp = await axios.get(`${API_BASE}/gis/risk-overlay?hazard=${hazard}&day=${dayIndex}`);
      setGeoJsonData(resp.data);
    } catch (err) {
      console.error('Failed to load risk overlay:', err);
    } finally {
      setLoadingOverlay(false);
    }
  };

  useEffect(() => {
    loadRiskOverlay();
  }, [hazard, dayIndex]);

  // Initial load for default location
  useEffect(() => {
    handleMapClick(13.0827, 80.2707, 'Chennai');
  }, []);

  // Debounced place search
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
    }, 250);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Handle map click with authoritative multi-hazard & point-in-polygon resolution
  const handleMapClick = async (lat, lon, placeLabel = null) => {
    setSelectedPoint({ lat, lon });
    setDetailsLoading(true);
    try {
      // 1. Identify containing district via Point-in-Polygon
      const revRes = await axios.get(`${API_BASE}/locations/reverse?lat=${lat}&lon=${lon}`);
      const districtId = revRes.data.district_id;
      const districtName = revRes.data.district_name;

      if (!districtId) {
        setSelectedDetails({
          placeName: placeLabel || `${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E`,
          error: "Location outside supported Tamil Nadu boundary."
        });
        return;
      }

      // 2. Fetch authoritative risk bundle and forecast
      const [riskRes, forecastRes] = await Promise.all([
        axios.get(`${API_BASE}/risk/district/${districtId}?day=${dayIndex}`),
        axios.get(`${API_BASE}/forecast/${districtId}`)
      ]);

      setSelectedDetails({
        placeName: placeLabel || districtName,
        districtName: districtName,
        districtId: districtId,
        riskAssessment: riskRes.data.assessment,
        demographicExposure: riskRes.data.demographic_exposure,
        forecast: forecastRes.data,
        timestamp: new Date().toLocaleTimeString()
      });
    } catch (err) {
      console.warn('Point resolution failed:', err);
      setSelectedDetails({
        placeName: placeLabel || `${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E`,
        error: "Location outside supported Tamil Nadu boundary."
      });
    } finally {
      setDetailsLoading(false);
    }
  };

  const handleSelectSearchResult = (item) => {
    setSearchQuery(item.name);
    setShowSearchDropdown(false);
    setMapCenter([item.latitude, item.longitude]);
    setMapZoom(11);
    handleMapClick(item.latitude, item.longitude, item.name);
  };

  // Authoritative GIS Styling logic
  const getFeatureStyle = (feature) => {
    if (!showRiskOverlay) {
      return {
        fillColor: '#64748b',
        weight: 1.5,
        opacity: 0.8,
        color: '#475569',
        fillOpacity: 0.05
      };
    }

    const props = feature.properties || {};
    const riskLevel = props.risk_level;

    let fillColor = '#10b981'; // LOW = green
    let fillOpacity = 0.45;

    if (riskLevel === 'HIGH' || riskLevel === 'SEVERE') {
      fillColor = '#ef4444'; // HIGH = red
      fillOpacity = 0.65;
    } else if (riskLevel === 'MEDIUM') {
      fillColor = '#f59e0b'; // MEDIUM = amber/yellow
      fillOpacity = 0.55;
    } else if (riskLevel === 'UNAVAILABLE' || riskLevel === null) {
      fillColor = '#94a3b8'; // UNAVAILABLE = neutral gray
      fillOpacity = 0.30;
    }

    return {
      fillColor,
      weight: showBoundaries ? 1.5 : 0.5,
      opacity: 0.9,
      color: '#334155',
      dashArray: '',
      fillOpacity
    };
  };

  const onEachFeature = (feature, layer) => {
    const props = feature.properties || {};
    const name = props.district_name || 'District';
    const level = props.risk_level || 'LOW';
    const probStr = props.probability !== null && props.probability !== undefined
      ? `${(props.probability * 100).toFixed(1)}%`
      : 'Unavailable (No SPI)';

    layer.bindTooltip(`
      <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 4px;">
        <strong style="color: #0f172a; font-size: 13px;">${name}</strong><br/>
        <span style="font-size: 11px; color: #64748b;">${hazard.toUpperCase()} Risk:</span>
        <strong style="color: ${level === 'HIGH' || level === 'SEVERE' ? '#ef4444' : level === 'MEDIUM' ? '#f59e0b' : level === 'UNAVAILABLE' ? '#64748b' : '#10b981'}; font-size: 12px;">
          ${level} ${props.probability !== null ? `(${probStr})` : ''}
        </strong>
      </div>
    `, { sticky: true, className: 'leaflet-tooltip-clean' });

    layer.on({
      mouseover: (e) => {
        const l = e.target;
        l.setStyle({
          weight: 2.5,
          color: '#0284c7',
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
        handleMapClick(lat, lon, name);
      }
    });
  };

  const basemapTiles = {
    road: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    light: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
  };

  return (
    <div className="relative w-full h-[calc(100vh)] flex flex-col bg-slate-100 overflow-hidden font-sans">
      {/* Top Floating Google-Maps Style Search & Control Bar */}
      <div className="absolute top-4 left-4 z-[1000] flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        {/* Search Box */}
        <div className="relative w-80 sm:w-96 shadow-lg rounded-2xl bg-white border border-slate-200">
          <div className="flex items-center px-3.5 py-2.5">
            <Search className="w-5 h-5 text-slate-400 mr-2 flex-shrink-0" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search place in Tamil Nadu (e.g. Marina Beach, Avadi)"
              className="w-full text-xs sm:text-sm text-slate-800 placeholder-slate-400 focus:outline-none bg-transparent"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Autocomplete Results */}
          {showSearchDropdown && searchResults.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1.5 bg-white border border-slate-200 rounded-2xl shadow-2xl overflow-hidden z-[1010] max-h-64 overflow-y-auto">
              {searchResults.map((item, i) => (
                <div
                  key={i}
                  onClick={() => handleSelectSearchResult(item)}
                  className="px-4 py-2.5 hover:bg-slate-50 cursor-pointer border-b border-slate-100 last:border-0 flex items-center justify-between text-xs"
                >
                  <div>
                    <p className="font-semibold text-slate-800">{item.name}</p>
                    <p className="text-[11px] text-slate-500">District: {item.district_name}</p>
                  </div>
                  <span className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
                    {item.category}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Hazard & Horizon Selector */}
        <div className="flex items-center gap-1.5 p-1 bg-white border border-slate-200 shadow-lg rounded-2xl">
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
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {item.label}
            </button>
          ))}

          {/* Forecast Days */}
          <div className="flex items-center pl-2 border-l border-slate-200 space-x-1">
            {[0, 1, 2, 3, 4, 5, 6].map((day) => (
              <button
                key={day}
                onClick={() => setDayIndex(day)}
                className={`w-6 h-6 rounded-lg text-[11px] font-bold transition flex items-center justify-center ${
                  dayIndex === day
                    ? 'bg-slate-800 text-white'
                    : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'
                }`}
                title={`Day ${day === 0 ? 'Today' : day}`}
              >
                {day === 0 ? 'D0' : `D${day}`}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Layer Control Card (Bottom Left) */}
      <div className="absolute bottom-6 left-6 z-[1000] bg-white border border-slate-200 shadow-xl rounded-2xl p-3 text-xs space-y-2 max-w-[220px]">
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Map Layers & Scale
        </span>

        {/* Risk Level Colors */}
        <div className="space-y-1 pb-2 border-b border-slate-100">
          <div className="flex items-center space-x-2">
            <span className="w-3 h-3 rounded bg-rose-500"></span>
            <span className="text-slate-700 text-[11px]">High (≥ 70%)</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-3 h-3 rounded bg-amber-500"></span>
            <span className="text-slate-700 text-[11px]">Medium (40–69%)</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-3 h-3 rounded bg-emerald-500"></span>
            <span className="text-slate-700 text-[11px]">Low (&lt; 40%)</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-3 h-3 rounded bg-slate-400"></span>
            <span className="text-slate-700 text-[11px]">Unavailable</span>
          </div>
        </div>

        {/* Toggles */}
        <div className="space-y-1.5 pt-1">
          <label className="flex items-center space-x-2 cursor-pointer text-slate-700">
            <input
              type="checkbox"
              checked={showRiskOverlay}
              onChange={(e) => setShowRiskOverlay(e.target.checked)}
              className="rounded text-blue-600 focus:ring-0"
            />
            <span>Hazard Risk Overlay</span>
          </label>
          <label className="flex items-center space-x-2 cursor-pointer text-slate-700">
            <input
              type="checkbox"
              checked={showBoundaries}
              onChange={(e) => setShowBoundaries(e.target.checked)}
              className="rounded text-blue-600 focus:ring-0"
            />
            <span>District Boundaries</span>
          </label>
        </div>
      </div>

      {/* Main Interactive Map */}
      <div className="flex-1 w-full h-full relative z-0">
        <MapContainer
          center={mapCenter}
          zoom={mapZoom}
          className="w-full h-full"
          zoomControl={true}
          minZoom={6}
          maxZoom={15}
        >
          <MapController center={mapCenter} zoom={mapZoom} />
          <MapClickListener onMapClick={handleMapClick} />

          {/* Standard Road Map Tiles */}
          <TileLayer
            url={basemapTiles[activeBasemap]}
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {/* GeoJSON District Polygons */}
          {geoJsonData && (
            <GeoJSON
              key={`${hazard}_${dayIndex}_${showRiskOverlay}_${showBoundaries}`}
              data={geoJsonData}
              style={getFeatureStyle}
              onEachFeature={onEachFeature}
            />
          )}

          {/* Location Pin */}
          {selectedPoint && (
            <Marker position={[selectedPoint.lat, selectedPoint.lon]} icon={customLocationPin}>
              <Popup>
                <div className="text-xs">
                  <strong>{selectedDetails?.placeName || 'Selected Place'}</strong>
                  <p className="text-slate-500 text-[10px]">
                    {selectedPoint.lat.toFixed(4)}°N, {selectedPoint.lon.toFixed(4)}°E
                  </p>
                </div>
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </div>

      {/* Right Floating Google-Maps Style Risk Information Panel */}
      {selectedPoint && (
        <div className="absolute top-4 right-4 bottom-6 z-[1000] w-96 max-w-[calc(100vw-32px)] bg-white border border-slate-200 shadow-2xl rounded-3xl p-5 overflow-y-auto space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            {/* Panel Header */}
            <div className="flex items-start justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <div className="p-2 rounded-xl bg-blue-50 text-blue-600">
                  <MapPin className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900 leading-tight">
                    {selectedDetails?.placeName || 'Selected Location'}
                  </h3>
                  <p className="text-xs text-slate-500">
                    District: {selectedDetails?.districtName || 'Resolving...'}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSelectedPoint(null)}
                className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {detailsLoading ? (
              <div className="py-16 flex flex-col items-center justify-center space-y-3 text-xs text-slate-500">
                <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <span>Executing Point-in-Polygon & ML Risk Inference...</span>
              </div>
            ) : selectedDetails?.error ? (
              <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-xs text-rose-700 flex items-start space-x-2">
                <AlertTriangle className="w-4 h-4 text-rose-500 flex-shrink-0 mt-0.5" />
                <span>{selectedDetails.error}</span>
              </div>
            ) : (
              <>
                {/* 1. Current Weather Section */}
                {selectedDetails?.forecast?.current && (
                  <div className="p-4 bg-slate-50 border border-slate-200/80 rounded-2xl space-y-2">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                      Current Atmospheric State
                    </span>
                    <div className="flex items-baseline justify-between">
                      <div>
                        <span className="text-3xl font-extrabold text-slate-900">
                          {selectedDetails.forecast.current.temperature_c}°C
                        </span>
                        <span className="text-xs text-slate-500 block">
                          Feels like {selectedDetails.forecast.current.feels_like_c}°C
                        </span>
                      </div>
                      <span className="text-xs font-semibold text-blue-700 bg-blue-100/70 px-2.5 py-1 rounded-full">
                        {selectedDetails.forecast.current.condition}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-200/60 text-xs text-slate-600">
                      <div>Rainfall: <strong>{selectedDetails.forecast.current.precipitation_mm} mm</strong></div>
                      <div>Humidity: <strong>{selectedDetails.forecast.current.humidity_pct}%</strong></div>
                      <div>Wind: <strong>{selectedDetails.forecast.current.wind_speed_ms} m/s</strong></div>
                      <div>High/Low: <strong>{selectedDetails.forecast.current.high_c}° / {selectedDetails.forecast.current.low_c}°</strong></div>
                    </div>
                  </div>
                )}

                {/* 2. Authoritative Multi-Hazard Risk Section */}
                {selectedDetails?.riskAssessment && (
                  <div className="space-y-2.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                        Authoritative ML Climate Risk (Day {dayIndex})
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        selectedDetails.riskAssessment.overall_hazard_level === 'HIGH' ? 'bg-rose-100 text-rose-700' :
                        selectedDetails.riskAssessment.overall_hazard_level === 'MEDIUM' ? 'bg-amber-100 text-amber-700' :
                        selectedDetails.riskAssessment.overall_hazard_level === 'LOW' ? 'bg-emerald-100 text-emerald-700' :
                        'bg-slate-100 text-slate-600'
                      }`}>
                        {selectedDetails.riskAssessment.overall_hazard_level} OVERALL
                      </span>
                    </div>

                    <div className="space-y-2">
                      {/* Flood Card */}
                      <div className="p-3 bg-white border border-slate-200 rounded-2xl flex items-center justify-between">
                        <div className="flex items-center space-x-2.5">
                          <CloudRain className="w-5 h-5 text-blue-500" />
                          <div>
                            <p className="text-xs font-bold text-slate-900">Flood</p>
                            <p className="text-[10px] text-slate-500">XGBoost ML Classifier</p>
                          </div>
                        </div>
                        <div className="text-right">
                          {selectedDetails.riskAssessment.flood?.probability !== null && selectedDetails.riskAssessment.flood?.probability !== undefined && selectedDetails.riskAssessment.flood?.status !== 'UNAVAILABLE' ? (
                            <>
                              <span className="text-xs font-bold text-slate-900">
                                {(selectedDetails.riskAssessment.flood.probability * 100).toFixed(1)}%
                              </span>
                              <span className={`block text-[9px] font-bold px-1.5 py-0.2 rounded-full ${
                                selectedDetails.riskAssessment.flood.risk_level === 'HIGH' ? 'bg-rose-100 text-rose-700' :
                                selectedDetails.riskAssessment.flood.risk_level === 'MEDIUM' ? 'bg-amber-100 text-amber-700' :
                                'bg-emerald-100 text-emerald-700'
                              }`}>
                                {selectedDetails.riskAssessment.flood.risk_level}
                              </span>
                            </>
                          ) : (
                            <>
                              <span className="text-xs font-bold text-slate-500">—</span>
                              <span className="block text-[9px] font-semibold text-slate-500 bg-slate-100 px-1.5 py-0.2 rounded-full">
                                Unavailable — insufficient data
                              </span>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Heatwave Card */}
                      <div className="p-3 bg-white border border-slate-200 rounded-2xl flex items-center justify-between">
                        <div className="flex items-center space-x-2.5">
                          <Flame className="w-5 h-5 text-rose-500" />
                          <div>
                            <p className="text-xs font-bold text-slate-900">Heatwave</p>
                            <p className="text-[10px] text-slate-500">Anomaly Climatology Model</p>
                          </div>
                        </div>
                        <div className="text-right">
                          {selectedDetails.riskAssessment.heatwave?.probability !== null && selectedDetails.riskAssessment.heatwave?.probability !== undefined && selectedDetails.riskAssessment.heatwave?.status !== 'UNAVAILABLE' ? (
                            <>
                              <span className="text-xs font-bold text-slate-900">
                                {(selectedDetails.riskAssessment.heatwave.probability * 100).toFixed(1)}%
                              </span>
                              <span className={`block text-[9px] font-bold px-1.5 py-0.2 rounded-full ${
                                selectedDetails.riskAssessment.heatwave.risk_level === 'HIGH' ? 'bg-rose-100 text-rose-700' :
                                selectedDetails.riskAssessment.heatwave.risk_level === 'MEDIUM' ? 'bg-amber-100 text-amber-700' :
                                'bg-emerald-100 text-emerald-700'
                              }`}>
                                {selectedDetails.riskAssessment.heatwave.risk_level}
                              </span>
                            </>
                          ) : (
                            <>
                              <span className="text-xs font-bold text-slate-500">—</span>
                              <span className="block text-[9px] font-semibold text-slate-500 bg-slate-100 px-1.5 py-0.2 rounded-full">
                                Unavailable — insufficient data
                              </span>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Drought Card (Zero-Tolerance: Unavailable when SPI missing) */}
                      <div className="p-3 bg-white border border-slate-200 rounded-2xl flex items-center justify-between">
                        <div className="flex items-center space-x-2.5">
                          <Droplets className="w-5 h-5 text-amber-500" />
                          <div>
                            <p className="text-xs font-bold text-slate-900">Drought</p>
                            <p className="text-[10px] text-slate-500">SPI_3 / SPI_6 Model</p>
                          </div>
                        </div>
                        <div className="text-right">
                          {selectedDetails.riskAssessment.drought?.status === 'UNAVAILABLE' || selectedDetails.riskAssessment.drought?.probability === null || selectedDetails.riskAssessment.drought?.probability === undefined ? (
                            <>
                              <span className="text-xs font-bold text-slate-500">—</span>
                              <span className="block text-[9px] font-semibold text-slate-500 bg-slate-100 px-1.5 py-0.2 rounded-full" title="Requires antecedent 90-day rainfall observations for SPI calculation">
                                Unavailable — insufficient data
                              </span>
                            </>
                          ) : (
                            <>
                              <span className="text-xs font-bold text-slate-900">
                                {(selectedDetails.riskAssessment.drought.probability * 100).toFixed(1)}%
                              </span>
                              <span className={`block text-[9px] font-bold px-1.5 py-0.2 rounded-full ${
                                selectedDetails.riskAssessment.drought.risk_level === 'HIGH' ? 'bg-rose-100 text-rose-700' :
                                selectedDetails.riskAssessment.drought.risk_level === 'MEDIUM' ? 'bg-amber-100 text-amber-700' :
                                'bg-emerald-100 text-emerald-700'
                              }`}>
                                {selectedDetails.riskAssessment.drought.risk_level}
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* 3. Vulnerability Context */}
                {selectedDetails?.demographicExposure && (
                  <div className="p-3 bg-slate-50 border border-slate-200/80 rounded-2xl text-[11px] space-y-1 text-slate-600">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                      Demographic & Spatial Exposure
                    </span>
                    <div className="flex justify-between">
                      <span>Population:</span>
                      <strong className="text-slate-800">{selectedDetails.demographicExposure.population?.toLocaleString()}</strong>
                    </div>
                    <div className="flex justify-between">
                      <span>Zone Type:</span>
                      <strong className="text-slate-800">{selectedDetails.demographicExposure.coastal ? 'Coastal Maritime' : 'Inland'}</strong>
                    </div>
                    <div className="flex justify-between">
                      <span>Urbanization:</span>
                      <strong className="text-slate-800">{selectedDetails.demographicExposure.urban_percentage}%</strong>
                    </div>
                  </div>
                )}

                {/* 4. Data Status & Model Lineage */}
                <div className="p-3 bg-slate-50 border border-slate-200/80 rounded-2xl text-[11px] space-y-1 text-slate-600">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    Data Status & Model Lineage
                  </span>
                  <div className="flex justify-between">
                    <span>Model Status:</span>
                    <strong className="text-slate-800">Verified XGBoost (53 features)</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Data Source:</span>
                    <strong className="text-slate-800">Open-Meteo & NASA POWER</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Coordinates:</span>
                    <strong className="text-slate-800 font-mono">{selectedPoint.lat.toFixed(4)}°N, {selectedPoint.lon.toFixed(4)}°E</strong>
                  </div>
                </div>

                {/* 5. Adaptation Decision Support */}
                <div className="p-3 bg-blue-50/60 border border-blue-100 rounded-2xl text-[11px] space-y-1">
                  <span className="text-[10px] font-bold text-blue-500 uppercase tracking-wider block">
                    ADAPTATION DECISION SUPPORT
                  </span>
                  <p className="text-slate-600 italic">
                    Available after adaptation module is implemented.
                  </p>
                </div>
              </>
            )}
          </div>

          {/* Panel Footer */}
          <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
            <span className="flex items-center space-x-1">
              <Clock className="w-3 h-3" />
              <span>Forecast: {selectedDetails?.timestamp || 'Live'}</span>
            </span>
            <span>NASA POWER / Open-Meteo</span>
          </div>
        </div>
      )}
    </div>
  );
}
