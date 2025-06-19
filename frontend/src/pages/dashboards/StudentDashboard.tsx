import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/useAuth';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Users, BookOpen, TrendingUp, ClipboardCheck, Bell, Calendar, CheckCircle, Clock, FileText, UserPlus, Edit, MessageSquare, Settings } from "lucide-react";

const StudentDashboard = () => {
  const { user } = useAuth();

  const upcomingAssignments = [
    { id: 1, title: "Math Problem Set 5", course: "Calculus I", dueDate: "2025-06-15", priority: "high" },
    { id: 2, title: "History Essay", course: "World History", dueDate: "2025-06-18", priority: "medium" },
    { id: 3, title: "Lab Report", course: "Chemistry", dueDate: "2025-06-20", priority: "low" },
  ];

  const currentCourses = [
    { id: 1, name: "Calculus I", instructor: "Dr. Smith", progress: 75, nextClass: "Today 2:00 PM", color: "blue" },
    { id: 2, name: "World History", instructor: "Prof. Johnson", progress: 60, nextClass: "Tomorrow 10:00 AM", color: "purple" },
    { id: 3, name: "Chemistry", instructor: "Dr. Brown", progress: 85, nextClass: "Wed 1:00 PM", color: "green" },
    { id: 4, name: "English Literature", instructor: "Ms. Davis", progress: 70, nextClass: "Thu 11:00 AM", color: "orange" },
  ];

  const recentAnnouncements = [
    { id: 1, title: "Midterm Exam Schedule Released", time: "2 hours ago", course: "All Courses" },
    { id: 2, title: "Library Hours Extended for Finals", time: "1 day ago", course: "General" },
    { id: 3, title: "Career Fair Next Week - Sign Up!", time: "3 days ago", course: "General" },
  ];

  const quickStats = [
      { label: "Active Courses", value: currentCourses.length, icon: BookOpen, color: "blue" },
      { label: "Pending Assignments", value: upcomingAssignments.filter(a => a.priority !== 'low').length, icon: ClipboardCheck, color: "orange" }, // Example: count high/medium priority
      { label: "Overall Progress", value: "72%", icon: TrendingUp, color: "green" }, // Mocked overall progress
      { label: "Attendance Rate", value: "95%", icon: CheckCircle, color: "purple" }, // Mocked attendance
  ];

  const getPriorityBadgeVariant = (priority: string) => {
    if (priority === 'high') return 'destructive';
    if (priority === 'medium') return 'default';
    return 'secondary';
  };

  const getProgressColor = (progress: number) => {
    if (progress < 50) return "bg-red-500";
    if (progress < 80) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, {user?.first_name || 'Student'}! 👋
          </h1>
          <p className="text-blue-100">
            Here's your academic progress and upcoming tasks at a glance.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickStats.map((stat, index) => (
            <Card key={index} className="border-0 shadow-md hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-gray-500">{stat.label}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                  </div>
                  <div className={`w-12 h-12 bg-${stat.color}-100 rounded-lg flex items-center justify-center`}>
                    <stat.icon className={`h-6 w-6 text-${stat.color}-600`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upcoming Assignments */}
          <Card className="lg:col-span-2 border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ClipboardCheck className="h-5 w-5 text-orange-600" />
                Upcoming Assignments
              </CardTitle>
              <CardDescription>
                Stay on top of your deadlines.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {upcomingAssignments.map((assignment) => (
                  <div key={assignment.id} className="p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors border">
                    <div className="flex justify-between items-start">
                        <div>
                            <h4 className="font-semibold text-sm">{assignment.title}</h4>
                            <p className="text-xs text-gray-500">{assignment.course} - Due: {new Date(assignment.dueDate).toLocaleDateString()}</p>
                        </div>
                        <Badge variant={getPriorityBadgeVariant(assignment.priority)}>{assignment.priority}</Badge>
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
                <Bell className="h-5 w-5 text-purple-600" />
                Recent Announcements
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentAnnouncements.map((announcement) => (
                  <div key={announcement.id} className="p-3 bg-purple-50 border-l-4 border-purple-400 rounded-r-md">
                    <h4 className="font-semibold text-sm text-purple-700">{announcement.title}</h4>
                    <p className="text-xs text-purple-500">{announcement.course} - {announcement.time}</p>
                  </div>
                ))}
              </div>
              <Link to="/announcements">
                <Button variant="outline" className="w-full mt-4" size="sm">
                  View All Announcements
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Current Courses */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-blue-600" />
              Current Courses
            </CardTitle>
            <CardDescription>
              Your enrolled courses and progress.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {currentCourses.map((course) => (
                <Card key={course.id} className={`border-l-4 border-${course.color}-500 shadow-sm hover:shadow-md transition-shadow`}>
                  <CardHeader>
                    <CardTitle className="text-md">{course.name}</CardTitle>
                    <CardDescription>Instructor: {course.instructor}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-2">
                        <div className="flex justify-between text-xs text-gray-500 mb-1">
                            <span>Progress</span>
                            <span>{course.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                          <div 
                            className={`h-2 rounded-full ${getProgressColor(course.progress)}`}
                            style={{ width: `${course.progress}%` }}
                          ></div>
                        </div>
                      </div>
                    <p className="text-xs text-gray-500"><Clock className="inline h-3 w-3 mr-1"/>Next class: {course.nextClass}</p>
                    <Button variant="outline" size="sm" className="mt-3 w-full text-xs">Go to Course</Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
  );
};

export default StudentDashboard;
