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

export interface UserProfileData {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  date_joined?: string;
  last_login?: string;
  is_active?: boolean;
  is_staff?: boolean;
  is_superuser?: boolean;
  user_permissions?: string[];
  groups?: string[];
}

export interface UserBasicData {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
  full_name?: string; // Often constructed like `first_name + ' ' + last_name` or provided by backend
  email?: string; // Optional: if needed for display or contact
  // avatar_url?: string; // Optional: if you have avatars for users
}

// Added SentMessageData interface
export interface SentMessageData {
  recipient_id: number; // ID of the user receiving the message
  subject: string;
  body: string; // Content of the message
}

// Added ReceivedMessageData interface
export interface ReceivedMessageData {
  id: number | string; // Unique ID of the message
  sender?: UserBasicData; // Information about the sender
  recipient?: UserBasicData; // Information about the recipient
  subject: string;
  body: string; // Content of the message
  created_at: string; // Timestamp of when the message was created (ISO 8601 format)
  is_read: boolean;
  // Fallback fields if sender/recipient objects are not fully populated or available
  sender_name?: string; 
  recipient_name?: string;
}

// Examination/Assessment related interfaces
export interface ExamData {
  id?: number;
  title: string;
  description?: string;
  course: number;
  course_title?: string;
  total_marks: number;
  passing_marks: number;
  duration: number; // in minutes
  exam_date: string;
  start_time: string;
  end_time: string;
  is_published: boolean;
  instructions?: string;
  created_by?: number;
  created_by_name?: string;
  created_at?: string;
  updated_at?: string;
}

export interface TestData {
  id?: number;
  title: string;
  description?: string;
  course: number;
  course_title?: string;
  total_marks: number;
  passing_marks: number;
  duration: number; // in minutes
  max_attempts: number;
  is_published: boolean;
  instructions?: string;
  created_by?: number;
  created_by_name?: string;
  created_at?: string;
  updated_at?: string;
}

export interface QuestionData {
  id?: number;
  test: number;
  question_text: string;
  question_type: 'multiple_choice' | 'true_false' | 'short_answer' | 'essay';
  marks: number;
  order: number;
  is_required: boolean;
}

export interface AnswerData {
  id?: number;
  question: number;
  answer_text: string;
  is_correct: boolean;
  order: number;
}

export interface TestAttemptData {
  id?: number;
  test: number;
  test_title?: string;
  student: number;
  student_name?: string;
  start_time: string;
  end_time?: string;
  score?: number;
  is_submitted: boolean;
  attempt_number: number;
  created_at?: string;
}

export interface StudentAnswerData {
  id?: number;
  test_attempt: number;
  question: number;
  answer_text?: string;
  selected_answer?: number;
  marks_awarded?: number;
}

export interface ExamResultData {
  id?: number;
  exam: number;
  exam_title?: string;
  student: number;
  student_name?: string;
  marks_obtained: number;
  percentage: number;
  grade?: string;
  is_passed: boolean;
  exam_date: string;
  graded_by?: number;
  graded_by_name?: string;
  feedback?: string;
  created_at?: string;
}

const API_BASE_URL = 'http://localhost:8000/api'; // Adjusted to match backend DRF routes

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for cookies, including CSRF
});

