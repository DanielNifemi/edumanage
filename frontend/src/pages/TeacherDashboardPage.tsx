import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useNavigate } from 'react-router-dom';
import { BookOpen, Users, BarChart3, Edit3, PlusCircle, Bell, Settings } from 'lucide-react';

// Mock Data Interfaces
interface TeacherCourse {
  id: string;
  title: string;
  studentCount: number;
  status: 'Draft' | 'Published' | 'Archived';
}

interface TeacherAnnouncement {
  id: string;
  title: string;
  date: string;
  course?: string; // Optional: if announcement is course-specific
}

// Mock Data
const mockTeacherCourses: TeacherCourse[] = [
  { id: 'c1', title: 'Introduction to Programming', studentCount: 45, status: 'Published' },
  { id: 'c2', title: 'Advanced Algorithms', studentCount: 28, status: 'Published' },
  { id: 'c3', title: 'Web Development Bootcamp', studentCount: 0, status: 'Draft' },
];

const mockTeacherAnnouncements: TeacherAnnouncement[] = [
  { id: 'an1', title: 'Midterm Exam Schedule Updated', date: '2025-06-10', course: 'Advanced Algorithms' },
  { id: 'an2', title: 'Welcome to New Semester!', date: '2025-06-01' },
];

const TeacherDashboardPage: React.FC = () => {
  const navigate = useNavigate();

  const getStatusColor = (status: TeacherCourse['status']) => {
    if (status === 'Published') return 'bg-green-500 hover:bg-green-600';
    if (status === 'Draft') return 'bg-yellow-500 hover:bg-yellow-600';
    if (status === 'Archived') return 'bg-gray-500 hover:bg-gray-600';
    return 'bg-blue-500';
  };

  return (
    <div className="container mx-auto p-4 md:p-6 space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-800">Teacher Dashboard</h1>
        <Button onClick={() => navigate('/teacher/courses/new')} className="bg-indigo-600 hover:bg-indigo-700">
          <PlusCircle className="mr-2 h-5 w-5" /> Create New Course
        </Button>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-purple-50 border-purple-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-purple-700">Active Courses</CardTitle>
            <BookOpen className="h-5 w-5 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-900">{mockTeacherCourses.filter(c => c.status === 'Published').length}</div>
            <p className="text-xs text-purple-600">Currently teaching</p>
          </CardContent>
        </Card>
        <Card className="bg-teal-50 border-teal-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-teal-700">Total Students</CardTitle>
            <Users className="h-5 w-5 text-teal-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-teal-900">
              {mockTeacherCourses.reduce((sum, course) => sum + course.studentCount, 0)}
            </div>
            <p className="text-xs text-teal-600">Across all active courses</p>
          </CardContent>
        </Card>
        <Card className="bg-sky-50 border-sky-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-sky-700">Draft Courses</CardTitle>
            <Edit3 className="h-5 w-5 text-sky-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-sky-900">{mockTeacherCourses.filter(c => c.status === 'Draft').length}</div>
            <p className="text-xs text-sky-600">Pending publication</p>
          </CardContent>
        </Card>
        <Card className="bg-rose-50 border-rose-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-rose-700">Recent Announcements</CardTitle>
            <Bell className="h-5 w-5 text-rose-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-rose-900">{mockTeacherAnnouncements.length}</div>
            <p className="text-xs text-rose-600">Last 7 days (mock)</p>
          </CardContent>
        </Card>
      </div>

      {/* My Courses */}
      <Card className="shadow-lg">
        <CardHeader className="bg-gradient-to-r from-blue-500 to-cyan-600 text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-2"><BookOpen /> My Courses</CardTitle>
          <CardDescription className="text-blue-100">Manage your courses, view student progress, and create assignments.</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {mockTeacherCourses.map(course => (
              <Card key={course.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg">{course.title}</CardTitle>
                    <Badge className={`text-white ${getStatusColor(course.status)}`}>{course.status}</Badge>
                  </div>
                  <CardDescription>Students Enrolled: {course.studentCount}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => navigate(`/courses/${course.id}`)}>
                      View Details
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => navigate(`/teacher/courses/edit/${course.id}`)}>
                      Edit Course
                    </Button>
                     <Button variant="outline" size="sm" onClick={() => navigate(`/teacher/courses/${course.id}/assignments`)}>
                      Manage Assignments
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
            {mockTeacherCourses.length === 0 && (
                <p className="text-center text-gray-500 py-4">You haven't created any courses yet.</p>
            )}
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Announcements */}
        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><Bell /> Recent Announcements</CardTitle>
            <CardDescription className="text-pink-100">Keep your students informed.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            {mockTeacherAnnouncements.length > 0 ? (
              <ul className="space-y-3">
                {mockTeacherAnnouncements.map(announcement => (
                  <li key={announcement.id} className="p-3 bg-gray-50 rounded-md border">
                    <h4 className="font-semibold">{announcement.title}</h4>
                    <p className="text-sm text-gray-500">
                      {announcement.course ? `${announcement.course} - ` : 'General - '}
                      Posted: {announcement.date}
                    </p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-center text-gray-500 py-4">No recent announcements.</p>
            )}
            <Button variant="outline" className="mt-4 w-full" onClick={() => navigate('/announcements/new')}>Create Announcement</Button>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-green-400 to-emerald-500 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><Settings /> Quick Actions</CardTitle>
            <CardDescription className="text-green-50">Access common teacher tools.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 grid grid-cols-2 gap-4">
            <Button variant="outline" className="w-full justify-start text-left p-4 h-auto flex-col items-start hover:bg-gray-50" onClick={() => navigate('/teacher/attendance')}>
                <Users className="h-6 w-6 mb-1 text-green-700"/> 
                <span className="font-semibold">Manage Attendance</span>
                <span className="text-xs text-gray-500">Track student presence</span>
            </Button>
            <Button variant="outline" className="w-full justify-start text-left p-4 h-auto flex-col items-start hover:bg-gray-50" onClick={() => navigate('/teacher/grades')}>
                <BarChart3 className="h-6 w-6 mb-1 text-green-700"/> 
                <span className="font-semibold">Enter Grades</span>
                <span className="text-xs text-gray-500">Update student marks</span>
            </Button>
            <Button variant="outline" className="w-full justify-start text-left p-4 h-auto flex-col items-start hover:bg-gray-50" onClick={() => navigate('/schedule')}>
                <CalendarDays className="h-6 w-6 mb-1 text-green-700"/> 
                <span className="font-semibold">View Schedule</span>
                <span className="text-xs text-gray-500">Your teaching timetable</span>
            </Button>
            <Button variant="outline" className="w-full justify-start text-left p-4 h-auto flex-col items-start hover:bg-gray-50" onClick={() => navigate('/messages')}>
                <Bell className="h-6 w-6 mb-1 text-green-700"/> 
                <span className="font-semibold">Messages</span>
                <span className="text-xs text-gray-500">Communicate with students</span>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default TeacherDashboardPage;
