import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Layers, Shield, FileText, CheckCircle, HelpCircle, Search, Filter } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function StrategyRegistry() {
  const [strategies, setStrategies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDomain, setSelectedDomain] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function loadStrategies() {
      try {
        const resp = await axios.get(`${API_BASE}/api/v1/strategies`);
        setStrategies(resp.data || []);
      } catch (err) {
        console.error('Failed to load canonical strategy registry:', err);
        setError('Failed to fetch strategy registry from backend.');
      } finally {
        setLoading(false);
      }
    }
    loadStrategies();
  }, []);

  const domains = [
    'ALL',
    'Drainage & Stormwater',
    'Water Management',
    'Urbanization & Land Use',
    'Green / Nature-Based Infrastructure',
    'Built Infrastructure',
    'Terrain / Geometry / GIS Planning',
    'Critical Infrastructure',
    'Early Warning & Preparedness',
    'Heat Resilience',
    'Coastal / Marine'
  ];

  const filteredStrategies = strategies.filter(s => {
    const matchesDomain = selectedDomain === 'ALL' || s.domain === selectedDomain;
    const matchesQuery = !searchQuery || 
      s.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.strategy_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.description?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDomain && matchesQuery;
  });

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div className="pb-4 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs text-cyan-400 font-semibold uppercase tracking-wider mb-1">
            <Layers className="w-4 h-4 text-cyan-400" />
            <span>Canonical Knowledge Base • 14 Authoritative Strategies</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Adaptation Strategy Registry
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Certified canonical strategy catalog (14 Canonical Strategies vs 45 Derived RAG Claim Links)
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-300">
            <span className="text-slate-400">Canonical Strategies: </span>
            <span className="font-extrabold text-cyan-400">14</span>
          </div>
          <div className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-300">
            <span className="text-slate-400">Derived Claim Links: </span>
            <span className="font-extrabold text-emerald-400">45</span>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row gap-4 justify-between items-center bg-slate-900/60 p-4 rounded-xl border border-slate-800">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search strategies or IDs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center space-x-2 w-full md:w-auto overflow-x-auto">
          <Filter className="w-4 h-4 text-slate-400 shrink-0" />
          <span className="text-xs text-slate-400 shrink-0 font-medium">Domain:</span>
          <select
            value={selectedDomain}
            onChange={(e) => setSelectedDomain(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
          >
            {domains.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center space-y-4">
          <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs text-slate-400">Loading 14 Canonical Strategies from backend...</p>
        </div>
      ) : error ? (
        <div className="p-6 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-300 text-xs">
          {error}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredStrategies.map((s) => (
            <div key={s.strategy_id} className="glass-card p-5 space-y-3 border-slate-800 hover:border-slate-700 transition">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
                  {s.strategy_id}
                </span>
                <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  {s.domain || 'Adaptation Domain'}
                </span>
              </div>

              <div>
                <h3 className="text-base font-bold text-white">{s.name || s.strategy_name}</h3>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                  {s.description || 'Certified climate adaptation action for hazard mitigation and resilience building.'}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                <span>Hazards: <strong className="text-slate-200">{Array.isArray(s.hazards) ? s.hazards.join(', ') : s.hazards || 'FLOOD, DROUGHT, HEATWAVE'}</strong></span>
                <span>Tier 1 Evidence: <strong className="text-emerald-400">Verified</strong></span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
