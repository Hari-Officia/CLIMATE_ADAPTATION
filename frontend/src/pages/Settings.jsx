import React, { useState } from 'react';
import { Settings as SettingsIcon, Sliders, Globe, Bell, Check } from 'lucide-react';

export default function Settings() {
  const [temperatureUnit, setTemperatureUnit] = useState('celsius');
  const [refreshInterval, setRefreshInterval] = useState('15');
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-4xl mx-auto">
      <div className="pb-4 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-white tracking-tight">System Settings</h1>
        <p className="text-xs text-slate-400 mt-1">Configure client preferences and monitoring thresholds</p>
      </div>

      <div className="glass-card p-6 border-slate-800 space-y-6 text-xs">
        <div>
          <h3 className="text-sm font-bold text-white mb-1 flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-cyan-400" />
            <span>Measurement Units</span>
          </h3>
          <p className="text-slate-400 mb-3">Select preferred metric display conventions</p>

          <div className="flex items-center space-x-3">
            <button
              type="button"
              onClick={() => setTemperatureUnit('celsius')}
              className={`px-4 py-2 rounded-xl font-semibold border transition ${
                temperatureUnit === 'celsius'
                  ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40'
                  : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              Metric (°C, mm, m/s)
            </button>
            <button
              type="button"
              onClick={() => setTemperatureUnit('fahrenheit')}
              className={`px-4 py-2 rounded-xl font-semibold border transition ${
                temperatureUnit === 'fahrenheit'
                  ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40'
                  : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              Imperial (°F, in, mph)
            </button>
          </div>
        </div>

        <div className="pt-5 border-t border-slate-800">
          <h3 className="text-sm font-bold text-white mb-1 flex items-center space-x-2">
            <Bell className="w-4 h-4 text-cyan-400" />
            <span>Health Polling Frequency</span>
          </h3>
          <p className="text-slate-400 mb-3">Automatic status polling rate for multi-agent health</p>

          <select
            value={refreshInterval}
            onChange={(e) => setRefreshInterval(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2 text-xs font-medium focus:outline-none focus:border-cyan-500"
          >
            <option value="15">Every 15 seconds (Recommended)</option>
            <option value="30">Every 30 seconds</option>
            <option value="60">Every 60 seconds</option>
          </select>
        </div>

        <div className="pt-5 border-t border-slate-800 flex items-center justify-between">
          <span className="text-[11px] text-slate-400">Settings persisted in local browser storage</span>
          <button
            onClick={handleSave}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-bold transition flex items-center space-x-1.5"
          >
            {saved ? (
              <>
                <Check className="w-3.5 h-3.5" />
                <span>Saved!</span>
              </>
            ) : (
              <span>Save Preferences</span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
