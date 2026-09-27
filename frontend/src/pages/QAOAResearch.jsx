import React from 'react';
import { Cpu, AlertTriangle, ShieldCheck, CheckCircle } from 'lucide-react';

export default function QAOAResearch() {
  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div className="pb-4 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs text-amber-400 font-semibold uppercase tracking-wider mb-1">
            <Cpu className="w-4 h-4 text-amber-400" />
            <span>Quantum Research Module • Phase M Verification</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            QAOA Experimental Research Dashboard
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates Quantum Approximate Optimization Algorithm (QAOA) against classical MILP baseline
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <span className="px-3 py-1.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/40 text-xs font-bold">
            EXPERIMENTAL (Phase M)
          </span>
          <span className="px-3 py-1.5 rounded-xl bg-rose-500/20 text-rose-300 border border-rose-500/40 text-xs font-bold">
            Quantum Advantage: NOT ESTABLISHED
          </span>
        </div>
      </div>

      {/* Mandatory Warning Banner */}
      <div className="glass-card p-5 border-amber-500/40 bg-amber-500/5 space-y-2">
        <div className="flex items-center space-x-2 text-amber-400 font-bold text-sm">
          <AlertTriangle className="w-5 h-5 shrink-0" />
          <span>Scientific Governance Guardrail — Experimental Quantum Disclaimer</span>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed">
          The QAOA quantum solver is evaluated strictly as an experimental benchmark ($p=1..4$, 1024 shots). 
          The classical HIGHS MILP solver remains 100% authoritative for all production adaptation decisions. 
          Current reference objective gap for QAOA is <strong>0.4700</strong>. Quantum advantage has NOT been established.
        </p>
      </div>

      {/* Benchmark Metrics Table */}
      <div className="glass-card p-6 border-slate-800 space-y-4">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider">
          Classical MILP vs QAOA Quantum Benchmark
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-slate-400 border-b border-slate-800">
                <th className="pb-3 font-semibold">Evaluation Metric</th>
                <th className="pb-3 font-semibold text-emerald-400">Classical HIGHS MILP (Authoritative)</th>
                <th className="pb-3 font-semibold text-amber-400">QAOA Quantum Simulator (Experimental)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
              <tr className="hover:bg-slate-900/40">
                <td className="py-3 font-sans text-white font-medium">Solver Classification</td>
                <td className="py-3 text-emerald-300 font-bold">PRODUCTION AUTHORITATIVE</td>
                <td className="py-3 text-amber-300 font-bold">EXPERIMENTAL RESEARCH</td>
              </tr>
              <tr className="hover:bg-slate-900/40">
                <td className="py-3 font-sans text-white font-medium">Reference Objective Gap</td>
                <td className="py-3 text-emerald-300 font-bold">0.0000 (0.0%)</td>
                <td className="py-3 text-amber-400 font-bold">0.4700 (47.0%)</td>
              </tr>
              <tr className="hover:bg-slate-900/40">
                <td className="py-3 font-sans text-white font-medium">Quantum Advantage Claimed</td>
                <td className="py-3 text-slate-400">N/A</td>
                <td className="py-3 text-rose-400 font-bold">FALSE (NOT ESTABLISHED)</td>
              </tr>
              <tr className="hover:bg-slate-900/40">
                <td className="py-3 font-sans text-white font-medium">Circuit Depth (p)</td>
                <td className="py-3 text-slate-400">N/A</td>
                <td className="py-3 text-slate-200">p = 1..4 (Evaluated)</td>
              </tr>
              <tr className="hover:bg-slate-900/40">
                <td className="py-3 font-sans text-white font-medium">Shot Count</td>
                <td className="py-3 text-slate-400">N/A</td>
                <td className="py-3 text-slate-200">1024 shots per depth</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
