import React from 'react';
import { User, Mail, ShieldCheck, Calendar, Key, Check } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-4xl mx-auto">
      <div className="pb-4 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-white tracking-tight">Operator Profile</h1>
        <p className="text-xs text-slate-400 mt-1">Authenticated credentials and access privileges</p>
      </div>

      <div className="glass-card p-6 border-slate-800 space-y-6">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white text-2xl font-extrabold shadow-lg shadow-cyan-500/20">
            {user?.full_name?.charAt(0) || 'U'}
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">{user?.full_name || 'Operator'}</h2>
            <p className="text-xs text-slate-400">@{user?.username || 'user'}</p>
            <div className="mt-2">
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                  user?.role === 'ADMIN'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                    : 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40'
                }`}
              >
                Role: {user?.role || 'USER'}
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-800 text-xs">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
            <span className="text-slate-400 text-[11px] block">Email Contact</span>
            <span className="font-semibold text-white mt-1 block">
              {user?.email || `${user?.username || 'user'}@climaterisk.tn.gov.in`}
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
            <span className="text-slate-400 text-[11px] block">Role Permissions</span>
            <span className="font-semibold text-white mt-1 block">
              {user?.role === 'ADMIN' ? 'Full System & Cache Administration' : 'Operational Dashboard Read & Inference'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
