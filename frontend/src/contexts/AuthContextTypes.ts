import { createContext } from 'react';

export interface UserProfileData {
  user_type: 'student' | 'teacher' | 'admin' | 'staff';
  created_at: string;
  updated_at: string;
  student_id?: string;
  admission_date?: string;
  teacher_id?: string;
  join_date?: string;
  subjects_count?: number;
  staff_id?: string;
  // department?: string; // This was commented out, ensure it's correct based on backend
  phone_number?: string; // Added based on ProfilePage usage
  profile_image_url?: string; // Added for profile image
}

export interface User {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  role: 'student' | 'teacher' | 'admin' | 'staff'; // Changed from userType
  is_active?: boolean;
  is_staff?: boolean;
  date_joined?: string;
  last_login?: string;
  profile_data?: UserProfileData;
  phone_number?: string; // Added based on ProfilePage usage, ensure it's part of user object or profile_data
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  user_type: 'student' | 'teacher' | 'staff' | 'admin';
  // Optional fields, align with your backend RegisterSerializer
  student_id?: string;
  employee_id?: string;
  department?: string;
  admin_code?: string;
}

// Added export
export interface Announcement {
  id: string;
  title: string;
  content: string;
  author: string; // Assuming author is a user ID
  author_details?: { // Optional: To store more author info if needed by frontend
    id: string;
    username: string;
    first_name?: string;
    last_name?: string;
  };
  created_at: string;
  updated_at: string;
  published_at?: string | null;
  is_published: boolean;
  // Add any other relevant fields from your backend model
}

// Added export
export interface Notification {
  id: string;
  recipient: string; // User ID
  sender?: string | null; // User ID or system
  sender_details?: { // Optional: To store more sender info
    id: string;
    username: string;
    first_name?: string;
    last_name?: string;
  };
  message: string;
  notification_type: string; // e.g., 'new_assignment', 'announcement', 'grade_update'
  is_read: boolean;
  created_at: string;
  // Add any other relevant fields from your backend model
  path?: string; // Optional path to navigate to when notification is clicked
  related_object_id?: string | number | null; // Optional ID of related object (e.g., assignment ID)
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  loading: boolean;
  error: string | null;
  unreadNotificationsCount: number; // Added
  refreshUnreadCount: () => Promise<void>; // Added
  refreshUserData: () => Promise<void>; // Added to refresh user data
}

export const AuthContext = createContext<AuthContextType | null>(null);
