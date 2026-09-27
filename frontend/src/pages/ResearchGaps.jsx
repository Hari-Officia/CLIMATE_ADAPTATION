import React from 'react';
import { AlertTriangle, ShieldCheck, Database, Cpu } from 'lucide-react';

export default function ResearchGaps() {
  const gaps = [
    {
      id: 'RG-001',
      title: 'QAOA Circuit Depth & Scaling Limitation',
      status: 'UNDER_INVESTIGATION',
      severity: 'HIGH',
      impact: 'Limits quantum solver accuracy to reference gap 0.4700 at depth p=1..4.',
      description: 'Quantum approximate optimization algorithm performance on current noisy quantum simulators exhibits significant objective gaps compared to classical HIGHS MILP solver.'
    },
    {
      id: 'RG-002',
      title: 'Ground-Truth Adaptation Outcome Label Delay',
      status: 'MONITORED',
      severity: 'MEDIUM',
      impact: 'Observational validation labels require 1–3 years of longitudinal field outcome data.',
      description: 'Adaptation measures like mangrove restoration or rainwater harvesting require multi-year observation windows before real-world reduction in vulnerability can be quantitatively confirmed.'
    },
    {
      id: 'RG-003',
      title: 'Coastal Surge Downscaling Uncertainty',
      status: 'ACCEPTED_BOUND',
      severity: 'MEDIUM',
      impact: 'Hydrodynamic coastal storm surge downscaling introduces ±12% local elevation uncertainty.',
      description: 'High-resolution digital elevation models (DEM) for low-lying coastal districts carry spatial resolution tolerances affecting extreme wave inundation modeling.'
    },
    {
      id: 'NC-002',
      title: 'Single-Node PostgreSQL Staging Non-HA Status',
      status: 'ACCEPTED_RISK',
      severity: 'MEDIUM',
      impact: 'Single-node database instance in staging environment lacks active-active replication.',
      description: 'High availability (HA) cluster migration scheduled for v4.0.0. Current deployment certified under ACCEPTED_RISK condition.'
    }
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div className="pb-4 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs text-amber-400 font-semibold uppercase tracking-wider mb-1">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>Scientific & Technological Governance • Known Limitations</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Research Gaps & System Limitations
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Transparent registry of active scientific research gaps, model uncertainties, and engineering non-conformities
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {gaps.map((gap) => (
          <div key={gap.id} className="glass-card p-6 space-y-3 border-slate-800">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded border border-cyan-500/20">
                  {gap.id}
                </span>
                <h3 className="text-base font-bold text-white">{gap.title}</h3>
              </div>
              <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full border ${
                gap.severity === 'HIGH' ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' : 'bg-slate-800 text-slate-300 border-slate-700'
              }`}>
                {gap.status}
              </span>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              {gap.description}
            </p>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400">
              <strong className="text-amber-400">Operational Impact: </strong>
              {gap.impact}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
