import axios from 'axios';

// TypeScript interfaces for API data
export interface StudentData {
  id?: string;
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  user_type?: 'student';
  student_id?: string;
  grade_level?: string;
  enrollment_date?: string;
  date_of_birth?: string;
  grade?: string;
  address?: string;
  parent_name?: string;
  parent_contact?: string;
  // Legacy field names for backward compatibility
  phone_number?: string;
  parent_guardian?: string;
  emergency_contact?: string;
}

export interface TeacherData {
  id?: string;
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  user_type?: 'teacher';
  employee_id?: string;
  department?: string;
  subjects?: string[];
  hire_date?: string;
}

export interface CourseData {
  id?: string;
  title?: string;
  description?: string;
  subject_id?: string;
  instructor_id?: string;
  difficulty_level?: 'beginner' | 'intermediate' | 'advanced';
  status?: 'draft' | 'published' | 'archived';
  start_date?: string;
  end_date?: string;
  max_students?: number;
  credits?: number;
  thumbnail?: string;
}

export interface AttendanceData {
  student_id: string;
  course_id: string;
  date: string;
  status: 'present' | 'absent' | 'late' | 'excused';
  notes?: string;
}

export interface MessageData {
  recipient_id?: string;
  recipient_type?: 'student' | 'teacher' | 'admin' | 'staff';
  subject?: string;
  content?: string;
  priority?: 'low' | 'normal' | 'high' | 'urgent';
}

export interface AssignmentData {
  id?: string;
  content_id?: string;
  title?: string;
  description?: string;
  course_id?: string;
  course_title?: string;
  due_date?: string;
  total_points?: number;
  submission_type?: 'file' | 'text' | 'url' | 'multiple';
  instructions?: string;
  allow_late_submission?: boolean;
  late_penalty_per_day?: number;
  is_overdue?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface AssignmentSubmissionData {
  id?: string;
  assignment_id?: string;
  assignment_title?: string;
  student_id?: string;
  student_name?: string;
  submitted_file?: File;
  submitted_text?: string;
  submitted_url?: string;
  submitted_at?: string;
  grade?: number;
  feedback?: string;
  graded_by?: string;
  graded_at?: string;
  is_late?: boolean;
  is_graded?: boolean;
}

export interface UserProfileUpdateData {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone_number?: string;
}

const API_BASE_URL = 'http://localhost:8000/api'; // Adjusted to match backend DRF routes

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('edumanage_token');
    if (token) {
      // config.headers.Authorization = `Token ${token}`; // Changed to 'Token' based on typical Django REST framework token auth
      config.headers.Authorization = `Bearer ${token}`; // Reverted to Bearer token based on JWT usage
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth data on unauthorized
      localStorage.removeItem('edumanage_token');
      localStorage.removeItem('edumanage_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: async (email: string, password: string) => {
    // const response = await api.post(\'/auth/login/\', { email, password });
    const response = await api.post('/auth/login/', { email, password }); // Adjusted path
    return response.data;
  },

  register: async (userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name: string;
    last_name: string;
    user_type: 'student' | 'teacher' | 'staff' | 'admin';
  }) => {
    // const response = await api.post(\'/auth/register/\', userData);
    const response = await api.post('/auth/register/', userData); // Adjusted path
    return response.data;
  },

  getProfile: async () => {
    // const response = await api.get(\'/auth/profile/\');
    const response = await api.get('/auth/user/'); // Adjusted path to /api/accounts/user/
    return response.data;
  },

  logout: async () => {
    // const response = await api.post(\'/auth/logout/\');
    const response = await api.post('/auth/logout/'); // Adjusted path
    return response.data;
  },

  // Assuming these paths also need to be relative to /api/accounts/
  forgotPassword: async (email: string) => {
    // const response = await api.post(\'/auth/forgot-password/\', { email });
    const response = await api.post('/auth/forgot-password/', { email }); // Adjusted path
    return response.data;
  },

  resetPassword: async (token: string, password: string) => {
    // const response = await api.post(\'/auth/reset-password/\', { token, password });
    const response = await api.post('/auth/reset-password/', { token, password }); // Adjusted path
    return response.data;
  },

  verifyEmail: async (token: string) => {
    // const response = await api.post(\'/auth/verify-email/\', { token });
    const response = await api.post('/auth/verify-email/', { token }); // Adjusted path
    return response.data;
  },

  updateProfile: async (userId: string, data: UserProfileUpdateData) => {
    const response = await api.patch(`/auth/users/${userId}/`, data); // Using PATCH for partial updates
    return response.data;
  },
};

// Students API
export const studentsAPI = {
  getAll: async () => {
    const response = await api.get('/students/');
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/students/${id}/`);
    return response.data;
  },
  create: async (studentData: StudentData) => {
    const response = await api.post('/students/', studentData);
    return response.data;
  },

  update: async (id: string, studentData: StudentData) => {
    const response = await api.put(`/students/${id}/`, studentData);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/students/${id}/`);
    return response.data;
  },
};

