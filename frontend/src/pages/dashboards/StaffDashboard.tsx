
import { useAuth } from "@/hooks/useAuth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Users, Calendar, FileText, Clock, TrendingUp, Bell } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Link } from "react-router-dom";

const StaffDashboard = () => {
  const { user } = useAuth();

  const workloadStats = [
    { label: "Active Tasks", value: "8", change: "-2 from yesterday", icon: FileText },
    { label: "Students Assisted", value: "24", change: "+5 from yesterday", icon: Users },
    { label: "Hours This Week", value: "32", change: "8 hours remaining", icon: Clock },
    { label: "Department Rating", value: "4.8", change: "+0.2 this month", icon: TrendingUp },
  ];

  const todaySchedule = [
    { time: "9:00 AM", task: "Student Registration Support", location: "Registration Office", type: "student-service" },
    { time: "11:00 AM", task: "Department Meeting", location: "Conference Room A", type: "meeting" },
    { time: "2:00 PM", task: "Academic Records Review", location: "Records Office", type: "administrative" },
    { time: "4:00 PM", task: "Parent Consultation", location: "Office 205", type: "consultation" },
  ];

  const pendingRequests = [
    { id: 1, type: "Transcript Request", student: "Alice Johnson", submitted: "2 hours ago", priority: "high" },
    { id: 2, type: "Course Change", student: "Bob Smith", submitted: "4 hours ago", priority: "medium" },
    { id: 3, type: "Grade Appeal", student: "Carol Davis", submitted: "1 day ago", priority: "high" },
    { id: 4, type: "Transfer Credit", student: "David Wilson", submitted: "2 days ago", priority: "low" },
  ];

  const notifications = [
    { id: 1, message: "New student enrollment forms ready for review", time: "30 minutes ago" },
    { id: 2, message: "Department budget meeting rescheduled", time: "2 hours ago" },
    { id: 3, message: "Updated academic calendar available", time: "1 day ago" },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Welcome, {user?.firstName}! 🏢
          </h1>
          <p className="text-blue-100">
            You have 4 tasks scheduled today and 8 pending student requests. Let's help students succeed!
          </p>
        </div>

        {/* Workload Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {workloadStats.map((stat, index) => (
            <Card key={index} className="border-0 shadow-md">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                    <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                    <p className="text-sm text-gray-500">{stat.change}</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <stat.icon className="h-6 w-6 text-blue-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Today's Schedule */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Today's Schedule
              </CardTitle>
              <CardDescription>Your tasks and appointments</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {todaySchedule.map((item, index) => (
                  <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                    <div className={`w-3 h-3 rounded-full ${
                      item.type === 'student-service' ? 'bg-blue-500' : 
                      item.type === 'meeting' ? 'bg-green-500' : 
                      item.type === 'administrative' ? 'bg-orange-500' : 'bg-purple-500'
                    }`}></div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 text-sm">{item.task}</p>
                      <p className="text-xs text-gray-600">{item.location}</p>
                    </div>
                    <p className="text-sm font-medium text-gray-700">{item.time}</p>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4" size="sm">
                View Full Calendar
              </Button>
            </CardContent>
          </Card>

          {/* Pending Requests */}
          <Card className="lg:col-span-2 border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Pending Student Requests
              </CardTitle>
              <CardDescription>Requests requiring your attention</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {pendingRequests.map((request) => (
                  <div key={request.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <h4 className="font-medium text-gray-900">{request.type}</h4>
                        <Badge 
                          variant={request.priority === 'high' ? 'destructive' : 
                                  request.priority === 'medium' ? 'default' : 'secondary'}
                        >
                          {request.priority}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600">Student: {request.student}</p>
                      <p className="text-xs text-gray-500">Submitted: {request.submitted}</p>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        Review
                      </Button>
                      <Button size="sm">
                        Process
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
              <Link to="/staff/requests">
                <Button variant="outline" className="w-full mt-4">
                  View All Requests
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions & Notifications */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Quick Actions */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Common staff tasks and tools</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3">
                <Button className="h-20 flex-col gap-2" variant="outline">
                  <Users className="h-5 w-5" />
                  <span className="text-sm">Student Lookup</span>
                </Button>
                <Button className="h-20 flex-col gap-2" variant="outline">
                  <FileText className="h-5 w-5" />
                  <span className="text-sm">Generate Report</span>
                </Button>
                <Button className="h-20 flex-col gap-2" variant="outline">
                  <Calendar className="h-5 w-5" />
                  <span className="text-sm">Schedule Meeting</span>
                </Button>
                <Button className="h-20 flex-col gap-2" variant="outline">
                  <Bell className="h-5 w-5" />
                  <span className="text-sm">Send Notice</span>
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Notifications */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Recent Notifications
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {notifications.map((notification) => (
                  <div key={notification.id} className="p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-900 mb-1">{notification.message}</p>
                    <p className="text-xs text-gray-500">{notification.time}</p>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4" size="sm">
                View All Notifications
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Department Overview */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Department Performance
            </CardTitle>
            <CardDescription>Overview of departmental metrics and achievements</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <h3 className="text-2xl font-bold text-blue-600">98%</h3>
                <p className="text-sm text-gray-600">Request Processing Rate</p>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <h3 className="text-2xl font-bold text-green-600">4.8/5</h3>
                <p className="text-sm text-gray-600">Student Satisfaction</p>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <h3 className="text-2xl font-bold text-purple-600">2.5hrs</h3>
                <p className="text-sm text-gray-600">Avg. Response Time</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default StaffDashboard;
