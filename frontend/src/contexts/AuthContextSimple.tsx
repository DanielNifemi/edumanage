import React, { useState } from 'react';
import { AuthContext, User, AuthContextType } from './AuthContextTypes';

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProviderSimple: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log('Simple login attempt:', { email, password });
      // Mock successful login
      const mockUser: User = {
        id: '1',
        email: email,
        firstName: 'Test',
        lastName: 'User',
        role: 'student',
        username: email.split('@')[0],
        userType: 'student'
      };
      setUser(mockUser);
    } catch (error: unknown) {
      const errorMessage = error instanceof Error 
        ? error.message 
        : 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name: string;
    last_name: string;
    user_type: 'student' | 'teacher' | 'staff' | 'admin';
  }) => {
    setLoading(true);
    setError(null);
    try {
      console.log('Simple register attempt:', userData);
      // Mock successful registration
      const mockUser: User = {
        id: '1',
        email: userData.email,
        firstName: userData.first_name,
        lastName: userData.last_name,
        role: userData.user_type,
        username: userData.username,
        userType: userData.user_type
      };
      setUser(mockUser);
    } catch (error: unknown) {
      const errorMessage = error instanceof Error 
        ? error.message 
        : 'Registration failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    console.log('Simple logout');
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    loading,
    error
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
