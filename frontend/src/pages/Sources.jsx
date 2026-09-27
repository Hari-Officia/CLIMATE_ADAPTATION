import React from 'react';
import { Database, FileText, CheckCircle, ExternalLink } from 'lucide-react';

export default function Sources() {
  const sourcesList = [
    { id: 'SRC-001', title: 'Tamil Nadu State Action Plan on Climate Change (TN-SAPCC 2.0)', tier: 'Tier 1', org: 'Department of Environment & Climate Change, Govt of Tamil Nadu', year: 2023 },
    { id: 'SRC-002', title: 'IPCC Sixth Assessment Report (AR6 WGII - Impacts, Adaptation & Vulnerability)', tier: 'Tier 1', org: 'Intergovernmental Panel on Climate Change', year: 2022 },
    { id: 'SRC-003', title: 'IMD Climatological Normals & Extreme Weather Records', tier: 'Tier 1', org: 'India Meteorological Department (IMD)', year: 2024 },
    { id: 'SRC-004', title: 'NASA POWER Hydro-Meteorological Data Surface', tier: 'Tier 2', org: 'NASA Applied Sciences Program', year: 2024 }
  ];

  return (
    <div className="p-6 lg:p-8 max-w-5xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white tracking-tight">Authoritative Knowledge Base & Evidence Sources</h1>
        <p className="text-xs text-slate-400 mt-1">
          Peer-reviewed publications, government action plans, and official meteorological data indexes supporting RAG decision claims.
        </p>
      </div>

      <div className="space-y-3">
        {sourcesList.map((src) => (
          <div key={src.id} className="glass-card p-4 space-y-2 border-slate-800">
            <div className="flex items-center justify-between">
              <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                {src.tier}
              </span>
              <span className="text-xs font-mono text-slate-400">{src.id}</span>
            </div>
            <h3 className="text-sm font-bold text-white">{src.title}</h3>
            <div className="text-xs text-slate-400 flex items-center justify-between pt-1">
              <span>{src.org}</span>
              <span>Year: {src.year}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
