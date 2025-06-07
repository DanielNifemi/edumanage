import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '@/lib/api';

interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'student' | 'teacher' | 'admin' | 'staff';
  avatar?: string;
  username?: string;
  userType?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name: string;
    last_name: string;
    user_type: 'student' | 'teacher' | 'staff' | 'admin';
  }) => Promise<void>;
  logout: () => void;
  loading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check for existing authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('edumanage_token');
        if (token) {
          const profileData = await authAPI.getProfile();
          if (profileData && profileData.user && profileData.authenticated) {
            const userData = profileData.user;
            setUser({
              id: userData.id?.toString() || '',
              email: userData.email || '',
              firstName: userData.first_name || '',
              lastName: userData.last_name || '',
              role: userData.user_type || 'student',
              username: userData.username || '',
              userType: userData.user_type || '',
              avatar: userData.first_name && userData.last_name 
                ? `https://ui-avatars.com/api/?name=${userData.first_name}+${userData.last_name}&background=0369a1&color=fff`
                : undefined
            });
          } else {
            // Clear invalid token
            localStorage.removeItem('edumanage_token');
            localStorage.removeItem('edumanage_user');
          }
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('edumanage_token');
        localStorage.removeItem('edumanage_user');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authAPI.login(email, password);
      
      if (response.access) {
        localStorage.setItem('edumanage_token', response.access);
        
        // Get user profile after login
        const profileData = await authAPI.getProfile();
        if (profileData && profileData.user) {
          const userData = profileData.user;
          const userObj: User = {
            id: userData.id?.toString() || '',
            email: userData.email || '',
            firstName: userData.first_name || '',
            lastName: userData.last_name || '',
            role: userData.user_type || 'student',
            username: userData.username || '',
            userType: userData.user_type || '',
            avatar: userData.first_name && userData.last_name 
              ? `https://ui-avatars.com/api/?name=${userData.first_name}+${userData.last_name}&background=0369a1&color=fff`
              : undefined
          };
          
          localStorage.setItem('edumanage_user', JSON.stringify(userObj));
          setUser(userObj);
        }
      } else {
        throw new Error('Login failed - no access token received');
      }
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
      const response = await authAPI.register(userData);
      
      if (response.user) {
        // Auto-login after successful registration
        await login(userData.email, userData.password);
      }
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
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('edumanage_token');
      localStorage.removeItem('edumanage_user');
      setUser(null);
    }
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
