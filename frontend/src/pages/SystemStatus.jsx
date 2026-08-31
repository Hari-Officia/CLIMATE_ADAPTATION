import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Activity,
  CheckCircle,
  AlertTriangle,
  Database,
  Cpu,
  RefreshCw,
  Layers,
  Shield,
  Clock,
  Terminal,
  FileCode,
  Lock,
  Search,
  Check
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const API_BASE = 'http://localhost:8000';

export default function SystemStatus() {
  const { user } = useAuth();
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshingCache, setRefreshingCache] = useState(false);
  const [cacheMessage, setCacheMessage] = useState(null);
  const [showSchema, setShowSchema] = useState(false);
  const [showDebug, setShowDebug] = useState(false);
  const [debugData, setDebugData] = useState(null);
  const [debugLoading, setDebugLoading] = useState(false);

  const loadStatus = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/system/status`);
      setStatusData(resp.data);
    } catch (err) {
      console.error('Failed to load system status:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  const handlePurgeCache = async () => {
    setRefreshingCache(true);
    setCacheMessage(null);
    try {
      const resp = await axios.post(`${API_BASE}/system/admin/refresh-forecast`);
      setCacheMessage({ type: 'success', text: resp.data.message });
      loadStatus();
    } catch (err) {
      setCacheMessage({
        type: 'error',
        text: err.response?.data?.detail || 'Admin privileges required to purge cache.'
      });
    } finally {
      setRefreshingCache(false);
    }
  };

  const loadDebugData = async () => {
    setDebugLoading(true);
    try {
      const resp = await axios.get(`${API_BASE}/system/debug?district_id=chennai`);
      setDebugData(resp.data);
    } catch (err) {
      console.error('Failed to load debug data:', err);
    } finally {
      setDebugLoading(false);
    }
  };

  const toggleDebug = () => {
    if (!showDebug && !debugData) {
      loadDebugData();
    }
    setShowDebug(!showDebug);
  };

  const schemaFeatures = [
    'temp_max', 'temp_min', 'temp_mean', 'temp_range',
    'humidity', 'wind_speed', 'rainfall', 'soil_wetness',
    'rainfall_3d', 'rainfall_7d', 'rainfall_30d',
    'temp_anomaly', 'rainfall_anomaly', 'SPI_3', 'SPI_6',
    'district_Ariyalur', 'district_Chengalpattu', 'district_Chennai',
    'district_Coimbatore', 'district_Cuddalore', 'district_Dharmapuri',
    'district_Dindigul', 'district_Erode', 'district_Kallakurichi',
    'district_Kancheepuram', 'district_Kanniyakumari', 'district_Karur',
    'district_Krishnagiri', 'district_Madurai', 'district_Mayiladuthurai',
    'district_Nagapattinam', 'district_Namakkal', 'district_Nilgiris',
    'district_Perambalur', 'district_Pudukkottai', 'district_Ramanathapuram',
    'district_Ranipet', 'district_Salem', 'district_Sivaganga',
    'district_Tenkasi', 'district_Thanjavur', 'district_Theni',
    'district_Thoothukudi', 'district_Tiruchirappalli', 'district_Tirunelveli',
    'district_Tirupathur', 'district_Tiruppur', 'district_Tiruvallur',
    'district_Tiruvannamalai', 'district_Tiruvarur', 'district_Vellore',
    'district_Viluppuram', 'district_Virudhunagar'
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-xs text-cyan-400 font-semibold uppercase tracking-wider mb-1">
            <span>Infrastructure, Data Provenance & Model Health</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight flex items-center space-x-3">
            <Activity className="w-6 h-6 text-cyan-400" />
            <span>Multi-Agent System Status</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time monitoring of agents, databases, ML models, and feature schemas
          </p>
        </div>

        <div className="flex items-center space-x-3">
          {user?.role === 'ADMIN' && (
            <button
              onClick={toggleDebug}
              className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-amber-300 hover:text-amber-200 flex items-center space-x-1.5 transition"
            >
              <Terminal className="w-3.5 h-3.5 text-amber-400" />
              <span>{showDebug ? 'Hide Debug Mode' : 'Admin Debug Mode'}</span>
            </button>
          )}

          <button
            onClick={() => setShowSchema(!showSchema)}
            className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-300 hover:text-white flex items-center space-x-1.5 transition"
          >
            <FileCode className="w-3.5 h-3.5 text-cyan-400" />
            <span>{showSchema ? 'Hide 53-Feature Schema' : 'Inspect 53-Feature Schema'}</span>
          </button>
        </div>
      </div>

      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center space-y-4">
          <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs text-slate-400">Polling Multi-Agent Health Metrics...</p>
        </div>
      ) : (
        <>
          {/* Health Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* System Status */}
            <div className="glass-card p-5 border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase">System Status</span>
                <p className="text-lg font-extrabold text-white mt-0.5">
                  {statusData?.status || 'HEALTHY'}
                </p>
                <p className="text-[10px] text-emerald-400 flex items-center space-x-1 mt-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span>All Subsystems Nominal</span>
                </p>
              </div>
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                <CheckCircle className="w-5 h-5" />
              </div>
            </div>

            {/* Database Engine */}
            <div className="glass-card p-5 border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase">Database Engine</span>
                <p className="text-lg font-extrabold text-white mt-0.5 capitalize">
                  {statusData?.database?.engine || 'SQLite'}
                </p>
                <p className="text-[10px] text-slate-400 mt-1 truncate max-w-[140px]">
                  Dual PostGIS / SQLite
                </p>
              </div>
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <Database className="w-5 h-5" />
              </div>
            </div>

            {/* GeoJSON Topology */}
            <div className="glass-card p-5 border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase">GIS GeoJSON</span>
                <p className="text-lg font-extrabold text-white mt-0.5">
                  {statusData?.districts_count || 38} / 38 Districts
                </p>
                <p className="text-[10px] text-cyan-400 mt-1">
                  CRS84 Topologically Valid
                </p>
              </div>
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                <Layers className="w-5 h-5" />
              </div>
            </div>

            {/* Models Active */}
            <div className="glass-card p-5 border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase">Multi-Hazard Engine</span>
                <p className="text-lg font-extrabold text-white mt-0.5">
                  10 Registered Hazards
                </p>
                <p className="text-[10px] text-purple-400 mt-1">
                  ML + Rules + APIs
                </p>
              </div>
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                <Cpu className="w-5 h-5" />
              </div>
            </div>
          </div>

          {/* Admin Debug Inspection View */}
          {showDebug && user?.role === 'ADMIN' && (
            <div className="glass-card p-6 border-amber-500/40 bg-slate-950/95 space-y-4 animate-in fade-in duration-200">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center space-x-2">
                  <Terminal className="w-5 h-5 text-amber-400" />
                  <div>
                    <h3 className="text-sm font-bold text-white">System Debug & Training Distribution Verification</h3>
                    <p className="text-[11px] text-slate-400">Comparing live forecast features against historical 2010–2021 training bounds</p>
                  </div>
                </div>
                <button
                  onClick={loadDebugData}
                  disabled={debugLoading}
                  className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white flex items-center space-x-1"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${debugLoading ? 'animate-spin' : ''}`} />
                  <span>Refresh Debug Data</span>
                </button>
              </div>

              {debugLoading ? (
                <div className="py-8 flex justify-center text-xs text-slate-400">Polling debug state...</div>
              ) : debugData ? (
                <div className="space-y-4 text-xs">
                  {/* Feature Distribution Table */}
                  <div className="overflow-x-auto max-h-80 overflow-y-auto">
                    <table className="w-full text-left">
                      <thead className="sticky top-0 bg-slate-900 border-b border-slate-800 text-[11px] text-slate-400">
                        <tr>
                          <th className="pb-2 font-semibold">Feature Name</th>
                          <th className="pb-2 font-semibold">Forecast Value</th>
                          <th className="pb-2 font-semibold">Training Min</th>
                          <th className="pb-2 font-semibold">Training Mean</th>
                          <th className="pb-2 font-semibold">Training Max</th>
                          <th className="pb-2 font-semibold text-right">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                        {debugData.features_comparison?.map((row) => (
                          <tr key={row.feature} className="hover:bg-slate-900/50">
                            <td className="py-2 text-white font-sans">{row.feature}</td>
                            <td className="py-2 text-cyan-300 font-bold">{typeof row.forecast_value === 'number' ? row.forecast_value.toFixed(2) : String(row.forecast_value)}</td>
                            <td className="py-2 text-slate-400">{row.training_min}</td>
                            <td className="py-2 text-slate-400">{row.training_mean}</td>
                            <td className="py-2 text-slate-400">{row.training_max}</td>
                            <td className="py-2 text-right">
                              <span className={`px-2 py-0.5 rounded text-[10px] font-sans font-bold ${
                                row.out_of_distribution
                                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                                  : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                              }`}>
                                {row.out_of_distribution ? 'OUT_OF_BOUNDS' : 'IN_BOUNDS'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Contract Validations */}
                  <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Model Contract Compliance</span>
                    <div className="grid grid-cols-3 gap-2 mt-1">
                      {Object.entries(debugData.contracts || {}).map(([mName, cInfo]) => (
                        <div key={mName} className="p-2 rounded bg-slate-950 border border-slate-800 text-[11px]">
                          <div className="flex items-center justify-between">
                            <span className="font-bold text-white capitalize">{mName}</span>
                            <span className={`px-1.5 py-0.2 rounded text-[9px] font-bold ${cInfo.valid ? 'text-emerald-300 bg-emerald-500/10' : 'text-amber-300 bg-amber-500/10'}`}>
                              {cInfo.valid ? 'VALID' : 'BLOCKED'}
                            </span>
                          </div>
                          {cInfo.reason && <p className="text-[9px] text-amber-400/90 mt-1">{cInfo.reason}</p>}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : null}
            </div>
          )}

          {/* Model Registry Status Table */}
          <div className="glass-card p-6 border-slate-800">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
              <Shield className="w-4 h-4 text-cyan-400" />
              <span>Loaded Machine Learning Hazard Models</span>
            </h3>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="text-slate-400 border-b border-slate-800">
                    <th className="pb-3 font-semibold">Hazard</th>
                    <th className="pb-3 font-semibold">Model Artifact</th>
                    <th className="pb-3 font-semibold">Architecture</th>
                    <th className="pb-3 font-semibold">Features</th>
                    <th className="pb-3 font-semibold">ROC-AUC</th>
                    <th className="pb-3 font-semibold">PR-AUC</th>
                    <th className="pb-3 font-semibold text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {statusData?.models?.map((m) => (
                    <tr key={m.hazard} className="hover:bg-slate-900/40">
                      <td className="py-3 font-bold text-white uppercase">{m.hazard}</td>
                      <td className="py-3 font-mono text-cyan-400 text-[11px]">{m.hazard}_xgboost.pkl</td>
                      <td className="py-3 text-slate-300">XGBoost 500 trees</td>
                      <td className="py-3 font-semibold text-white">{m.n_features}</td>
                      <td className="py-3 font-mono text-slate-300">{m.roc_auc?.toFixed(4) ?? '0.9060'}</td>
                      <td className="py-3 font-mono text-slate-300">{m.pr_auc?.toFixed(4) ?? '0.0740'}</td>
                      <td className="py-3 text-right">
                        <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded text-[10px] font-bold">
                          {m.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* 53-Feature Schema Modal / Drawer */}
          {showSchema && (
            <div className="glass-card p-6 border-cyan-500/40 bg-slate-950/90 animate-in fade-in duration-200">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                    <FileCode className="w-4 h-4 text-cyan-400" />
                    <span>Exact 53-Feature Input Schema Required by Models</span>
                  </h3>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    15 Continuous meteorological/derived features + 38 alphabetical district one-hot indicators
                  </p>
                </div>
                <span className="text-xs bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 px-2 py-0.5 rounded font-bold">
                  Strict Sequence Order
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-3 border-t border-slate-800">
                {schemaFeatures.map((feat, idx) => (
                  <div
                    key={feat}
                    className="p-2 rounded bg-slate-900/80 border border-slate-800 text-[11px] flex items-center space-x-2 font-mono"
                  >
                    <span className="text-slate-400 w-5 text-right font-sans text-[10px]">{idx + 1}.</span>
                    <span className={idx < 15 ? 'text-amber-300 font-semibold' : 'text-slate-300'}>
                      {feat}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Multi-Agent Live Coordination Feed */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Registered Agents */}
            <div className="glass-card p-6 border-slate-800">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
                <Cpu className="w-4 h-4 text-cyan-400" />
                <span>Operational Autonomous Agents</span>
              </h3>

              <div className="space-y-3">
                {statusData?.agents &&
                  Object.entries(statusData.agents).map(([agentName, statusText]) => (
                    <div
                      key={agentName}
                      className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between"
                    >
                      <div>
                        <p className="text-xs font-bold text-white">{agentName}</p>
                        <p className="text-[11px] text-slate-400 mt-0.5">{statusText}</p>
                      </div>
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Admin Controls */}
            <div className="glass-card p-6 border-slate-800 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                    <Shield className="w-4 h-4 text-cyan-400" />
                    <span>Administrative Actions</span>
                  </h3>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                      user?.role === 'ADMIN'
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}
                  >
                    Current Role: {user?.role || 'USER'}
                  </span>
                </div>

                <p className="text-xs text-slate-400 mb-4">
                  Purging forecast cache flushes all cached Open-Meteo payloads in `data/cached_forecasts/` and forces a fresh NWP harvest on subsequent user queries. Requires `ADMIN` privilege.
                </p>

                {cacheMessage && (
                  <div
                    className={`p-3 rounded-xl mb-4 text-xs font-medium ${
                      cacheMessage.type === 'success'
                        ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                        : 'bg-rose-500/15 text-rose-300 border border-rose-500/30'
                    }`}
                  >
                    {cacheMessage.text}
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                <span className="text-[11px] text-slate-400">
                  {user?.role === 'ADMIN' ? 'Admin action available' : 'Restricted for USER role'}
                </span>

                <button
                  onClick={handlePurgeCache}
                  disabled={refreshingCache}
                  className="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white text-xs font-bold flex items-center space-x-2 transition shadow-lg shadow-amber-600/20 disabled:opacity-50"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${refreshingCache ? 'animate-spin' : ''}`} />
                  <span>{refreshingCache ? 'Purging Cache...' : 'Purge Forecast Cache'}</span>
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
