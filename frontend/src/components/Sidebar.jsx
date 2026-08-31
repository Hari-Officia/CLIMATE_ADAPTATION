import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  CloudSun,
  Map as MapIcon,
  Activity,
  Sparkles,
  Settings,
  LogOut,
  ShieldCheck,
  User as UserIcon,
  Globe
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/weather', label: 'Weather', icon: CloudSun },
    { to: '/risk-map', label: 'Risk Map (GIS)', icon: MapIcon },
    { to: '/system-status', label: 'System Status', icon: Activity },
  ];

  return (
    <aside className="w-64 bg-slate-950/80 border-r border-slate-800/80 flex flex-col h-screen sticky top-0 backdrop-blur-xl z-30 select-none">
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
            <p className="text-xs text-cyan-400 font-medium">Intelligence System</p>
          </div>
        </div>

        {/* Operational Status Pill */}
        <div className="mt-4 flex items-center space-x-2 px-2.5 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="text-[11px] font-medium text-emerald-400">Review II Active (38 Districts)</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
          Core Operations
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}

        {/* Disabled Future Review Phase Link */}
        <div className="pt-3">
          <div className="px-3 pb-2 text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
            Future Modules
          </div>
          <div
            className="flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium text-slate-500 bg-slate-900/30 border border-slate-800/40 cursor-not-allowed opacity-60"
            title="Scheduled for Review III"
          >
            <div className="flex items-center space-x-3">
              <Sparkles className="w-4 h-4 text-purple-400/60" />
              <span>Adaptation Insights</span>
            </div>
            <span className="text-[9px] font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/30 px-1.5 py-0.5 rounded">
              Review III
            </span>
          </div>
        </div>
      </nav>

      {/* User Footer Profile */}
      <div className="p-3 border-t border-slate-800/60 bg-slate-950/40">
        <div className="flex items-center justify-between p-2 rounded-xl bg-slate-900/70 border border-slate-800/80">
          <div className="flex items-center space-x-3 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white">
              {user?.full_name ? user.full_name.charAt(0) : 'U'}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-white truncate leading-snug">
                {user?.full_name || user?.username || 'Guest'}
              </p>
              <div className="flex items-center space-x-1.5">
                <span
                  className={`text-[9px] font-bold px-1.5 py-0.2 rounded border ${
                    user?.role === 'ADMIN'
                      ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                      : 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40'
                  }`}
                >
                  {user?.role || 'USER'}
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-1">
            <button
              onClick={() => navigate('/settings')}
              className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition"
              title="Settings"
            >
              <Settings className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={handleLogout}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition"
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