// Add a request interceptor to include the CSRF token
api.interceptors.request.use(
  (config) => {
    // Function to get CSRF token from cookies
    function getCookie(name: string): string | null {
      let cookieValue: string | null = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            try {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            } catch (e) {
              console.error(`Error decoding cookie "${name}":`, e);
              // If decoding fails, ensure cookieValue is null to prevent using a malformed token.
              cookieValue = null;
            }
            break;
          }
        }
      }
      return cookieValue;
    }

    if (config.method && ['post', 'put', 'delete', 'patch'].includes(config.method.toLowerCase())) {
      const csrfToken = getCookie('csrftoken');
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }
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
    const response = await api.post('/auth/login/', { email, password });
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
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/user/');
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout/');
    return response.data;
  },

  forgotPassword: async (email: string) => {
    const response = await api.post('/auth/forgot-password/', { email });
    return response.data;
  },

  resetPassword: async (token: string, password: string) => {
    const response = await api.post('/auth/reset-password/', { token, password });
    return response.data;
  },

  verifyEmail: async (token: string) => {
    const response = await api.post('/auth/verify-email/', { token });
    return response.data;
  },

  updateProfile: async (userId: string, data: UserProfileUpdateData) => {
    const response = await api.patch(`/auth/users/${userId}/`, data);
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
    // Use the correct backend endpoints 
    if (userType === 'teacher') {
      const response = await api.get(`/schedules/schedules/by-teacher/?teacher_id=${userId}`);
      return response.data;
    } else if (userType === 'student') {
      const response = await api.get(`/schedules/schedules/by-class/?class_id=${userId}`);
      return response.data;
    } else {
      // For general users, get all schedules
      const response = await api.get('/schedules/schedules/');
      return response.data;
    }
  },

  getAll: async () => {
    const response = await api.get('/schedules/schedules/');
    return response.data;
  },
};

