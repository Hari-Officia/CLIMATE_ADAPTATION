import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DistrictSearchSelector from '../components/DistrictSearchSelector';
import {
  Sun,
  Cloud,
  CloudRain,
  Wind,
  Droplets,
  Gauge,
  Thermometer,
  Compass,
  ArrowUpRight,
  ChevronRight,
  ShieldAlert,
  Search,
  MapPin,
  RefreshCw
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const API_BASE = 'http://localhost:8000';

const DEFAULT_DISTRICTS = [
  { id: 'chennai', name: 'Chennai' },
  { id: 'coimbatore', name: 'Coimbatore' },
  { id: 'madurai', name: 'Madurai' },
  { id: 'nilgiris', name: 'Nilgiris (Ooty)' },
  { id: 'kanniyakumari', name: 'Kanniyakumari' },
  { id: 'thanjavur', name: 'Thanjavur' }
];

export default function Weather() {
  const [districtId, setDistrictId] = useState('chennai');
  const [districtName, setDistrictName] = useState('Chennai');
  const [forecast, setForecast] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [districtsList, setDistrictsList] = useState(DEFAULT_DISTRICTS);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API_BASE}/districts`)
      .then(res => {
        if (res.data && res.data.length > 0) setDistrictsList(res.data);
      })
      .catch(err => console.error(err));
  }, []);

  const loadWeatherData = async (id) => {
    setLoading(true);
    try {
      const [forecastRes, riskRes] = await Promise.all([
        axios.get(`${API_BASE}/forecast/${id}`),
        axios.get(`${API_BASE}/risk/district/${id}?day=0`)
      ]);
      setForecast(forecastRes.data);
      setRiskData(riskRes.data);
      setDistrictName(forecastRes.data.district_name || id);
    } catch (err) {
      console.error('Error fetching weather:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWeatherData(districtId);
  }, [districtId]);

  const current = forecast?.current;
  const hourly = Array.isArray(forecast?.hourly) ? forecast.hourly : [];
  const daily = Array.isArray(forecast?.daily) ? forecast.daily : [];

  const isRainy = (current?.precipitation_mm || 0) > 0 || ((current?.weather_code || 0) >= 51);

  return (
    <div className="min-h-screen relative p-6 lg:p-8 space-y-6 max-w-7xl mx-auto overflow-hidden font-sans">
      {/* Ambient Atmospheric Glow */}
      <div className="absolute top-0 right-1/4 w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

      {/* Header & Quick Selector */}
      <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-xs text-cyan-400 font-semibold uppercase tracking-wider mb-1">
            <span>Atmospheric Observation & NWP Horizon</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight flex items-center space-x-2">
            <span>Weather Intelligence</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time WMO-compliant observations and 7-day numerical weather predictions
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <DistrictSearchSelector
            selectedDistrictId={districtId}
            onSelectDistrict={(newId) => setDistrictId(newId)}
            className="min-w-[220px]"
          />
        </div>
      </div>

      {loading ? (
        <div className="py-24 flex flex-col items-center justify-center space-y-4 relative z-10">
          <div className="w-10 h-10 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-slate-400">Harvesting Open-Meteo NWP Forecast...</p>
        </div>
      ) : (
        <div className="relative z-10 space-y-6">
          {/* Hero Weather Display */}
          <div className="glass-card p-8 text-center relative overflow-hidden border-slate-800/80 bg-gradient-to-b from-slate-900/80 to-slate-950/90 shadow-2xl">
            <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-slate-800/80 text-cyan-400 text-xs font-semibold mb-3 border border-slate-700/60">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
              <span className="capitalize">{districtName}, Tamil Nadu</span>
            </div>

            <h2 className="text-6xl lg:text-7xl font-extrabold text-white tracking-tighter">
              {current?.temperature_c ?? 32}°
            </h2>

            <p className="text-lg text-slate-200 font-medium mt-2">
              {current?.condition || 'Clear Sky'}
            </p>

            <div className="flex items-center justify-center space-x-4 mt-2 text-sm text-slate-400 font-medium">
              <span>H: {current?.high_c ?? 34}°</span>
              <span>•</span>
              <span>L: {current?.low_c ?? 24}°</span>
              <span>•</span>
              <span>Wind: {current?.wind_speed_ms ?? 3.5} m/s</span>
            </div>

            {/* Compact Link to Risk Map */}
            <div className="mt-6 pt-5 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between gap-3 text-left">
              <div className="flex items-center space-x-2.5">
                <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                  <span className="font-bold text-xs">AI</span>
                </div>
                <div>
                  <p className="text-xs font-semibold text-white">
                    Assessed Climate Hazard: <span className="text-cyan-400">{riskData?.assessment?.overall_hazard_level || 'LOW'}</span>
                  </p>
                  <p className="text-[11px] text-slate-400">
                    District-level XGBoost multi-hazard ensemble active
                  </p>
                </div>
              </div>

              <button
                onClick={() => navigate('/risk-map')}
                className="px-3.5 py-1.5 rounded-lg bg-cyan-500/15 hover:bg-cyan-500/25 border border-cyan-500/30 text-cyan-300 text-xs font-semibold flex items-center space-x-1.5 transition cursor-pointer"
              >
                <span>View GIS Risk Map</span>
                <span className="text-xs">→</span>
              </button>
            </div>
          </div>

          {/* 24-Hour Hourly Forecast Slider */}
          {hourly.length > 0 && (
            <div className="glass-card p-6 border-slate-800">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center space-x-2">
                <span>24-Hour Hourly Outlook</span>
              </h3>

              <div className="flex space-x-3 overflow-x-auto pb-2 scrollbar-thin">
                {hourly.map((h, i) => {
                  const hour = h.time ? (h.time.split('T')[1] || h.time) : `+${i}h`;
                  return (
                    <div
                      key={i}
                      className="flex-shrink-0 w-20 p-3 rounded-xl bg-slate-900/60 border border-slate-800/80 text-center flex flex-col items-center justify-between space-y-2 hover:bg-slate-800/60 transition"
                    >
                      <span className="text-[11px] font-medium text-slate-400">{hour}</span>
                      <div className="w-6 h-6 flex items-center justify-center text-cyan-400">
                        {h.precipitation_mm > 0 ? '🌧️' : '☀️'}
                      </div>
                      <span className="text-sm font-bold text-white">{h.temperature_c}°</span>
                      <span className="text-[10px] text-slate-400 font-semibold">
                        {h.precipitation_mm > 0 ? `${h.precipitation_mm}mm` : `${h.humidity_pct}%`}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* 7-Day Forecast Grid & Atmospheric Metric Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 7-Day Forecast with Range Bars */}
            {daily.length > 0 && (
              <div className="glass-card p-6 border-slate-800 flex flex-col justify-between">
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">
                  7-Day Weather Projection
                </h3>

                <div className="space-y-3">
                  {daily.map((d, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between text-xs py-2 border-b border-slate-800/60 last:border-0"
                    >
                      <span className="w-24 font-semibold text-slate-300">
                        {idx === 0 ? 'Today' : d.date}
                      </span>

                      <div className="flex items-center space-x-2 w-32">
                        <span className="text-slate-400 text-[11px] truncate">{d.condition}</span>
                      </div>

                      <div className="flex items-center space-x-3 flex-1 justify-end">
                        <span className="text-slate-400 font-medium w-8 text-right">{d.temp_min_c}°</span>
                        <div className="w-24 bg-slate-800 h-2 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-cyan-500 to-amber-500 rounded-full"
                            style={{
                              width: `${Math.min(100, Math.max(20, (d.temp_max_c - 15) * 4))}%`
                            }}
                          ></div>
                        </div>
                        <span className="text-white font-bold w-8 text-right">{d.temp_max_c}°</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Atmospheric Metrics Grid */}
            <div className="grid grid-cols-2 gap-4">
              <div className="glass-card p-5 border-slate-800 flex flex-col justify-between">
                <span className="text-slate-400 text-xs font-semibold">Relative Humidity</span>
                <div className="my-2">
                  <span className="text-2xl font-extrabold text-white">
                    {current?.humidity_pct ?? 65}%
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Relative humidity at 2 meters altitude
                </p>
              </div>

              <div className="glass-card p-5 border-slate-800 flex flex-col justify-between">
                <span className="text-slate-400 text-xs font-semibold">Wind Speed</span>
                <div className="my-2">
                  <span className="text-2xl font-extrabold text-white">
                    {current?.wind_speed_ms ?? 3.5} <span className="text-xs font-normal">m/s</span>
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Surface horizontal wind velocity
                </p>
              </div>

              <div className="glass-card p-5 border-slate-800 flex flex-col justify-between">
                <span className="text-slate-400 text-xs font-semibold">Surface Pressure</span>
                <div className="my-2">
                  <span className="text-2xl font-extrabold text-white">
                    {current?.pressure_hpa ?? 1012} <span className="text-xs font-normal">hPa</span>
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Mean atmospheric surface barometric pressure
                </p>
              </div>

              <div className="glass-card p-5 border-slate-800 flex flex-col justify-between">
                <span className="text-slate-400 text-xs font-semibold">Rainfall Rate</span>
                <div className="my-2">
                  <span className="text-2xl font-extrabold text-white">
                    {current?.precipitation_mm ?? 0.0} <span className="text-xs font-normal">mm</span>
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Hourly precipitation accumulation
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
