import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  AlertTriangle,
  CloudRain,
  Flame,
  Droplets,
  Wind,
  TrendingUp,
  MapPin,
  Users,
  Building2,
  Anchor,
  Layers,
  ChevronRight,
  RefreshCw,
  Info,
  Shield,
  Zap,
  Activity,
  Compass,
  CheckCircle,
  HelpCircle,
  X
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';

const API_BASE = 'http://localhost:8000';

const NOTABLE_DISTRICTS = [
  { id: 'chennai', name: 'Chennai' },
  { id: 'coimbatore', name: 'Coimbatore' },
  { id: 'madurai', name: 'Madurai' },
  { id: 'tiruchirappalli', name: 'Tiruchirappalli' },
  { id: 'salem', name: 'Salem' },
  { id: 'nilgiris', name: 'Nilgiris' },
  { id: 'thanjavur', name: 'Thanjavur' },
  { id: 'kanniyakumari', name: 'Kanniyakumari' },
  { id: 'cuddalore', name: 'Cuddalore' }
];

export default function Dashboard() {
  const [selectedDistrict, setSelectedDistrict] = useState('chennai');
  const [districtsList, setDistrictsList] = useState(NOTABLE_DISTRICTS);
  const [multiHazardData, setMultiHazardData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [timelineData, setTimelineData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeDetailsModal, setActiveDetailsModal] = useState(null);

  useEffect(() => {
    // Fetch full district list
    axios.get(`${API_BASE}/districts`)
      .then(res => {
        if (res.data && res.data.length > 0) {
          setDistrictsList(res.data);
        }
      })
      .catch(err => console.error('Failed to load districts list:', err));
  }, []);

  const loadDistrictIntelligence = async (districtId) => {
    setLoading(true);
    try {
      const [hazardRes, forecastRes, timelineRes] = await Promise.all([
        axios.get(`${API_BASE}/risk/${districtId}/hazards?day=0`),
        axios.get(`${API_BASE}/forecast/${districtId}`),
        axios.get(`${API_BASE}/risk/timeline/${districtId}`).catch(() => ({ data: null }))
      ]);

      setMultiHazardData(hazardRes.data);
      setForecastData(forecastRes.data);

      if (timelineRes?.data?.timeline) {
        const formatted = timelineRes.data.timeline.map((d, idx) => ({
          day: `Day ${idx === 0 ? 'Today' : idx}`,
          date: d.date,
          Flood: Math.round((d.flood?.probability || 0) * 100),
          Heatwave: Math.round((d.heatwave?.probability || 0) * 100),
          Drought: d.drought?.probability !== null ? Math.round(d.drought.probability * 100) : 0
        }));
        setTimelineData(formatted);
      }
    } catch (err) {
      console.error('Error fetching district intelligence:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadDistrictIntelligence(selectedDistrict);
  }, [selectedDistrict]);

  const handleRefresh = () => {
    setRefreshing(true);
    loadDistrictIntelligence(selectedDistrict);
  };

  const getHazardIcon = (id) => {
    switch (id) {
      case 'flood':
      case 'extreme_rainfall':
        return <CloudRain className="w-5 h-5 text-blue-400" />;
      case 'heatwave':
      case 'heat_stress':
        return <Flame className="w-5 h-5 text-rose-400" />;
      case 'drought':
        return <Droplets className="w-5 h-5 text-amber-400" />;
      case 'extreme_wind':
        return <Wind className="w-5 h-5 text-cyan-400" />;
      case 'thunderstorm':
        return <Zap className="w-5 h-5 text-purple-400" />;
      case 'coastal':
        return <Anchor className="w-5 h-5 text-teal-400" />;
      case 'air_quality':
        return <Activity className="w-5 h-5 text-emerald-400" />;
      case 'cyclone':
        return <Compass className="w-5 h-5 text-indigo-400" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-cyan-400" />;
    }
  };

  const getBadgeStyle = (level, status) => {
    if (status === 'NOT_APPLICABLE') {
      return 'bg-slate-800 text-slate-400 border-slate-700';
    }
    if (status === 'UNAVAILABLE') {
      return 'bg-slate-800/80 text-amber-300 border-amber-500/40';
    }
    switch (level) {
      case 'SEVERE':
        return 'bg-purple-500/20 text-purple-300 border-purple-500/40 animate-pulse';
      case 'HIGH':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'MEDIUM':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default:
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
    }
  };

  const getEngineBadge = (type) => {
    switch (type) {
      case 'ml_probability':
        return { label: 'ML Model', cls: 'bg-cyan-500/10 text-cyan-300 border-cyan-500/30' };
      case 'rule_based':
        return { label: 'Rule-based', cls: 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30' };
      default:
        return { label: 'External API', cls: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30' };
    }
  };

  const hazards = multiHazardData?.hazards || {};
  const currentThreat = multiHazardData?.overall_threat_level || 'LOW';

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Top Header & District Quick Switcher */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-xs text-cyan-400 font-semibold uppercase tracking-wider mb-1">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            <span>Quantum Decision Support Engine • Multi-Hazard Framework</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Executive Climate Risk Dashboard
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time multi-hazard assessment across Machine Learning models, meteorological rules, and sensor networks
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative min-w-[200px]">
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-xs font-semibold focus:outline-none focus:border-cyan-500 appearance-none shadow-lg cursor-pointer"
            >
              {districtsList.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name} {d.coastal ? '🌊 (Coastal)' : ''}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="p-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 transition shadow-lg"
            title="Refresh district intelligence"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {loading ? (
        <div className="py-24 flex flex-col items-center justify-center space-y-4">
          <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs text-slate-400">Evaluating multi-hazard risk engine across models & rules...</p>
        </div>
      ) : (
        <>
          {/* Top Status & Weather Highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Active District Status Card */}
            <div className="glass-card p-5 border-slate-800 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    Selected Administrative Unit
                  </span>
                  <MapPin className="w-4 h-4 text-cyan-400" />
                </div>
                <h2 className="text-xl font-bold text-white mt-1 capitalize">
                  {multiHazardData?.district_name} District
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  {multiHazardData?.demographic_exposure?.coastal ? 'Maritime / Coastal Zone' : 'Inland Agricultural / Urban Zone'}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-xs text-slate-400">Overall Threat Tier:</span>
                <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${getBadgeStyle(currentThreat, 'AVAILABLE')}`}>
                  {currentThreat} THREAT
                </span>
              </div>
            </div>

            {/* Current Weather Card */}
            <div className="glass-card p-5 border-slate-800 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    Current Atmospheric State
                  </span>
                  <CloudRain className="w-4 h-4 text-blue-400" />
                </div>
                <div className="flex items-baseline space-x-3 mt-1">
                  <span className="text-3xl font-extrabold text-white">
                    {forecastData?.current?.temperature_c || 30.0}°C
                  </span>
                  <span className="text-xs text-slate-300 font-medium">
                    {forecastData?.current?.condition || 'Partly cloudy'}
                  </span>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                <span>Humidity: {forecastData?.current?.humidity_pct}%</span>
                <span>Wind: {forecastData?.current?.wind_speed_ms} m/s</span>
                <span>High: {forecastData?.current?.high_c}°C</span>
              </div>
            </div>

            {/* Demographic Exposure Context */}
            <div className="glass-card p-5 border-slate-800 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    Vulnerability Context
                  </span>
                  <Users className="w-4 h-4 text-purple-400" />
                </div>
                <div className="mt-1">
                  <span className="text-xl font-bold text-white">
                    {multiHazardData?.demographic_exposure?.population?.toLocaleString() || '1,200,000'}
                  </span>
                  <span className="text-xs text-slate-400 ml-1.5">Residents</span>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                <span>Urban: {multiHazardData?.demographic_exposure?.urban_percentage}%</span>
                <span>Elevation: {multiHazardData?.demographic_exposure?.elevation_m}m</span>
                <span>{multiHazardData?.demographic_exposure?.coastal ? 'Coastal Zone' : 'Inland'}</span>
              </div>
            </div>
          </div>

          {/* Dynamic Multi-Hazard Risk Grid */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                <Shield className="w-4 h-4 text-cyan-400" />
                <span>Multi-Hazard Risk Portfolio (10 Registered Hazards)</span>
              </h3>
              <span className="text-[11px] text-slate-400">
                Differentiates ML probabilities, physical rules, and sensor feeds
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
              {Object.entries(hazards).map(([id, h]) => {
                const engine = getEngineBadge(h.engine_type);
                const isUnavailable = h.status === 'UNAVAILABLE';
                const isNotApplicable = h.status === 'NOT_APPLICABLE';

                return (
                  <div
                    key={id}
                    className={`glass-card p-4 border-slate-800 flex flex-col justify-between relative transition hover:border-slate-700 ${
                      isNotApplicable ? 'opacity-60 bg-slate-950/40' : ''
                    }`}
                  >
                    <div>
                      {/* Card Header: Icon + Name + Engine Badge */}
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-center space-x-2">
                          <div className="p-1.5 rounded-lg bg-slate-900 border border-slate-800">
                            {getHazardIcon(id)}
                          </div>
                          <div>
                            <h4 className="text-xs font-bold text-white leading-tight">
                              {h.hazard_name}
                            </h4>
                            <span className={`inline-block text-[9px] font-semibold px-1.5 py-0.2 rounded border mt-0.5 ${engine.cls}`}>
                              {engine.label}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Display Value & Risk Badge */}
                      <div className="mt-3">
                        <div className="flex items-baseline justify-between">
                          <span className={`text-base font-extrabold tracking-tight ${
                            isUnavailable ? 'text-amber-400 font-mono' : isNotApplicable ? 'text-slate-400' : 'text-white'
                          }`}>
                            {h.display_value}
                          </span>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getBadgeStyle(h.risk_level, h.status)}`}>
                            {isUnavailable ? 'DATA UNAVAILABLE' : isNotApplicable ? 'NOT APPLICABLE' : h.risk_level}
                          </span>
                        </div>

                        {/* ML Probability Bar (Only rendered for valid ML models) */}
                        {h.engine_type === 'ml_probability' && !isUnavailable && (
                          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mt-2">
                            <div
                              className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all duration-500"
                              style={{ width: `${Math.min(100, Math.max(3, (h.probability || 0) * 100))}%` }}
                            ></div>
                          </div>
                        )}
                      </div>

                      {/* Scientific Note / Reason */}
                      <p className="text-[10px] text-slate-400 mt-2 line-clamp-2">
                        {isUnavailable ? h.reason : isNotApplicable ? h.reason : h.confidence_note || h.explanation}
                      </p>
                    </div>

                    {/* Footer / Expandable Details Button */}
                    <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[10px]">
                      <span className="text-slate-400 truncate max-w-[100px]">{h.source?.split(' ')[0]}</span>
                      <button
                        onClick={() => setActiveDetailsModal(h)}
                        className="text-cyan-400 hover:text-cyan-300 font-semibold flex items-center space-x-1"
                      >
                        <span>Why?</span>
                        <ChevronRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 7-Day ML Risk Trend Trajectory Chart */}
          {timelineData.length > 0 && (
            <div className="glass-card p-6 border-slate-800">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                    <TrendingUp className="w-4 h-4 text-cyan-400" />
                    <span>7-Day Multi-Hazard Probability Trajectory (ML Ensemble)</span>
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Continuous multi-day forecast risk tracking across Flood and Heatwave models
                  </p>
                </div>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={timelineData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="floodGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#38bdf8" stopOpacity={0.0} />
                      </linearGradient>
                      <linearGradient id="heatGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} unit="%" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '11px' }}
                      formatter={(val) => [`${val}%`, '']}
                    />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                    <Area type="monotone" dataKey="Flood" stroke="#38bdf8" fill="url(#floodGrad)" strokeWidth={2} />
                    <Area type="monotone" dataKey="Heatwave" stroke="#f43f5e" fill="url(#heatGrad)" strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Details Modal ("Why?") */}
          {activeDetailsModal && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 animate-in fade-in duration-200">
              <div className="glass-card max-w-lg w-full p-6 border-slate-700 shadow-2xl space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center space-x-2.5">
                    {getHazardIcon(activeDetailsModal.hazard_id)}
                    <div>
                      <h3 className="text-base font-bold text-white">{activeDetailsModal.hazard_name}</h3>
                      <span className="text-[10px] text-cyan-400 font-semibold">{activeDetailsModal.engine_type}</span>
                    </div>
                  </div>
                  <button
                    onClick={() => setActiveDetailsModal(null)}
                    className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <div className="space-y-3 text-xs">
                  <div>
                    <span className="text-slate-400 text-[11px] font-semibold block">Calculation Method</span>
                    <p className="text-white mt-0.5 font-medium">{activeDetailsModal.method}</p>
                  </div>

                  <div>
                    <span className="text-slate-400 text-[11px] font-semibold block">Scientific Explanation</span>
                    <p className="text-slate-300 mt-0.5 leading-relaxed">{activeDetailsModal.explanation}</p>
                  </div>

                  <div>
                    <span className="text-slate-400 text-[11px] font-semibold block">Data Source</span>
                    <p className="text-slate-300 mt-0.5">{activeDetailsModal.source}</p>
                  </div>

                  {activeDetailsModal.details && Object.keys(activeDetailsModal.details).length > 0 && (
                    <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1 font-mono text-[11px]">
                      <span className="text-slate-400 text-[10px] font-sans font-bold uppercase tracking-wider block mb-1">
                        Engine Input Parameters
                      </span>
                      {Object.entries(activeDetailsModal.details)
                        .filter(([k]) => k !== 'diagnostics')
                        .map(([k, v]) => (
                          <div key={k} className="flex justify-between">
                            <span className="text-slate-400">{k}:</span>
                            <span className="text-white font-semibold">{typeof v === 'number' ? v.toFixed(2) : String(v)}</span>
                          </div>
                        ))}
                    </div>
                  )}
                </div>

                <div className="pt-3 border-t border-slate-800 flex justify-end">
                  <button
                    onClick={() => setActiveDetailsModal(null)}
                    className="px-4 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold transition"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
