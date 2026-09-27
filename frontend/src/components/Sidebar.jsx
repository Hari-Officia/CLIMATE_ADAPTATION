import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Map as MapIcon,
  Activity,
  Settings,
  LogOut,
  Globe,
  Layers,
  Cpu,
  FileText,
  AlertTriangle,
  BookOpen,
  Building,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const sections = [
    {
      title: 'OVERVIEW',
      items: [
        { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { to: '/risk-map', label: 'Risk Map (GIS)', icon: MapIcon }
      ]
    },
    {
      title: 'DISTRICT DECISION SUPPORT',
      items: [
        { to: '/district/chennai', label: 'District Intelligence', icon: Building }
      ]
    },
    {
      title: 'KNOWLEDGE',
      items: [
        { to: '/strategies', label: 'Strategy Registry (14)', icon: Layers },
        { to: '/evidence', label: 'Evidence & RAG', icon: FileText },
        { to: '/sources', label: 'Source Hierarchy', icon: BookOpen }
      ]
    },
    {
      title: 'RESEARCH TRACK',
      items: [
        { to: '/research/quantum', label: 'Quantum Advantage Track', icon: Sparkles },
        { to: '/optimization', label: 'Classical MILP', icon: Cpu },
        { to: '/qaoa', label: 'QAOA Research', icon: Cpu },
        { to: '/research', label: 'Research Gaps', icon: AlertTriangle },
        { to: '/methodology', label: 'Methodology', icon: BookOpen }
      ]
    },
    {
      title: 'SYSTEM',
      items: [
        { to: '/system-status', label: 'System Status & Cert.', icon: Activity }
      ]
    }
  ];

  return (
    <aside className="w-64 bg-slate-950/90 border-r border-slate-800/80 flex flex-col h-screen sticky top-0 backdrop-blur-xl z-30 select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800/60">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/25">
            <Globe className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-tight text-white leading-tight">
              Climate Risk
            </h1>
            <p className="text-xs text-cyan-400 font-medium">Quantum Decision Engine</p>
          </div>
        </div>

        {/* Operational Status Pill */}
        <div className="mt-3 flex items-center justify-between px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
          <span className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-[10px] font-bold text-emerald-400">v3.1.0 Certified</span>
          </span>
          <span className="text-[9px] font-mono text-slate-400">38 TN Districts</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-3 space-y-4 overflow-y-auto">
        {sections.map((sec) => (
          <div key={sec.title} className="space-y-1">
            <div className="px-3 text-[9px] font-extrabold text-slate-400 uppercase tracking-wider">
              {sec.title}
            </div>
            {sec.items.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                      isActive
                        ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/10'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span className="truncate">{item.label}</span>
                </NavLink>
              );
            })}
          </div>
        ))}
      </nav>

      {/* User Footer Profile */}
      <div className="p-3 border-t border-slate-800/60 bg-slate-950/40">
        <div className="flex items-center justify-between p-2 rounded-xl bg-slate-900/70 border border-slate-800/80">
          <div className="flex items-center space-x-2.5 min-w-0">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white">
              {user?.full_name ? user.full_name.charAt(0) : 'U'}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-white truncate leading-tight">
                {user?.full_name || user?.username || 'Guest'}
              </p>
              <span className="text-[9px] text-cyan-400 font-mono block">
                {user?.role || 'USER'}
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-1">
            <button
              onClick={() => navigate('/settings')}
              className="p-1 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition"
              title="Settings"
            >
              <Settings className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={handleLogout}
              className="p-1 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition"
              title="Log Out"
            >
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}
