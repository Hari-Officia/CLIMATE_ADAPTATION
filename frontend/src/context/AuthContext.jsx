import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

const API_BASE = 'http://localhost:8000';

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user');
    return saved ? JSON.parse(saved) : { username: 'harish', role: 'USER', full_name: 'Harish Kumar' };
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const login = async (username, password) => {
    setLoading(true);
    try {
      const resp = await axios.post(`${API_BASE}/auth/login`, { username, password });
      const data = resp.data;
      setToken(data.access_token);
      const userInfo = {
        username: data.username,
        role: data.role,
        full_name: data.full_name || data.username
      };
      setUser(userInfo);
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(userInfo));
      return { success: true, user: userInfo };
    } catch (err) {
      console.error('Login failed:', err);
      return {
        success: false,
        error: err.response?.data?.detail || 'Invalid username or password'
      };
    } finally {
      setLoading(false);
    }
  };

  const loginAsDemo = async (role) => {
    if (role === 'ADMIN') {
      return await login('admin', 'admin123');
    } else {
      return await login('harish', 'user123');
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ token, user, loading, login, loginAsDemo, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
