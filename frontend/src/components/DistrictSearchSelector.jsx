import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Search, MapPin, ChevronDown, Check, X } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

const NOTABLE_FALLBACKS = [
  { district_id: 'ariyalur', district_name: 'Ariyalur', coastal: false },
  { district_id: 'chengalpattu', district_name: 'Chengalpattu', coastal: true },
  { district_id: 'chennai', district_name: 'Chennai', coastal: true },
  { district_id: 'coimbatore', district_name: 'Coimbatore', coastal: false },
  { district_id: 'cuddalore', district_name: 'Cuddalore', coastal: true },
  { district_id: 'dharmapuri', district_name: 'Dharmapuri', coastal: false },
  { district_id: 'dindigul', district_name: 'Dindigul', coastal: false },
  { district_id: 'erode', district_name: 'Erode', coastal: false },
  { district_id: 'kallakurichi', district_name: 'Kallakurichi', coastal: false },
  { district_id: 'kancheepuram', district_name: 'Kancheepuram', coastal: false },
  { district_id: 'kanniyakumari', district_name: 'Kanniyakumari', coastal: true },
  { district_id: 'karur', district_name: 'Karur', coastal: false },
  { district_id: 'krishnagiri', district_name: 'Krishnagiri', coastal: false },
  { district_id: 'madurai', district_name: 'Madurai', coastal: false },
  { district_id: 'mayiladuthurai', district_name: 'Mayiladuthurai', coastal: true },
  { district_id: 'nagapattinam', district_name: 'Nagapattinam', coastal: true },
  { district_id: 'namakkal', district_name: 'Namakkal', coastal: false },
  { district_id: 'nilgiris', district_name: 'Nilgiris', coastal: false },
  { district_id: 'perambalur', district_name: 'Perambalur', coastal: false },
  { district_id: 'pudukkottai', district_name: 'Pudukkottai', coastal: true },
  { district_id: 'ramanathapuram', district_name: 'Ramanathapuram', coastal: true },
  { district_id: 'ranipet', district_name: 'Ranipet', coastal: false },
  { district_id: 'salem', district_name: 'Salem', coastal: false },
  { district_id: 'sivaganga', district_name: 'Sivaganga', coastal: false },
  { district_id: 'tenkasi', district_name: 'Tenkasi', coastal: false },
  { district_id: 'thanjavur', district_name: 'Thanjavur', coastal: true },
  { district_id: 'theni', district_name: 'Theni', coastal: false },
  { district_id: 'thoothukudi', district_name: 'Thoothukudi', coastal: true },
  { district_id: 'tiruchirappalli', district_name: 'Tiruchirappalli', coastal: false },
  { district_id: 'tirunelveli', district_name: 'Tirunelveli', coastal: true },
  { district_id: 'tirupathur', district_name: 'Tirupathur', coastal: false },
  { district_id: 'tiruppur', district_name: 'Tiruppur', coastal: false },
  { district_id: 'tiruvallur', district_name: 'Tiruvallur', coastal: true },
  { district_id: 'tiruvannamalai', district_name: 'Tiruvannamalai', coastal: false },
  { district_id: 'tiruvarur', district_name: 'Tiruvarur', coastal: true },
  { district_id: 'vellore', district_name: 'Vellore', coastal: false },
  { district_id: 'viluppuram', district_name: 'Viluppuram', coastal: true },
  { district_id: 'virudhunagar', district_name: 'Virudhunagar', coastal: false }
];

export default function DistrictSearchSelector({ selectedDistrictId, onSelectDistrict, className = "" }) {
  const [districts, setDistricts] = useState(NOTABLE_FALLBACKS);
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const containerRef = useRef(null);

  useEffect(() => {
    axios.get(`${API_BASE}/districts`)
      .then(res => {
        if (res.data && res.data.length > 0) {
          const formatted = res.data.map(d => ({
            district_id: d.district_id || d.id,
            district_name: d.district_name || d.name || d.district_id,
            coastal: d.profile ? d.profile.coastal : (d.coastal || false)
          }));
          setDistricts(formatted);
        }
      })
      .catch(err => console.warn('Using district fallback list:', err));
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const currentDistrict = districts.find(d => 
    String(d.district_id).toLowerCase() === String(selectedDistrictId).toLowerCase()
  ) || districts.find(d => d.district_id === 'chennai') || districts[0];

  const filteredDistricts = districts.filter(d => 
    d.district_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.district_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelect = (dist) => {
    onSelectDistrict(dist.district_id);
    setIsOpen(false);
    setSearchTerm('');
  };

  return (
    <div className={`relative z-50 ${className}`} ref={containerRef}>
      {/* Selector Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-3 bg-slate-900/90 border border-slate-700 hover:border-cyan-500/60 text-white rounded-xl px-4 py-2.5 text-xs font-semibold shadow-lg transition-all"
      >
        <div className="flex items-center space-x-2 truncate">
          <MapPin className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
          <span className="truncate">{currentDistrict?.district_name} District</span>
          {currentDistrict?.coastal && (
            <span className="text-[10px] bg-teal-500/20 text-teal-300 border border-teal-500/30 px-1.5 py-0.5 rounded shrink-0">
              Coastal
            </span>
          )}
        </div>
        <ChevronDown className={`w-3.5 h-3.5 text-slate-400 shrink-0 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown Panel */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-72 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-150">
          {/* Search Box Header */}
          <div className="p-2.5 border-b border-slate-800 bg-slate-950/80 flex items-center space-x-2">
            <Search className="w-4 h-4 text-cyan-400 shrink-0" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search 38 TN districts..."
              autoFocus
              className="w-full bg-transparent text-xs text-white placeholder-slate-500 focus:outline-none"
            />
            {searchTerm && (
              <button onClick={() => setSearchTerm('')} className="text-slate-400 hover:text-white">
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* District List Container */}
          <div className="max-h-64 overflow-y-auto divide-y divide-slate-800/50 scrollbar-thin scrollbar-thumb-slate-700">
            {filteredDistricts.length === 0 ? (
              <div className="p-4 text-center text-xs text-slate-500">
                No matching district found
              </div>
            ) : (
              filteredDistricts.map((d) => {
                const isSelected = String(d.district_id).toLowerCase() === String(selectedDistrictId).toLowerCase();
                return (
                  <button
                    key={d.district_id}
                    type="button"
                    onClick={() => handleSelect(d)}
                    className={`w-full text-left px-3.5 py-2.5 text-xs flex items-center justify-between transition-colors ${
                      isSelected 
                        ? 'bg-cyan-500/15 text-cyan-300 font-semibold' 
                        : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      <span>{d.district_name}</span>
                      {d.coastal && (
                        <span className="text-[10px] text-teal-400/80 bg-teal-950/50 px-1 py-0.2 rounded border border-teal-800/40">
                          🌊 Coastal
                        </span>
                      )}
                    </div>
                    {isSelected && <Check className="w-3.5 h-3.5 text-cyan-400" />}
                  </button>
                );
              })
            )}
          </div>

          {/* Footer Info */}
          <div className="px-3 py-2 bg-slate-950/90 border-t border-slate-800 text-[10px] text-slate-500 flex justify-between">
            <span>Tamil Nadu • 38 Districts</span>
            <span>{filteredDistricts.length} shown</span>
          </div>
        </div>
      )}
    </div>
  );
}
