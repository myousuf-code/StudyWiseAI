import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { User, LoginRequest, RegisterRequest } from '../types/index';
import { apiService, AUTH_LOGOUT_EVENT } from '../services/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const token = sessionStorage.getItem('authToken');
    const savedUser = sessionStorage.getItem('user');

    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('authToken');
      }
    }
    setIsLoading(false);
  }, []);

  // Listen for 401 logout events dispatched by the API service
  useEffect(() => {
    const handleForceLogout = () => setUser(null);
    window.addEventListener(AUTH_LOGOUT_EVENT, handleForceLogout);
    return () => window.removeEventListener(AUTH_LOGOUT_EVENT, handleForceLogout);
  }, []);

  const login = async (credentials: LoginRequest) => {
    const response = await apiService.login(credentials);
    sessionStorage.setItem('authToken', response.access_token);
    sessionStorage.setItem('user', JSON.stringify(response.user));
    setUser(response.user);
  };

  const register = async (data: RegisterRequest) => {
    await apiService.register(data);
    // After registration, user needs to log in
  };

  const logout = () => {
    sessionStorage.removeItem('authToken');
    sessionStorage.removeItem('user');
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
