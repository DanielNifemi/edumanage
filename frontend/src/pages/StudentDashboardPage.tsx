
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { BookOpen, CheckCircle, CalendarDays, ClipboardList, TrendingUp, AlertCircle, Clock } from 'lucide-react';

// Mock Data Interfaces
interface StudentCourse {
  id: string;
  title: string;
  instructor: string;
  progress: number; // percentage
}

interface StudentAssignment {
  id: string;
  title: string;
  course: string;
  dueDate: string;
  status: 'Pending' | 'Submitted' | 'Overdue';
}

interface StudentExam {
  id: string;
  course: string;
  date: string;
  time: string;
}

// Mock Data
const mockCourses: StudentCourse[] = [
  { id: '1', title: 'Introduction to Programming', instructor: 'Dr. Smith', progress: 75 },
  { id: '2', title: 'Calculus I', instructor: 'Prof. Jones', progress: 50 },
  { id: '3', title: 'World History', instructor: 'Ms. Davis', progress: 90 },
];

const mockAssignments: StudentAssignment[] = [
  { id: 'a1', title: 'Essay 1', course: 'World History', dueDate: '2025-06-15', status: 'Pending' },
  { id: 'a2', title: 'Lab Report 2', course: 'Intro to Programming', dueDate: '2025-06-18', status: 'Pending' },
  { id: 'a3', title: 'Problem Set 3', course: 'Calculus I', dueDate: '2025-06-10', status: 'Overdue' },
  { id: 'a4', title: 'Quiz 4', course: 'Calculus I', dueDate: '2025-06-20', status: 'Submitted' },
];

const mockExams: StudentExam[] = [
  { id: 'e1', course: 'Calculus I', date: '2025-06-25', time: '10:00 AM' },
  { id: 'e2', course: 'Introduction to Programming', date: '2025-06-28', time: '02:00 PM' },
];

const StudentDashboardPage: React.FC = () => {
  const getStatusColor = (status: StudentAssignment['status']) => {
    if (status === 'Pending') return 'bg-yellow-500 hover:bg-yellow-600';
    if (status === 'Submitted') return 'bg-green-500 hover:bg-green-600';
    if (status === 'Overdue') return 'bg-red-500 hover:bg-red-600';
    return 'bg-gray-500';
  };

  const getProgressColor = (progress: number) => {
    if (progress < 50) return "bg-red-500";
    if (progress < 80) return "bg-yellow-500";
    return "bg-green-500";
  }

  return (
    <div className="container mx-auto p-4 md:p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">My Dashboard</h1>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-blue-50 border-blue-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-blue-700">Active Courses</CardTitle>
            <BookOpen className="h-5 w-5 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-900">{mockCourses.length}</div>
            <p className="text-xs text-blue-600">Currently Enrolled</p>
          </CardContent>
        </Card>
        <Card className="bg-yellow-50 border-yellow-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-yellow-700">Pending Assignments</CardTitle>
            <ClipboardList className="h-5 w-5 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-900">{mockAssignments.filter(a => a.status === 'Pending').length}</div>
            <p className="text-xs text-yellow-600">To be completed</p>
          </CardContent>
        </Card>
        <Card className="bg-red-50 border-red-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-red-700">Overdue Tasks</CardTitle>
            <AlertCircle className="h-5 w-5 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-900">{mockAssignments.filter(a => a.status === 'Overdue').length}</div>
            <p className="text-xs text-red-600">Attention needed</p>
          </CardContent>
        </Card>
        <Card className="bg-green-50 border-green-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-green-700">Upcoming Exams</CardTitle>
            <CalendarDays className="h-5 w-5 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-900">{mockExams.length}</div>
            <p className="text-xs text-green-600">Prepare for these</p>
          </CardContent>
        </Card>
      </div>

      {/* My Courses */}
      <Card className="shadow-lg">
        <CardHeader className="bg-gradient-to-r from-purple-500 to-indigo-600 text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-2"><BookOpen /> My Courses</CardTitle>
          <CardDescription className="text-purple-100">Overview of your enrolled courses and progress.</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {mockCourses.map(course => (
              <Card key={course.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <CardTitle className="text-lg">{course.title}</CardTitle>
                  <CardDescription>Instructor: {course.instructor}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-gray-600">Progress</span>
                    <span className={`text-sm font-semibold ${course.progress < 50 ? 'text-red-600' : course.progress < 80 ? 'text-yellow-600' : 'text-green-600'}`}>{course.progress}%</span>
                  </div>
                  <Progress value={course.progress} indicatorClassName={getProgressColor(course.progress)} className="h-3" />
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pending Assignments */}
        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><ClipboardList /> Pending Assignments</CardTitle>
            <CardDescription className="text-yellow-50">Tasks that need your attention.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            {mockAssignments.filter(a => a.status !== 'Submitted').length > 0 ? (
              <ul className="space-y-3">
                {mockAssignments.filter(a => a.status !== 'Submitted').map(assignment => (
                  <li key={assignment.id} className="p-3 bg-gray-50 rounded-md border flex justify-between items-center">
                    <div>
                      <h4 className="font-semibold">{assignment.title}</h4>
                      <p className="text-sm text-gray-500">{assignment.course} - Due: {assignment.dueDate}</p>
                    </div>
                    <Badge className={`text-white ${getStatusColor(assignment.status)}`}>{assignment.status}</Badge>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-center text-gray-500 py-4">No pending assignments. Great job!</p>
            )}
          </CardContent>
        </Card>

        {/* Upcoming Exams */}
        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-teal-400 to-cyan-500 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><CalendarDays /> Upcoming Exams</CardTitle>
            <CardDescription className="text-teal-50">Mark your calendar for these exams.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            {mockExams.length > 0 ? (
              <ul className="space-y-3">
                {mockExams.map(exam => (
                  <li key={exam.id} className="p-3 bg-gray-50 rounded-md border">
                    <h4 className="font-semibold">{exam.course}</h4>
                    <p className="text-sm text-gray-500">Date: {exam.date} at {exam.time}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-center text-gray-500 py-4">No upcoming exams scheduled.</p>
            )}
          </CardContent>
        </Card>
      </div>
      
      {/* Placeholder for Attendance Summary */}
      <Card className="shadow-lg">
        <CardHeader className="bg-gradient-to-r from-pink-500 to-rose-500 text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-2"><CheckCircle /> Attendance Summary</CardTitle>
          <CardDescription className="text-pink-50">Your attendance record.</CardDescription>
        </CardHeader>
        <CardContent className="pt-6 text-center">
          <p className="text-gray-600">Overall Attendance: <span className="font-bold text-2xl text-green-600">92%</span></p>
          {/* More detailed attendance could go here */}
        </CardContent>
      </Card>

    </div>
  );
};

export default StudentDashboardPage;