// Communication API
export const communicationAPI = {
  getMessages: async (): Promise<ReceivedMessageData[]> => { // Ensure getMessages returns an array of ReceivedMessageData
    const response = await api.get<ReceivedMessageData[]>('/communication/messages/');
    return response.data;
  },
  getInboxMessages: async (): Promise<ReceivedMessageData[]> => {
    const response = await api.get<ReceivedMessageData[]>('/communication/messages/inbox/');
    return response.data;
  },
  getSentMessages: async (): Promise<ReceivedMessageData[]> => {
    const response = await api.get<ReceivedMessageData[]>('/communication/messages/sent/');
    return response.data;
  },
  sendMessage: async (messageData: MessageData) => {
    const response = await api.post('/communication/messages/', messageData);
    return response.data;
  },

  createMessage: async (messageData: SentMessageData): Promise<ReceivedMessageData> => {
    const response = await api.post<ReceivedMessageData>('/communication/messages/', messageData);
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

// Accounts API - Add getUsers if it's not already present or correctly defined
export const accountsAPI = {
  getUsers: async (): Promise<UserBasicData[]> => {
    const response = await api.get<UserBasicData[]>('/auth/users/');
    return response.data;
  },
  // ... any other existing accountsAPI methods
};

// Examinations API calls
export const examinationsAPI = {
  // Exams
  getExams: async () => {
    const response = await api.get('/examinations/exams/');
    return response.data;
  },
  getExam: async (examId: number) => {
    const response = await api.get(`/examinations/exams/${examId}/`);
    return response.data;
  },
  createExam: async (data: ExamData) => {
    const response = await api.post('/examinations/exams/', data);
    return response.data;
  },
  updateExam: async (examId: number, data: Partial<ExamData>) => {
    const response = await api.patch(`/examinations/exams/${examId}/`, data);
    return response.data;
  },
  deleteExam: async (examId: number) => {
    const response = await api.delete(`/examinations/exams/${examId}/`);
    return response.data;
  },
  publishExam: async (examId: number) => {
    const response = await api.post(`/examinations/exams/${examId}/publish/`);
    return response.data;
  },

  // Tests
  getTests: async () => {
    const response = await api.get('/examinations/tests/');
    return response.data;
  },
  getTest: async (testId: number) => {
    const response = await api.get(`/examinations/tests/${testId}/`);
    return response.data;
  },
  createTest: async (data: TestData) => {
    const response = await api.post('/examinations/tests/', data);
    return response.data;
  },
  updateTest: async (testId: number, data: Partial<TestData>) => {
    const response = await api.patch(`/examinations/tests/${testId}/`, data);
    return response.data;
  },
  deleteTest: async (testId: number) => {
    const response = await api.delete(`/examinations/tests/${testId}/`);
    return response.data;
  },
  publishTest: async (testId: number) => {
    const response = await api.post(`/examinations/tests/${testId}/publish/`);
    return response.data;
  },

  // Questions
  getQuestions: async (testId?: number) => {
    const url = testId ? `/examinations/questions/?test=${testId}` : '/examinations/questions/';
    const response = await api.get(url);
    return response.data;
  },
  getQuestion: async (questionId: number) => {
    const response = await api.get(`/examinations/questions/${questionId}/`);
    return response.data;
  },
  createQuestion: async (data: QuestionData) => {
    const response = await api.post('/examinations/questions/', data);
    return response.data;
  },
  updateQuestion: async (questionId: number, data: Partial<QuestionData>) => {
    const response = await api.patch(`/examinations/questions/${questionId}/`, data);
    return response.data;
  },
  deleteQuestion: async (questionId: number) => {
    const response = await api.delete(`/examinations/questions/${questionId}/`);
    return response.data;
  },

  // Answers
  getAnswers: async (questionId?: number) => {
    const url = questionId ? `/examinations/answers/?question=${questionId}` : '/examinations/answers/';
    const response = await api.get(url);
    return response.data;
  },
  createAnswer: async (data: AnswerData) => {
    const response = await api.post('/examinations/answers/', data);
    return response.data;
  },
  updateAnswer: async (answerId: number, data: Partial<AnswerData>) => {
    const response = await api.patch(`/examinations/answers/${answerId}/`, data);
    return response.data;
  },
  deleteAnswer: async (answerId: number) => {
    const response = await api.delete(`/examinations/answers/${answerId}/`);
    return response.data;
  },

  // Test Attempts
  getTestAttempts: async (testId?: number, studentId?: number) => {
    let url = '/examinations/test-attempts/';
    const params: string[] = [];
    if (testId) params.push(`test=${testId}`);
    if (studentId) params.push(`student=${studentId}`);
    if (params.length > 0) {
      url += `?${params.join('&')}`;
    }
    const response = await api.get(url);
    return response.data;
  },
  getTestAttempt: async (attemptId: number) => {
    const response = await api.get(`/examinations/test-attempts/${attemptId}/`);
    return response.data;
  },
  createTestAttempt: async (data: Partial<TestAttemptData>) => {
    const response = await api.post('/examinations/test-attempts/', data);
    return response.data;
  },
  updateTestAttempt: async (attemptId: number, data: Partial<TestAttemptData>) => {
    const response = await api.patch(`/examinations/test-attempts/${attemptId}/`, data);
    return response.data;
  },
  submitTestAttempt: async (attemptId: number) => {
    const response = await api.post(`/examinations/test-attempts/${attemptId}/submit/`);
    return response.data;
  },

  // Exam Results
  getExamResults: async (examId?: number, studentId?: number) => {
    let url = '/examinations/exam-results/';
    const params: string[] = [];
    if (examId) params.push(`exam=${examId}`);
    if (studentId) params.push(`student=${studentId}`);
    if (params.length > 0) {
      url += `?${params.join('&')}`;
    }
    const response = await api.get(url);
    return response.data;
  },
  getExamResult: async (resultId: number) => {
    const response = await api.get(`/examinations/exam-results/${resultId}/`);
    return response.data;
  },
  createExamResult: async (data: ExamResultData) => {
    const response = await api.post('/examinations/exam-results/', data);
    return response.data;
  },
  updateExamResult: async (resultId: number, data: Partial<ExamResultData>) => {
    const response = await api.patch(`/examinations/exam-results/${resultId}/`, data);
    return response.data;
  },
  deleteExamResult: async (resultId: number) => {
    const response = await api.delete(`/examinations/exam-results/${resultId}/`);
    return response.data;
  },

  // Student Answers (for grading)
  getStudentAnswers: async (attemptId: number) => {
    const response = await api.get(`/examinations/student-answers/?test_attempt=${attemptId}`);
    return response.data;
  },
  updateStudentAnswer: async (answerId: number, data: Partial<StudentAnswerData>) => {
    const response = await api.patch(`/examinations/student-answers/${answerId}/`, data);
    return response.data;
  },

  // Additional helper functions
  getAssessmentStats: async (assessmentType: 'exams' | 'tests', assessmentId: number) => {
    const response = await api.get(`/examinations/${assessmentType}/${assessmentId}/stats/`);
    return response.data;
  },
};

export default api;
