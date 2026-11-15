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
  ExternalLink,
  Cpu,
  GitCompare,
  Filter,
  Award,
  CheckCircle2,
  TrendingUp,
  BarChart3
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
        <path d="M12 0C5.37 0 0 5.37 0 12C0 21 12 34 12 34C12 34 24 21 24 12C24 5.37 18.63 0 12 0Z" fill="#2563EB" stroke="#FFFFFF" stroke-width="1.5"/>
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
      map.flyTo(center, zoom || 8, { duration: 1.2 });
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

const ALL_DOMAINS = [
  'Flood & Stormwater',
  'Heat & Urban Cooling',
  'Agriculture & Drought',
  'Water Security',
  'Coastal Adaptation',
  'Ecosystem & Nature-Based',
  'Buildings & Infrastructure',
  'Health & Preparedness'
];

const cleanStrategyName = (sId, name) => {
  if (sId === 'STR-EWS-002' && name && name.includes('Coastal')) {
    return 'Cyclone Telemetry & Multi-Hazard Mobile Sirens';
  }
  return name;
};

export default function RiskMap() {
  const [hazard, setHazard] = useState('overall'); // 'flood' | 'heatwave' | 'drought' | 'overall'
  const [decisionLayer, setDecisionLayer] = useState('milp'); // 'risk' | 'milp' | 'qaoa' | 'compare'
  const [selectedDomains, setSelectedDomains] = useState(ALL_DOMAINS);
  
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [loadingOverlay, setLoadingOverlay] = useState(true);

  // Selected District / Location Data
  const [selectedDistrictId, setSelectedDistrictId] = useState('chennai');
  const [districtDetail, setDistrictDetail] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  
  const [mapCenter, setMapCenter] = useState([11.1271, 78.6569]); // Center of Tamil Nadu
  const [mapZoom, setMapZoom] = useState(7);

  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showSearchDropdown, setShowSearchDropdown] = useState(false);

  // Layer control state
  const [showBoundaries, setShowBoundaries] = useState(true);
  const [activeBasemap, setActiveBasemap] = useState('road'); // 'road' | 'light' | 'dark'

  // Load Phase 7 Enriched GeoJSON Overlay from API
  const loadPhase7Overlay = async () => {
    setLoadingOverlay(true);
    try {
      const resp = await axios.get(`${API_BASE}/gis/adaptation-overlay`);
      setGeoJsonData(resp.data);
    } catch (err) {
      console.error('Failed to load Phase 7 adaptation overlay GeoJSON:', err);
    } finally {
      setLoadingOverlay(false);
    }
  };

  useEffect(() => {
    loadPhase7Overlay();
  }, []);

  // Fetch detailed district portfolio & comparison when district is selected
  const fetchDistrictDetails = async (dId) => {
    setDetailsLoading(true);
    try {
      const [detailRes, portfolioRes, comparisonRes] = await Promise.all([
        axios.get(`${API_BASE}/gis/districts/${dId}`),
        axios.get(`${API_BASE}/gis/portfolio/${dId}`),
        axios.get(`${API_BASE}/gis/comparison/${dId}`)
      ]);
      
      setDistrictDetail({
        gis: detailRes.data,
        portfolio: portfolioRes.data,
        comparison: comparisonRes.data
      });
    } catch (err) {
      console.error(`Failed to fetch details for district ${dId}:`, err);
    } finally {
      setDetailsLoading(false);
    }
  };

  useEffect(() => {
    if (selectedDistrictId) {
      fetchDistrictDetails(selectedDistrictId);
    }
  }, [selectedDistrictId]);

  // Debounced place search
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      setShowSearchDropdown(false);
      return;
    }

    const timer = setTimeout(async () => {
      try {
        const resp = await axios.get(`${API_BASE}/locations/search?q=${encodeURIComponent(searchQuery)}`);
        setSearchResults(resp.data || []);
        setShowSearchDropdown(true);
      } catch (err) {
        console.error('Location search failed:', err);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const handleSelectDistrict = (dId, lat, lon) => {
    setSelectedDistrictId(dId);
    if (lat && lon) {
      setMapCenter([lat, lon]);
      setMapZoom(9);
    }
  };

  // Dynamic GeoJSON Feature Styling based on Decision Layer & Filters
  const getFeatureStyle = (feature) => {
    const props = feature.properties || {};
    let fillColor = '#64748b';
    let fillOpacity = 0.55;

    if (decisionLayer === 'risk') {
      const riskVal = hazard === 'flood' ? props.risk_flood :
                      hazard === 'drought' ? props.risk_drought :
                      hazard === 'heatwave' ? props.risk_heatwave :
                      props.risk_overall || props.overall_risk;
      
      if (riskVal === 'HIGH' || riskVal === 'SEVERE') fillColor = '#ef4444';
      else if (riskVal === 'MEDIUM') fillColor = '#f59e0b';
      else if (riskVal === 'LOW') fillColor = '#10b981';
      else fillColor = '#94a3b8';

    } else if (decisionLayer === 'milp') {
      // Color by MILP Selected Strategy Count
      const count = props.milp_selected_count || 0;
      if (count >= 5) fillColor = '#1d4ed8'; // Dark blue
      else if (count >= 4) fillColor = '#2563eb'; // Medium blue
      else if (count >= 3) fillColor = '#3b82f6'; // Light blue
      else fillColor = '#93c5fd';

    } else if (decisionLayer === 'qaoa') {
      // Color by QAOA Approximation Ratio
      const approx = props.qaoa_approximation_ratio || 0.99;
      if (approx >= 0.995) fillColor = '#6d28d9'; // Deep Quantum Purple
      else if (approx >= 0.99) fillColor = '#7c3aed';
      else if (approx >= 0.98) fillColor = '#8b5cf6';
      else fillColor = '#c4b5fd';

    } else if (decisionLayer === 'compare') {
      // Color by Portfolio Match Ratio
      const match = props.portfolio_match_ratio || 0;
      if (match >= 0.8) fillColor = '#059669'; // Emerald match
      else if (match >= 0.6) fillColor = '#d97706'; // Amber partial match
      else fillColor = '#dc2626'; // Red low match
    }

    const isSelected = props.district_id === selectedDistrictId;

    return {
      fillColor,
      weight: isSelected ? 3 : (showBoundaries ? 1.5 : 0.5),
      opacity: isSelected ? 1.0 : 0.8,
      color: isSelected ? '#000000' : '#334155',
      dashArray: isSelected ? '' : '',
      fillOpacity: isSelected ? 0.75 : fillOpacity
    };
  };

  const onEachFeature = (feature, layer) => {
    const props = feature.properties || {};
    const name = props.district_name || 'District';
    const milpCount = props.milp_selected_count || 0;
    const qaoaCount = props.qaoa_selected_count || 0;
    const approxRatio = (props.qaoa_approximation_ratio ? (props.qaoa_approximation_ratio * 100).toFixed(2) : '99.50');
    const matchRatio = (props.portfolio_match_ratio ? (props.portfolio_match_ratio * 100).toFixed(0) : '60');

    layer.bindTooltip(`
      <div style="font-family: system-ui, sans-serif; padding: 4px;">
        <strong style="color: #0f172a; font-size: 13px;">${name}</strong><br/>
        <span style="font-size: 11px; color: #475569;">MILP Portfolio: <b>${milpCount} strategies</b></span><br/>
        <span style="font-size: 11px; color: #6b21a8;">QAOA Portfolio: <b>${qaoaCount} strategies</b> (${approxRatio}%)</span><br/>
        <span style="font-size: 11px; color: #047857;">Portfolio Overlap: <b>${matchRatio}%</b></span>
      </div>
    `, { sticky: true });

    layer.on({
      mouseover: (e) => {
        const l = e.target;
        l.setStyle({ weight: 3, color: '#2563eb', fillOpacity: 0.85 });
        l.bringToFront();
      },
      mouseout: (e) => {
        const l = e.target;
        l.setStyle(getFeatureStyle(feature));
      },
      click: (e) => {
        handleSelectDistrict(props.district_id, e.latlng.lat, e.latlng.lng);
      }
    });
  };

  const basemapTiles = {
    road: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    light: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
  };

  const toggleDomain = (domain) => {
    if (selectedDomains.includes(domain)) {
      setSelectedDomains(selectedDomains.filter(d => d !== domain));
    } else {
      setSelectedDomains([...selectedDomains, domain]);
    }
  };

  return (
    <div className="relative w-full h-[calc(100vh)] flex flex-col bg-slate-100 overflow-hidden font-sans">
      
      {/* LEFT CONTROL SIDEBAR */}
      <div className="absolute top-4 left-4 z-[1000] w-72 bg-white/95 backdrop-blur-md border border-slate-200 shadow-2xl rounded-3xl p-4 text-xs space-y-4 max-h-[calc(100vh-32px)] overflow-y-auto">
        <div>
          <h2 className="text-sm font-extrabold text-slate-900 tracking-tight flex items-center gap-1.5">
            <Compass className="w-4 h-4 text-blue-600" />
            Q-MADSS Spatial GIS Map
          </h2>
          <p className="text-[11px] text-slate-500">Tamil Nadu Adaptation Strategy Overlay</p>
        </div>

        {/* Search Input */}
        <div className="relative">
          <div className="flex items-center px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
            <Search className="w-4 h-4 text-slate-400 mr-2 flex-shrink-0" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search district..."
              className="w-full text-xs text-slate-800 placeholder-slate-400 bg-transparent focus:outline-none"
            />
          </div>

          {showSearchDropdown && searchResults.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-xl shadow-xl z-[1010] max-h-48 overflow-y-auto">
              {searchResults.map((item, i) => (
                <div
                  key={i}
                  onClick={() => {
                    setSearchQuery(item.name);
                    setShowSearchDropdown(false);
                    handleSelectDistrict(item.district_id, item.latitude, item.longitude);
                  }}
                  className="px-3 py-2 hover:bg-blue-50 cursor-pointer border-b border-slate-100 text-xs flex justify-between"
                >
                  <span className="font-semibold text-slate-800">{item.name}</span>
                  <span className="text-[10px] text-slate-500">{item.district_name}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Decision Layer Selector */}
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Decision Intelligence Layer
          </label>
          <div className="grid grid-cols-1 gap-1">
            {[
              { id: 'milp', label: 'MILP Ground Truth', icon: Shield, color: 'text-blue-600 bg-blue-50 border-blue-200' },
              { id: 'qaoa', label: 'QAOA Approximate Solution', icon: Cpu, color: 'text-purple-600 bg-purple-50 border-purple-200' },
              { id: 'compare', label: 'MILP vs QAOA Compare', icon: GitCompare, color: 'text-emerald-600 bg-emerald-50 border-emerald-200' },
              { id: 'risk', label: 'Climate Hazard Risk', icon: Flame, color: 'text-amber-600 bg-amber-50 border-amber-200' }
            ].map(layer => {
              const Icon = layer.icon;
              const isActive = decisionLayer === layer.id;
              return (
                <button
                  key={layer.id}
                  onClick={() => setDecisionLayer(layer.id)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-xl border text-xs font-semibold transition ${
                    isActive ? `${layer.color} shadow-sm border-2` : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Icon className="w-4 h-4" />
                    <span>{layer.label}</span>
                  </div>
                  {isActive && <CheckCircle2 className="w-3.5 h-3.5" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* Hazard Selector (When Risk layer active) */}
        {decisionLayer === 'risk' && (
          <div className="space-y-1.5 pt-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Climate Hazard Filter
            </label>
            <div className="grid grid-cols-2 gap-1">
              {[
                { id: 'overall', label: 'Overall Risk' },
                { id: 'flood', label: 'Flood Risk' },
                { id: 'drought', label: 'Drought Risk' },
                { id: 'heatwave', label: 'Heatwave Risk' }
              ].map(h => (
                <button
                  key={h.id}
                  onClick={() => setHazard(h.id)}
                  className={`px-2.5 py-1.5 rounded-lg text-[11px] font-semibold transition ${
                    hazard === h.id ? 'bg-amber-600 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {h.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Strategy Domain Filters */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Strategy Domains ({selectedDomains.length}/{ALL_DOMAINS.length})
            </label>
            <button
              onClick={() => setSelectedDomains(selectedDomains.length === ALL_DOMAINS.length ? [] : ALL_DOMAINS)}
              className="text-[10px] font-semibold text-blue-600 hover:underline"
            >
              {selectedDomains.length === ALL_DOMAINS.length ? 'Clear All' : 'Select All'}
            </button>
          </div>
          <div className="space-y-1 max-h-36 overflow-y-auto pr-1">
            {ALL_DOMAINS.map(domain => (
              <label key={domain} className="flex items-center space-x-2 text-[11px] text-slate-700 cursor-pointer hover:bg-slate-50 p-1 rounded-lg">
                <input
                  type="checkbox"
                  checked={selectedDomains.includes(domain)}
                  onChange={() => toggleDomain(domain)}
                  className="rounded text-blue-600 focus:ring-0 w-3.5 h-3.5"
                />
                <span className="truncate">{domain}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Legend Box */}
        <div className="p-3 bg-slate-50 border border-slate-200 rounded-2xl space-y-1.5">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Map Legend ({
              decisionLayer === 'milp' ? 'MILP Ground Truth' :
              decisionLayer === 'qaoa' ? 'QAOA Approximate Solution' :
              decisionLayer === 'compare' ? 'MILP vs QAOA Compare' : 'Climate Risk'
            })
          </span>
          {decisionLayer === 'milp' && (
            <div className="space-y-1 text-[11px]">
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-blue-700"></span><span>5+ MILP Strategies</span></div>
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-blue-500"></span><span>4 MILP Strategies</span></div>
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-blue-400"></span><span>3 MILP Strategies</span></div>
            </div>
          )}
          {decisionLayer === 'qaoa' && (
            <div className="space-y-1 text-[11px]">
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-purple-700"></span><span>≥ 99.5% QAOA Approx Ratio</span></div>
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-purple-500"></span><span>98.0–99.4% Approx Ratio</span></div>
            </div>
          )}
          {decisionLayer === 'compare' && (
            <div className="space-y-1 text-[11px]">
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-emerald-600"></span><span>≥ 80% Portfolio Overlap</span></div>
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-amber-500"></span><span>60–79% Portfolio Overlap</span></div>
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-rose-600"></span><span>&lt; 60% Portfolio Overlap</span></div>
            </div>
          )}
          {decisionLayer === 'risk' && (
            <div className="space-y-1 text-[11px]">
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-rose-500"></span><span>HIGH Risk</span></div>
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-amber-500"></span><span>MEDIUM Risk</span></div>
              <div className="flex items-center justify-between"><span className="w-3 h-3 rounded bg-emerald-500"></span><span>LOW Risk</span></div>
            </div>
          )}
        </div>
      </div>

      {/* CENTER INTERACTIVE MAP */}
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

          <TileLayer
            url={basemapTiles[activeBasemap]}
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {geoJsonData && (
            <GeoJSON
              key={`${decisionLayer}_${hazard}_${selectedDomains.join('_')}`}
              data={geoJsonData}
              style={getFeatureStyle}
              onEachFeature={onEachFeature}
            />
          )}
        </MapContainer>
      </div>

      {/* RIGHT DISTRICT DETAILS DRAWER */}
      {selectedDistrictId && (
        <div className="absolute top-4 right-4 bottom-4 z-[1000] w-96 bg-white/95 backdrop-blur-md border border-slate-200 shadow-2xl rounded-3xl p-5 overflow-y-auto space-y-4 flex flex-col justify-between">
          <div>
            {/* Header */}
            <div className="flex items-start justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <div className="p-2 rounded-xl bg-blue-50 text-blue-600">
                  <MapPin className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-extrabold text-slate-900 leading-tight capitalize">
                    {districtDetail?.gis?.district_name || selectedDistrictId} District
                  </h3>
                  <p className="text-xs text-slate-500">Spatial Decision Intelligence Model</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedDistrictId(null)}
                className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {detailsLoading ? (
              <div className="py-20 flex flex-col items-center justify-center space-y-3 text-xs text-slate-500">
                <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <span>Loading Spatial Decision Intelligence...</span>
              </div>
            ) : districtDetail ? (
              <div className="space-y-4 pt-2">
                
                {/* QAOA Approximation Summary Badge */}
                <div className="p-3.5 bg-purple-50 border border-purple-200 rounded-2xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-purple-700 uppercase tracking-wider flex items-center gap-1">
                      <Cpu className="w-3.5 h-3.5" />
                      QAOA Quantum Solution Status
                    </span>
                    <span className="text-xs font-extrabold text-purple-800 bg-purple-200/80 px-2 py-0.5 rounded-full">
                      {(districtDetail.portfolio.qaoa.approximation_ratio * 100).toFixed(2)}% Approx Ratio
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs pt-1">
                    <div>MILP Obj: <strong className="text-blue-900">{districtDetail.portfolio.milp.objective_value}</strong></div>
                    <div>QAOA Obj: <strong className="text-purple-900">{districtDetail.portfolio.qaoa.objective_value}</strong></div>
                    <div>Match Ratio: <strong className="text-emerald-700">{(districtDetail.comparison.metrics.portfolio_match_ratio * 100).toFixed(0)}%</strong></div>
                    <div>Status: <strong className="text-purple-700">{districtDetail.portfolio.qaoa.status}</strong></div>
                  </div>
                </div>

                {/* MILP Classical Ground Truth Portfolio */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-blue-900 flex items-center gap-1">
                      <Shield className="w-4 h-4 text-blue-600" />
                      MILP Portfolio ({districtDetail.portfolio.milp.selected_count} Strategies)
                    </span>
                    <span className="text-[10px] text-blue-600 font-semibold">Classical Optimum</span>
                  </div>
                  <div className="space-y-1.5">
                    {districtDetail.portfolio.milp.selected_strategy_names.map((name, idx) => {
                      const sId = districtDetail.portfolio.milp.selected_strategy_ids[idx];
                      const cName = cleanStrategyName(sId, name);
                      return (
                        <div key={idx} className="p-2.5 bg-blue-50/70 border border-blue-100 rounded-xl text-xs flex items-start space-x-2">
                          <CheckCircle className="w-3.5 h-3.5 text-blue-600 flex-shrink-0 mt-0.5" />
                          <div>
                            <p className="font-semibold text-slate-800 leading-tight">{cName}</p>
                            <p className="text-[10px] text-blue-700 font-mono mt-0.5">{sId}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* QAOA Quantum Approximate Portfolio */}
                <div className="space-y-2 pt-2 border-t border-slate-100">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-purple-900 flex items-center gap-1">
                      <Cpu className="w-4 h-4 text-purple-600" />
                      QAOA Quantum Portfolio ({districtDetail.portfolio.qaoa.selected_count} Strategies)
                    </span>
                    <span className="text-[10px] text-purple-600 font-semibold">p=2 Circuit</span>
                  </div>
                  <div className="space-y-1.5">
                    {districtDetail.portfolio.qaoa.selected_strategy_names.map((name, idx) => {
                      const sId = districtDetail.portfolio.qaoa.selected_strategy_ids[idx];
                      const cName = cleanStrategyName(sId, name);
                      const isCommon = districtDetail.comparison.metrics.common_strategies.includes(sId);
                      return (
                        <div key={idx} className={`p-2.5 border rounded-xl text-xs flex items-start space-x-2 ${
                          isCommon ? 'bg-purple-50/70 border-purple-200' : 'bg-amber-50/70 border-amber-200'
                        }`}>
                          {isCommon ? (
                            <CheckCircle2 className="w-3.5 h-3.5 text-purple-600 flex-shrink-0 mt-0.5" />
                          ) : (
                            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 flex-shrink-0 mt-0.5" />
                          )}
                          <div>
                            <p className="font-semibold text-slate-800 leading-tight">{cName}</p>
                            <div className="flex items-center gap-2 mt-0.5">
                              <span className="text-[10px] text-purple-700 font-mono">{sId}</span>
                              <span className={`text-[9px] px-1.5 py-0.2 rounded font-bold ${
                                isCommon ? 'bg-purple-100 text-purple-800' : 'bg-amber-100 text-amber-800'
                              }`}>
                                {isCommon ? 'Matches MILP' : 'QAOA Variant'}
                              </span>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Scientific Positioning Note */}
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-[10px] text-slate-600 space-y-1">
                  <span className="font-bold text-slate-800 uppercase block">Scientific Framing</span>
                  <p>
                    QAOA approximate solution candidate portfolios are benchmarked against exact classical MILP ground truth. MILP provides the certified reference optimum.
                  </p>
                </div>

              </div>
            ) : null}
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
            <span>Q-MADSS Phase 7 Spatial Intelligence</span>
            <span>38 Districts Certified</span>
          </div>
        </div>
      )}
    </div>
  );
}
