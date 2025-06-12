import { Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Users, Briefcase, CalendarCheck, Settings, UserPlus, FileText, Building, Bell } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import DashboardLayout from "@/components/layout/DashboardLayout";

const StaffDashboard = () => {
  const { user } = useAuth();

  const quickStatsData = [
    { label: "Total Students", value: "1250", icon: Users, color: "blue" },
    { label: "Active Staff", value: "75", icon: Briefcase, color: "green" },
    { label: "Upcoming Events", value: "5", icon: CalendarCheck, color: "orange" },
    { label: "System Alerts", value: "2", icon: Bell, color: "red" },
  ];

  const recentActivities = [
    { id: 1, activity: "New student enrollment: John B.", time: "10 mins ago", category: "Enrollment" },
    { id: 2, activity: "Staff meeting scheduled for 3 PM.", time: "1 hour ago", category: "Meetings" },
    { id: 3, activity: "Maintenance request #1024 closed.", time: "3 hours ago", category: "Maintenance" },
    { id: 4, activity: "New course 'Advanced Python' added.", time: "Yesterday", category: "Academics" },
  ];

  const pendingTasks = [
    { id: 1, task: "Process financial aid applications", due: "Tomorrow", priority: "high" as const },
    { id: 2, task: "Update student records for Grade 10", due: "Friday", priority: "medium" as const },
    { id: 3, task: "Organize staff training session", due: "Next week", priority: "low" as const },
  ];

  const getPriorityVariant = (priority: 'high' | 'medium' | 'low') => {
    if (priority === 'high') return 'destructive';
    if (priority === 'medium') return 'secondary';
    return 'outline';
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Welcome, {user?.first_name || 'Staff Member'}! 🏢
          </h1>
          <p className="text-indigo-100">
            Here's what's happening today. You have {pendingTasks.length} pending tasks.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickStatsData.map((stat, index) => (
            <Card key={index} className="border-0 shadow-md">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-500">{stat.label}</p>
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

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Activities */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle>Recent Activities</CardTitle>
              <CardDescription>Latest updates and actions in the system</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivities.length > 0 ? recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors">
                    <div className="flex-shrink-0 pt-1">
                      <Badge variant="outline" className="text-xs">{activity.category}</Badge>
                    </div>
                    <div>
                      <p className="text-sm font-medium">{activity.activity}</p>
                      <p className="text-xs text-gray-500">{activity.time}</p>
                    </div>
                  </div>
                )) : <p className="text-sm text-gray-500">No recent activities.</p>}
              </div>
            </CardContent>
          </Card>

          {/* Pending Tasks */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle>Pending Tasks</CardTitle>
              <CardDescription>Important tasks requiring your attention</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {pendingTasks.length > 0 ? pendingTasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-semibold text-sm">{task.task}</p>
                      <p className="text-xs text-gray-600">Due: {task.due}</p>
                    </div>
                    <Badge variant={getPriorityVariant(task.priority)} className="capitalize text-xs">{task.priority}</Badge>
                  </div>
                )) : <p className="text-sm text-gray-500">No pending tasks.</p>}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Commonly used staff functions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <Link to="/staff/student-enrollment">
                <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                  <UserPlus className="mb-1 h-6 w-6" /> Enroll Student
                </Button>
              </Link>
              <Link to="/staff/manage-records">
                <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                  <FileText className="mb-1 h-6 w-6" /> Manage Records
                </Button>
              </Link>
              <Link to="/staff/facility-management">
                <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                  <Building className="mb-1 h-6 w-6" /> Facility Management
                </Button>
              </Link>
              <Link to="/staff/system-settings">
                <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                  <Settings className="mb-1 h-6 w-6" /> System Settings
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default StaffDashboard;
