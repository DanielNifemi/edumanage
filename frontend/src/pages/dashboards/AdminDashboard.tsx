
import { useAuth } from "@/hooks/useAuth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Users, GraduationCap, BookOpen, TrendingUp, AlertTriangle, UserPlus } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Link } from "react-router-dom";

const AdminDashboard = () => {
  const { user } = useAuth();

  const systemStats = [
    { label: "Total Students", value: "2,847", change: "+12%", icon: Users, color: "blue" },
    { label: "Active Teachers", value: "156", change: "+3%", icon: GraduationCap, color: "green" },
    { label: "Courses Offered", value: "342", change: "+8%", icon: BookOpen, color: "purple" },
    { label: "System Uptime", value: "99.9%", change: "stable", icon: TrendingUp, color: "orange" },
  ];

  const recentActivities = [
    { id: 1, action: "New student registration", user: "John Doe", time: "5 minutes ago", type: "registration" },
    { id: 2, action: "Course completion", user: "Jane Smith", time: "1 hour ago", type: "achievement" },
    { id: 3, action: "Teacher account created", user: "Dr. Wilson", time: "2 hours ago", type: "registration" },
    { id: 4, action: "System backup completed", user: "System", time: "6 hours ago", type: "system" },
  ];

  const pendingApprovals = [
    { id: 1, type: "Teacher Application", name: "Dr. Sarah Johnson", department: "Mathematics", priority: "high" },
    { id: 2, type: "Course Proposal", name: "Advanced AI Ethics", department: "Computer Science", priority: "medium" },
    { id: 3, type: "Budget Request", name: "Lab Equipment", department: "Chemistry", priority: "low" },
  ];

  const alerts = [
    { id: 1, message: "Server maintenance scheduled for this weekend", type: "warning" },
    { id: 2, message: "New security patch available", type: "info" },
    { id: 3, message: "Storage capacity at 85%", type: "warning" },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            System Overview - {user?.firstName} 🎯
          </h1>
          <p className="text-blue-100">
            Manage your educational platform with comprehensive insights and administrative tools.
          </p>
        </div>

        {/* System Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {systemStats.map((stat, index) => (
            <Card key={index} className="border-0 shadow-md">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                    <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                    <p className={`text-sm ${stat.change.includes('+') ? 'text-green-600' : 'text-gray-500'}`}>
                      {stat.change}
                    </p>
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
          {/* Recent Activities */}
          <Card className="lg:col-span-2 border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Recent Activities
              </CardTitle>
              <CardDescription>Latest system activities and user actions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-8 rounded-full ${
                        activity.type === 'registration' ? 'bg-green-500' : 
                        activity.type === 'achievement' ? 'bg-blue-500' : 'bg-gray-500'
                      }`}></div>
                      <div>
                        <p className="font-medium text-gray-900">{activity.action}</p>
                        <p className="text-sm text-gray-600">{activity.user}</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-500">{activity.time}</p>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4">
                View All Activities
              </Button>
            </CardContent>
          </Card>

          {/* System Alerts */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                System Alerts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {alerts.map((alert) => (
                  <div key={alert.id} className={`p-3 rounded-lg border-l-4 ${
                    alert.type === 'warning' ? 'bg-yellow-50 border-yellow-400' : 'bg-blue-50 border-blue-400'
                  }`}>
                    <p className="text-sm text-gray-700">{alert.message}</p>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4" size="sm">
                Manage Alerts
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Pending Approvals */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <UserPlus className="h-5 w-5" />
              Pending Approvals
            </CardTitle>
            <CardDescription>Items requiring administrative approval</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {pendingApprovals.map((approval) => (
                <div key={approval.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h4 className="font-medium text-gray-900">{approval.name}</h4>
                      <Badge 
                        variant={approval.priority === 'high' ? 'destructive' : 
                                approval.priority === 'medium' ? 'default' : 'secondary'}
                      >
                        {approval.priority} priority
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600">{approval.type} • {approval.department}</p>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      Review
                    </Button>
                    <Button size="sm">
                      Approve
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link to="/admin/users/create">
            <Card className="border-0 shadow-md hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="p-6 text-center">
                <UserPlus className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                <h3 className="font-medium text-gray-900">Add User</h3>
                <p className="text-sm text-gray-600">Create new account</p>
              </CardContent>
            </Card>
          </Link>

          <Link to="/admin/reports">
            <Card className="border-0 shadow-md hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="p-6 text-center">
                <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
                <h3 className="font-medium text-gray-900">Reports</h3>
                <p className="text-sm text-gray-600">System analytics</p>
              </CardContent>
            </Card>
          </Link>

          <Link to="/admin/settings">
            <Card className="border-0 shadow-md hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="p-6 text-center">
                <AlertTriangle className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                <h3 className="font-medium text-gray-900">Settings</h3>
                <p className="text-sm text-gray-600">System configuration</p>
              </CardContent>
            </Card>
          </Link>

          <Link to="/admin/backup">
            <Card className="border-0 shadow-md hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="p-6 text-center">
                <BookOpen className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                <h3 className="font-medium text-gray-900">Backup</h3>
                <p className="text-sm text-gray-600">Data management</p>
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default AdminDashboard;
