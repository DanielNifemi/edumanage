import React, { useState, useEffect, useCallback } from 'react'; // Removed useContext
import { authAPI, notificationsAPI } from '@/lib/api'; // Added notificationsAPI
import { AuthContext, User, AuthContextType, RegisterData } from './AuthContextTypes';

// Define a more specific type for Axios errors
interface AxiosError extends Error {
  isAxiosError: boolean;
  response?: {
    data?: Record<string, unknown> | string; // Changed any to Record<string, unknown> | string
    status?: number;
    headers?: Record<string, string>; // Changed any to Record<string, string>
  };
}

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [unreadNotificationsCount, setUnreadNotificationsCount] = useState(0);

  // Forward declare logout to satisfy useCallback dependency for refreshUserData
  const logout = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      localStorage.removeItem('edumanage_token');
      setUser(null);
      setUnreadNotificationsCount(0);
      setLoading(false);
    }
  }, []); // No dependencies as it only uses setters and localStorage

  const refreshUserData = useCallback(async () => {
    if (!user) return;
    try {
      const profileData = await authAPI.getProfile();
      if (profileData && profileData.user) {
        const userDataFromProfile = profileData.user;
        const userObj: User = {
          id: userDataFromProfile.id?.toString() || '',
          email: userDataFromProfile.email || '',
          first_name: userDataFromProfile.first_name || '',
          last_name: userDataFromProfile.last_name || '',
          role: userDataFromProfile.role || 'student',
          username: userDataFromProfile.username || '',
          profile_data: userDataFromProfile.profile_data,
        };
        setUser(userObj);
      } else {
        console.warn('Failed to refresh user data, logging out.');
        await logout(); // Call the memoized logout
      }
    } catch (err) {
      console.error('Failed to refresh user data:', err);
      // await logout(); // Optionally call logout here too
    }
  }, [user, logout]); // Added logout to dependencies

  const refreshUnreadCount = useCallback(async () => {
    if (user) {
      try {
        const response = await notificationsAPI.getUnreadCount();
        if (typeof response.unread_count === 'number') {
          setUnreadNotificationsCount(response.unread_count);
        }
      } catch (err) {
        console.error('Failed to fetch unread notifications count in AuthContext:', err);
      }
    }
  }, [user]);

  useEffect(() => {
    if (user) {
      refreshUnreadCount();
      const intervalId = setInterval(refreshUnreadCount, 60000);
      return () => clearInterval(intervalId);
    }
  }, [user, refreshUnreadCount]);

  useEffect(() => {
    const checkAuth = async () => {
      setLoading(true); // Ensure loading is true at the start of auth check
      try {
        const token = localStorage.getItem('edumanage_token');
        if (token) {
          try {
            // Fetch profile first to ensure token is valid and to get user data
            const profileData = await authAPI.getProfile();
            if (profileData && profileData.user && profileData.authenticated) {
              const userDataFromProfile = profileData.user; // Use a different name to avoid confusion
              const userObj: User = {
                id: userDataFromProfile.id?.toString() || '',
                email: userDataFromProfile.email || '',
                // Ensure first_name and last_name are part of the profileData.user structure
                first_name: userDataFromProfile.first_name || '', 
                last_name: userDataFromProfile.last_name || '',
                role: userDataFromProfile.role || 'student',
                username: userDataFromProfile.username || '',
                profile_data: userDataFromProfile.profile_data, // Store full profile_data
                // avatar is removed, profile_image_url will be in profile_data
              };
              setUser(userObj);
              // Fetch unread count after user is set
              // This will be handled by the other useEffect that depends on `user`
            } else {
              localStorage.removeItem('edumanage_token');
              // localStorage.removeItem('edumanage_user'); // No longer storing user separately
              setUser(null); // Explicitly set user to null
            }
          } catch (apiError) {
            console.warn('Profile API call failed during initial auth check, clearing auth data:', apiError);
            localStorage.removeItem('edumanage_token');
            // localStorage.removeItem('edumanage_user');
            setUser(null);
          }
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('edumanage_token');
        // localStorage.removeItem('edumanage_user');
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []); // Empty dependency array: runs once on mount

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authAPI.login(email, password);
      if (response && response.access) {
        localStorage.setItem('edumanage_token', response.access);
        const profileData = await authAPI.getProfile();
        if (profileData && profileData.user) {
          const userDataFromProfile = profileData.user;
          const userObj: User = {
            id: userDataFromProfile.id?.toString() || '',
            email: userDataFromProfile.email || '',
            first_name: userDataFromProfile.first_name || '',
            last_name: userDataFromProfile.last_name || '',
            role: userDataFromProfile.role || 'student',
            username: userDataFromProfile.username || '',
            profile_data: userDataFromProfile.profile_data,
          };
          setUser(userObj);
          // refreshUnreadCount will be called by the useEffect hook watching `user`
        } else {
          throw new Error('Login successful, but failed to retrieve user profile.');
        }
      } else {
        throw new Error('Login failed - no access token received');
      }
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed';
      setError(errorMessage);
      localStorage.removeItem('edumanage_token'); // Clear token on login failure
      setUser(null); // Clear user on login failure
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: RegisterData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authAPI.register(userData);
      if (response.user) {
        await login(userData.email, userData.password);
      } else {
        // Handle cases where registration might succeed but not return a user object directly
        // or if an intermediate step is needed (e.g. email verification before login)
        throw new Error(response.message || 'Registration completed, but auto-login failed. Please try logging in.');
      }
    } catch (error: unknown) {
      let errorMessage = 'Registration failed';
      const typedError = error as AxiosError;
      if (typedError.isAxiosError && typedError.response && typedError.response.data) {
        const backendErrors = typedError.response.data;
        if (typeof backendErrors === 'string') {
          errorMessage = backendErrors;
        } else if (typeof backendErrors === 'object' && backendErrors !== null) {
          errorMessage = Object.entries(backendErrors)
            .map(([key, value]) => {
              const messages = Array.isArray(value) ? value.join(', ') : String(value);
              return `${key}: ${messages}`;
            })
            .join('; ');
        }
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        register,
        logout, // Use the memoized logout
        loading,
        error,
        unreadNotificationsCount,
        refreshUnreadCount,
        refreshUserData,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// REMOVED useAuth hook from here, it's now in its own file: src/contexts/useAuth.ts
