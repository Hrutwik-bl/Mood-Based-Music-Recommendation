import { useState, useEffect } from 'react';
import api from '../api/client';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is already logged in on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      // User is logged in (we don't have an endpoint to verify, so we assume it's valid)
      setUser({ token });
    }
    setLoading(false);
  }, []);

  const signup = async (email, password) => {
    try {
      setError(null);
      const response = await api.post('/auth/signup', { email, password });
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      setUser({ token: access_token });
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.detail || 'Signup failed';
      setError(message);
      return { success: false, error: message };
    }
  };

  const login = async (email, password) => {
    try {
      setError(null);
      const response = await api.post('/auth/login', { email, password });
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      setUser({ token: access_token });
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.detail || 'Login failed';
      setError(message);
      return { success: false, error: message };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    window.location.href = '/';
  };

  return {
    user,
    loading,
    error,
    signup,
    login,
    logout,
    isAuthenticated: !!user,
  };
};