// Teachers API
export const teachersAPI = {
  getAll: async () => {
    const response = await api.get('/teachers/');
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/teachers/${id}/`);
    return response.data;
  },
  create: async (teacherData: TeacherData) => {
    const response = await api.post('/teachers/', teacherData);
    return response.data;
  },

  update: async (id: string, teacherData: TeacherData) => {
    const response = await api.put(`/teachers/${id}/`, teacherData);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/teachers/${id}/`);
    return response.data;
  },
};

// Courses API
export const coursesAPI = {
  getAll: async () => {
    const response = await api.get('/courses/');
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/courses/${id}/`);
    return response.data;
  },
  create: async (courseData: CourseData) => {
    const response = await api.post('/courses/', courseData);
    return response.data;
  },

  update: async (id: string, courseData: CourseData) => {
    const response = await api.put(`/courses/${id}/`, courseData);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/courses/${id}/`);
    return response.data;
  },
};

// Attendance API
export const attendanceAPI = {
  getStudentAttendance: async (studentId: string) => {
    const response = await api.get(`/attendance/student/${studentId}/`);
    return response.data;
  },

  getClassAttendance: async (classId: string, date?: string) => {
    const params = date ? { date } : {};
    const response = await api.get(`/attendance/class/${classId}/`, { params });
    return response.data;
  },
  markAttendance: async (attendanceData: AttendanceData) => {
    const response = await api.post('/attendance/', attendanceData);
    return response.data;
  },
};

// Schedules API
export const schedulesAPI = {
  getByUser: async (userType: string, userId: string) => {
    const response = await api.get(`/schedules/${userType}/${userId}/`);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/schedules/');
    return response.data;
  },
};

// Communication API
export const communicationAPI = {
  getMessages: async () => {
    const response = await api.get('/communication/messages/');
    return response.data;
  },
  sendMessage: async (messageData: MessageData) => {
    const response = await api.post('/communication/messages/', messageData);
    return response.data;
  },

  getAnnouncements: async () => {
    const response = await api.get('/communication/announcements/');
    return response.data;
  },
};

// Assignments API
export const assignmentsAPI = {
  getAll: async () => {
    const response = await api.get('/courses/assignments/'); // Corrected path
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/courses/assignments/${id}/`); // Corrected path
    return response.data;
  },

  create: async (assignmentData: AssignmentData) => {
    const response = await api.post('/courses/assignments/', assignmentData); // Corrected path
    return response.data;
  },

  update: async (id: string, assignmentData: Partial<AssignmentData>) => {
    const response = await api.put(`/courses/assignments/${id}/`, assignmentData); // Corrected path
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/courses/assignments/${id}/`); // Corrected path
    return response.data;
  },

  getSubmissions: async (assignmentId: string) => {
    const response = await api.get(`/courses/assignments/${assignmentId}/submissions/`); // Corrected path
    return response.data;
  },

  submitAssignment: async (assignmentId: string, submissionData: FormData) => {
    const response = await api.post(`/courses/assignments/${assignmentId}/submit/`, submissionData, { // Corrected path
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  gradeSubmission: async (submissionId: string, gradeData: { grade: number; feedback?: string }) => {
    const response = await api.put(`/courses/submissions/${submissionId}/grade/`, gradeData); // Corrected path
    return response.data;
  },

  getStudentAssignments: async (studentId: string) => {
    const response = await api.get(`/students/${studentId}/assignments/`);
    return response.data;
  },

  getTeacherAssignments: async (teacherId: string) => {
    const response = await api.get(`/teachers/${teacherId}/assignments/`);
    return response.data;
  },
};

// Notifications API calls
export const notificationsAPI = {
  getAll: async () => {
    const response = await api.get(`/communication/notifications/`);
    return response.data;
  },
  markAsRead: async (notificationId: number) => {
    const response = await api.post(
      `/communication/notifications/${notificationId}/mark-as-read/`
    );
    return response.data;
  },
  markAllAsRead: async () => {
    const response = await api.post(
      `/communication/notifications/mark-all-as-read/`
    );
    return response.data;
  },
  getUnreadCount: async () => {
    const response = await api.get(
      `/communication/notifications/unread-count/`
    );
    return response.data;
  }
};

// Announcements API calls
export const announcementsAPI = {
  getAll: async () => {
    const response = await api.get(`/communication/announcements/`);
    return response.data;
  },
  getOne: async (announcementId: number) => {
    const response = await api.get(
      `/communication/announcements/${announcementId}/`
    );
    return response.data;
  },
  create: async (data: { title: string; content: string; is_published?: boolean }) => {
    const response = await api.post(`/communication/announcements/`, data);
    return response.data;
  },
  update: async (announcementId: number, data: Partial<{ title: string; content: string; is_published?: boolean }>) => {
    const response = await api.patch(
      `/communication/announcements/${announcementId}/`,
      data
    );
    return response.data;
  },
  delete: async (announcementId: number) => {
    const response = await api.delete(
      `/communication/announcements/${announcementId}/`
    );
    return response.data;
  },
  publish: async (announcementId: number) => {
    const response = await api.post(
      `/communication/announcements/${announcementId}/publish/`
    );
    return response.data;
  },
  unpublish: async (announcementId: number) => {
    const response = await api.post(
      `/communication/announcements/${announcementId}/unpublish/`
    );
    return response.data;
  },
};

export default api;
