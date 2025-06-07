import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import ForgotPassword from "./pages/auth/ForgotPassword";
import ResetPassword from "./pages/auth/ResetPassword";
import EmailVerification from "./pages/auth/EmailVerification";

import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import { AuthProvider } from "./contexts/AuthContext"; // Added AuthProvider import

// Dashboard components (Placeholder imports - create these components as needed)
const StudentDashboard = () => <div>Student Dashboard</div>; // Placeholder
const TeacherDashboard = () => <div>Teacher Dashboard</div>; // Placeholder
const AdminDashboard = () => <div>Admin Dashboard</div>;   // Placeholder
const StaffDashboard = () => <div>Staff Dashboard</div>;   // Placeholder

// Page components (Placeholder imports - create these components as needed)
const UsersList = () => <div>Users List</div>;             // Placeholder
const AdminReports = () => <div>Admin Reports</div>;         // Placeholder
const AdminSettings = () => <div>Admin Settings</div>;       // Placeholder
const TeacherClasses = () => <div>Teacher Classes</div>;       // Placeholder
const TeacherAssignments = () => <div>Teacher Assignments</div>; // Placeholder
const TeacherAttendance = () => <div>Teacher Attendance</div>;   // Placeholder
const StaffReports = () => <div>Staff Reports</div>;         // Placeholder
const StudentsList = () => <div>Students List</div>;         // Placeholder
const Attendance = () => <div>Attendance Page</div>;         // Placeholder
const TeachersList = () => <div>Teachers List</div>;         // Placeholder
const CourseDetails = () => <div>Course Details</div>;       // Placeholder


import Assignments from "./pages/assignments/Assignments";
import ProfilePage from "./pages/ProfilePage";
import NotificationsPage from './pages/NotificationsPage';
import AnnouncementsPage from './pages/AnnouncementsPage';
import CoursesPage from './pages/CoursesPage'; // Added import
import SchedulePage from './pages/SchedulePage'; // Added import
import MessagesPage from './pages/MessagesPage'; // Added import
import SettingsPage from './pages/SettingsPage'; // Added import

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password/:token" element={<ResetPassword />} />
            <Route path="/verify-email/:token" element={<EmailVerification />} />
            
            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              {/* Dashboard Routes */}
              <Route path="/student/dashboard" element={<StudentDashboard />} />
              <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
              <Route path="/admin/dashboard" element={<AdminDashboard />} />
              <Route path="/staff/dashboard" element={<StaffDashboard />} />
            
              {/* Profile, Notifications, Announcements */}
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/notifications" element={<NotificationsPage />} />
              <Route path="/announcements" element={<AnnouncementsPage />} />
            
              {/* Admin Routes */}
              <Route path="/admin/users" element={<UsersList />} />
              <Route path="/admin/reports" element={<AdminReports />} />
              <Route path="/admin/settings" element={<AdminSettings />} />
            
              {/* Teacher Routes */}
              <Route path="/teacher/classes" element={<TeacherClasses />} />
              <Route path="/teacher/assignments" element={<TeacherAssignments />} />
              <Route path="/teacher/attendance" element={<TeacherAttendance />} />
            
              {/* Staff Routes */}
              <Route path="/staff/reports" element={<StaffReports />} />
            
              {/* Student Routes */}
              <Route path="/student/assignments" element={<Assignments />} />
              <Route path="/student/attendance" element={<Attendance />} />
            
              {/* Teacher Management Routes */}
              <Route path="/teachers" element={<TeachersList />} />
            
              {/* Schedule Routes */}
              <Route path="/schedule" element={<SchedulePage />} /> 
            
              {/* Communication Routes */}
              <Route path="/messages" element={<MessagesPage />} />
            
              {/* Settings Route */}
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
            
            {/* Publicly accessible lists (if any) - adjust protection as needed */}
            <Route path="/students" element={<StudentsList />} /> 
            <Route path="/courses" element={<CoursesPage />} /> 
            <Route path="/courses/:id" element={<CourseDetails />} />
            
            {/* Catch-all route */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
