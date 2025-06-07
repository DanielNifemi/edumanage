
import { useAuth } from "@/hooks/useAuth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Calendar, BookOpen, ClipboardCheck, Clock, TrendingUp, Bell } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Link } from "react-router-dom";

const StudentDashboard = () => {
  const { user } = useAuth();

  const upcomingAssignments = [
    { id: 1, title: "Math Problem Set 5", course: "Calculus I", dueDate: "2024-01-15", priority: "high" },
    { id: 2, title: "History Essay", course: "World History", dueDate: "2024-01-18", priority: "medium" },
    { id: 3, title: "Lab Report", course: "Chemistry", dueDate: "2024-01-20", priority: "low" },
  ];

  const currentCourses = [
    { id: 1, name: "Calculus I", instructor: "Dr. Smith", progress: 75, nextClass: "Today 2:00 PM" },
    { id: 2, name: "World History", instructor: "Prof. Johnson", progress: 60, nextClass: "Tomorrow 10:00 AM" },
    { id: 3, name: "Chemistry", instructor: "Dr. Brown", progress: 85, nextClass: "Wed 1:00 PM" },
    { id: 4, name: "English Literature", instructor: "Ms. Davis", progress: 70, nextClass: "Thu 11:00 AM" },
  ];

  const recentAnnouncements = [
    { id: 1, title: "Midterm Exam Schedule Released", time: "2 hours ago" },
    { id: 2, title: "Library Hours Extended", time: "1 day ago" },
    { id: 3, title: "Career Fair Next Week", time: "3 days ago" },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, {user?.firstName}! 👋
          </h1>
          <p className="text-blue-100">
            You have 3 upcoming assignments and 2 classes today. Let's make it a productive day!
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Enrolled Courses</p>
                  <p className="text-3xl font-bold text-gray-900">4</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <BookOpen className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Pending Assignments</p>
                  <p className="text-3xl font-bold text-gray-900">3</p>
                </div>
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <ClipboardCheck className="h-6 w-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Attendance Rate</p>
                  <p className="text-3xl font-bold text-gray-900">94%</p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="h-6 w-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">GPA</p>
                  <p className="text-3xl font-bold text-gray-900">3.7</p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upcoming Assignments */}
          <Card className="lg:col-span-2 border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ClipboardCheck className="h-5 w-5" />
                Upcoming Assignments
              </CardTitle>
              <CardDescription>
                Stay on top of your deadlines
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {upcomingAssignments.map((assignment) => (
                  <div key={assignment.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{assignment.title}</h4>
                      <p className="text-sm text-gray-600">{assignment.course}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge 
                        variant={assignment.priority === 'high' ? 'destructive' : 
                                assignment.priority === 'medium' ? 'default' : 'secondary'}
                      >
                        {assignment.priority}
                      </Badge>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">Due {assignment.dueDate}</p>
                        <p className="text-xs text-gray-500 flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          3 days left
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <Link to="/student/assignments">
                <Button variant="outline" className="w-full mt-4">
                  View All Assignments
                </Button>
              </Link>
            </CardContent>
          </Card>

          {/* Announcements */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Recent Announcements
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentAnnouncements.map((announcement) => (
                  <div key={announcement.id} className="space-y-2">
                    <h4 className="font-medium text-gray-900 text-sm leading-tight">
                      {announcement.title}
                    </h4>
                    <p className="text-xs text-gray-500">{announcement.time}</p>
                    {announcement.id !== recentAnnouncements.length && (
                      <hr className="border-gray-200" />
                    )}
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4" size="sm">
                View All Announcements
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Current Courses */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Current Courses
            </CardTitle>
            <CardDescription>
              Your enrolled courses and progress
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {currentCourses.map((course) => (
                <div key={course.id} className="p-4 bg-gray-50 rounded-lg space-y-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-semibold text-gray-900">{course.name}</h4>
                      <p className="text-sm text-gray-600">{course.instructor}</p>
                    </div>
                    <Badge variant="outline">{course.progress}% Complete</Badge>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Progress</span>
                      <span className="font-medium">{course.progress}%</span>
                    </div>
                    <Progress value={course.progress} className="h-2" />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1 text-sm text-gray-600">
                      <Calendar className="h-4 w-4" />
                      {course.nextClass}
                    </div>
                    <Link to={`/courses/${course.id}`}>
                      <Button size="sm" variant="outline">
                        View Course
                      </Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default StudentDashboard;
