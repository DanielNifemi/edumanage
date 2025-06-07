import React, { FC } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '@/contexts/useAuth'; // Corrected import path
import DashboardLayout from '../layout/DashboardLayout'; // Import DashboardLayout

const ProtectedRoute: FC = () => {
  const { isAuthenticated, loading } = useAuth(); // Changed isLoading to loading

  if (loading) { // Changed isLoading to loading
    // You can return a loading spinner here if you have one
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  );
};

export default ProtectedRoute;
