import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, CloudRain, Wind, AlertTriangle, ArrowRight, Lock, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [username, setUsername] = useState('harish');
  const [password, setPassword] = useState('user123');
  const [error, setError] = useState(null);
  const { login, loginAsDemo, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    const result = await login(username, password);
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }
  };

  const handleDemoLogin = async (role) => {
    setError(null);
    const result = await loginAsDemo(role);
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col lg:flex-row text-slate-100 selection:bg-cyan-500 selection:text-white">
      {/* Left Column: Atmospheric Branding */}
      <div className="lg:w-1/2 relative p-8 lg:p-16 flex flex-col justify-between overflow-hidden border-b lg:border-b-0 lg:border-r border-slate-800/80 bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950/40">
        {/* Subtle decorative blurred glow */}
        <div className="absolute top-10 left-10 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold mb-6">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
            <span>Review II • Core Operational Foundation</span>
          </div>

          <h1 className="text-3xl lg:text-4xl font-extrabold tracking-tight text-white leading-tight">
            Quantum Multi-Agent Decision Support System
          </h1>
          <p className="mt-3 text-base text-slate-400 font-medium leading-relaxed max-w-lg">
            Climate Adaptation & Mitigation Strategy Planning across Tamil Nadu's 38 administrative districts.
          </p>

          {/* Active Agents Snapshot */}
          <div className="mt-8 space-y-3 max-w-md">
            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center space-x-3 backdrop-blur-sm">
              <div className="w-9 h-9 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <CloudRain className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-white">Climate Data Acquisition Agent</h2>
                <p className="text-[11px] text-slate-400">Open-Meteo API NWP integration with local caching</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center space-x-3 backdrop-blur-sm">
              <div className="w-9 h-9 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                <Wind className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-white">Multi-Hazard Risk Agent</h2>
                <p className="text-[11px] text-slate-400">XGBoost Ensemble: Flood, Drought & Heatwave (53 features)</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center space-x-3 backdrop-blur-sm">
              <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-white">Point-in-Polygon GIS Engine</h2>
                <p className="text-[11px] text-slate-400">Shapely spatial containment & Tamil Nadu district boundaries</p>
              </div>
            </div>
          </div>
        </div>

        <div className="relative z-10 mt-8 pt-6 border-t border-slate-800/60 text-xs text-slate-500">
          Academic Research Project • Department of Computer Science & Engineering
        </div>
      </div>

      {/* Right Column: Authentication Card */}
      <div className="lg:w-1/2 p-8 lg:p-16 flex items-center justify-center bg-slate-950">
        <div className="w-full max-w-md">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white tracking-tight">System Sign-In</h2>
            <p className="text-sm text-slate-400 mt-1">Authenticate to access climate risk dashboards</p>
          </div>

          {error && (
            <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-start space-x-3">
              <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
              <p className="text-xs text-rose-300 font-medium">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wider">
                Username
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <User className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900/90 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition"
                  placeholder="Enter username"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wider">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900/90 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition"
                  placeholder="Enter password"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-sm font-semibold flex items-center justify-center space-x-2 shadow-lg shadow-cyan-500/20 transition disabled:opacity-50"
            >
              <span>{loading ? 'Authenticating...' : 'Sign In'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Preset Demo Logins */}
          <div className="mt-8 pt-6 border-t border-slate-800/80">
            <p className="text-xs font-semibold text-slate-400 text-center mb-3">
              One-Click Review Demo Credentials
            </p>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => handleDemoLogin('USER')}
                disabled={loading}
                className="py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-left transition text-xs group"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white">Harish</span>
                  <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">
                    USER
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">Standard operator</p>
              </button>

              <button
                type="button"
                onClick={() => handleDemoLogin('ADMIN')}
                disabled={loading}
                className="py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-left transition text-xs group"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white">Admin</span>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded border border-amber-500/30">
                    ADMIN
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">System administrator</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
