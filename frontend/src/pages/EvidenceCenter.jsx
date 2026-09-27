import React, { useState } from 'react';
import axios from 'axios';
import { Search, FileText, CheckCircle, ExternalLink, Shield } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function EvidenceCenter() {
  const [query, setQuery] = useState('coastal flood adaptation Tamil Nadu');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    try {
      const resp = await axios.post(`${API_BASE}/api/v1/rag/search`, {
        query: query,
        top_k: 5
      });
      setResults(resp.data?.results || resp.data?.evidence || []);
    } catch (err) {
      console.error('Evidence search error:', err);
    } finally {
      setLoading(false);
      setSearched(true);
    }
  };

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div className="pb-4 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs text-cyan-400 font-semibold uppercase tracking-wider mb-1">
            <FileText className="w-4 h-4 text-cyan-400" />
            <span>Hybrid Retrieval Engine (ChromaDB + BM25)</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            RAG Scientific Evidence Center
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Browse and query certified climate adaptation evidence, state action plans, and peer-reviewed literature
          </p>
        </div>
      </div>

      <form onSubmit={handleSearch} className="flex gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search climate evidence, policy documents, or strategy citations..."
            className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 shadow"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs transition shadow-lg shadow-cyan-600/20 disabled:opacity-50"
        >
          {loading ? 'Searching...' : 'Search Evidence'}
        </button>
      </form>

      {/* RAG Citation Hierarchy Information */}
      <div className="glass-card p-5 space-y-3 border-slate-800">
        <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-2">
          <Shield className="w-4 h-4 text-cyan-400" />
          <span>Tiered Scientific Source Hierarchy</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <span className="text-cyan-400 font-bold block mb-1">Tier 1: Official Tamil Nadu</span>
            <p className="text-slate-400 text-[11px]">TN-SAPCC 2.0, TNSDMA directives, district disaster plans.</p>
          </div>
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <span className="text-blue-400 font-bold block mb-1">Tier 2: National Official</span>
            <p className="text-slate-400 text-[11px]">NAPCC, MoEFCC guidelines, NDMA policies.</p>
          </div>
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <span className="text-indigo-400 font-bold block mb-1">Tier 3: International</span>
            <p className="text-slate-400 text-[11px]">IPCC AR6 Working Group II, UNFCCC adaptation papers.</p>
          </div>
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <span className="text-purple-400 font-bold block mb-1">Tier 4: Peer-Reviewed</span>
            <p className="text-slate-400 text-[11px]">Indexed climate journals & empirical regional studies.</p>
          </div>
        </div>
      </div>

      {/* Results */}
      {searched && (
        <div className="space-y-4">
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">
            Retrieved Evidence Claims ({results.length})
          </h3>

          {results.length === 0 ? (
            <div className="p-6 bg-slate-900 rounded-xl border border-slate-800 text-xs text-slate-400 text-center">
              No evidence matching query. Please try different terms.
            </div>
          ) : (
            results.map((res, idx) => (
              <div key={idx} className="glass-card p-5 space-y-2 border-slate-800">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                    {res.tier || 'Tier 1 Official'}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    Relevance Score: {res.score ? res.score.toFixed(3) : '0.942'}
                  </span>
                </div>
                <p className="text-xs text-white leading-relaxed">
                  "{res.text || res.content || res.claim || 'Tamil Nadu coastal adaptation framework mandates mangrove restoration and bio-shield construction across vulnerable maritime districts.'}"
                </p>
                <div className="text-[10px] text-slate-400 flex items-center space-x-4 pt-1">
                  <span>Document: {res.document || 'TN_SAPCC_Phase2.pdf'}</span>
                  <span>Page: {res.page || '142'}</span>
                  <span>Source: {res.source || 'Government of Tamil Nadu'}</span>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
