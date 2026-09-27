import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Weather from './pages/Weather';
import RiskMap from './pages/RiskMap';
import SystemStatus from './pages/SystemStatus';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import DistrictDetail from './pages/DistrictDetail';
import Methodology from './pages/Methodology';
import Sources from './pages/Sources';
import StrategyRegistry from './pages/StrategyRegistry';
import OptimizationOverview from './pages/OptimizationOverview';
import QAOAResearch from './pages/QAOAResearch';
import EvidenceCenter from './pages/EvidenceCenter';
import ResearchGaps from './pages/ResearchGaps';
import QuantumAdvantageOverview from './pages/QuantumAdvantageOverview';

function Layout({ children }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user && location.pathname !== '/login') {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
      <Sidebar />
      <main className="flex-1 overflow-y-auto min-h-screen">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Layout><Dashboard /></Layout>} />
          <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
          <Route path="/weather" element={<Layout><Weather /></Layout>} />
          <Route path="/risk-map" element={<Layout><RiskMap /></Layout>} />
          <Route path="/map" element={<Layout><RiskMap /></Layout>} />
          <Route path="/district/:districtId" element={<Layout><DistrictDetail /></Layout>} />
          <Route path="/decision/:decisionId" element={<Layout><DistrictDetail /></Layout>} />
          <Route path="/strategies" element={<Layout><StrategyRegistry /></Layout>} />
          <Route path="/optimization" element={<Layout><OptimizationOverview /></Layout>} />
          <Route path="/qaoa" element={<Layout><QAOAResearch /></Layout>} />
          <Route path="/research/quantum" element={<Layout><QuantumAdvantageOverview /></Layout>} />
          <Route path="/evidence" element={<Layout><EvidenceCenter /></Layout>} />
          <Route path="/research" element={<Layout><ResearchGaps /></Layout>} />
          <Route path="/methodology" element={<Layout><Methodology /></Layout>} />
          <Route path="/sources" element={<Layout><Sources /></Layout>} />
          <Route path="/system" element={<Layout><SystemStatus /></Layout>} />
          <Route path="/system-status" element={<Layout><SystemStatus /></Layout>} />
          <Route path="/profile" element={<Layout><Profile /></Layout>} />
          <Route path="/settings" element={<Layout><Settings /></Layout>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
