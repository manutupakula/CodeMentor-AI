import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, profileAPI } from '../api/client';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('codementor_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('codementor_token');
      if (token) {
        try {
          const res = await authAPI.getMe();
          setUser(res.data);
          localStorage.setItem('codementor_user', JSON.stringify(res.data));
        } catch (err) {
          console.error("Auth verification error", err);
          localStorage.removeItem('codementor_token');
          localStorage.removeItem('codementor_user');
          setUser(null);
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = async (email, password) => {
    const res = await authAPI.login({ email, password });
    const { access_token, user: userData } = res.data;
    localStorage.setItem('codementor_token', access_token);
    localStorage.setItem('codementor_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const register = async (name, email, password, languages, self_declared_level, selected_topics) => {
    const res = await authAPI.register({
      name,
      email,
      password,
      languages,
      self_declared_level,
      selected_topics,
    });
    const { access_token, user: userData } = res.data;
    localStorage.setItem('codementor_token', access_token);
    localStorage.setItem('codementor_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const logout = () => {
    localStorage.removeItem('codementor_token');
    localStorage.removeItem('codementor_user');
    setUser(null);
  };

  const updateUser = (updatedData) => {
    setUser(prev => {
      const merged = { ...prev, ...updatedData };
      localStorage.setItem('codementor_user', JSON.stringify(merged));
      return merged;
    });
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
