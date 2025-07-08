import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/useAuth';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Users, GraduationCap, BookOpen, TrendingUp, AlertTriangle, UserPlus, Settings, DatabaseBackup, BarChart3, Activity } from "lucide-react";

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

  const getPriorityVariant = (priority: string) => {
    switch (priority) {
      case 'high': return 'destructive';
      case 'medium': return 'default';
      case 'low': return 'secondary';
      default: return 'outline';
    }
  };

  return (
      <div className="space-y-6 p-4 md:p-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-slate-900 to-slate-700 rounded-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            System Overview - Admin {user?.first_name || 'Admin'} 🎯
          </h1>
          <p className="text-slate-300">
            Manage users, courses, and system settings from one place.
          </p>
        </div>

        {/* System Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {systemStats.map((stat, index) => (
            <Card key={index} className="border-0 shadow-md hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-gray-500">{stat.label}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                    <p className={`text-xs ${stat.change.startsWith('+') ? 'text-green-500' : stat.change === 'stable' ? 'text-gray-500' : 'text-red-500'}`}>{stat.change}</p>
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
                <Activity className="h-5 w-5 text-indigo-600" />
                Recent Activities
              </CardTitle>
              <CardDescription>Latest system activities and user actions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-medium text-sm">{activity.action} 
                        <span className="text-xs text-gray-500 ml-1">by {activity.user}</span>
                      </p>
                      <p className="text-xs text-gray-400">{activity.time}</p>
                    </div>
                    {/* Placeholder for type icon if needed */}
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
                <AlertTriangle className="h-5 w-5 text-red-600" />
                System Alerts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div key={alert.id} className={`p-3 rounded-md border-l-4 ${alert.type === 'warning' ? 'bg-yellow-50 border-yellow-400' : 'bg-blue-50 border-blue-400'}`}>
                    <p className={`text-sm font-medium ${alert.type === 'warning' ? 'text-yellow-700' : 'text-blue-700'}`}>{alert.message}</p>
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
              <UserPlus className="h-5 w-5 text-green-600" />
              Pending Approvals
            </CardTitle>
            <CardDescription>Items requiring administrative approval</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {pendingApprovals.map((approval) => (
                <div key={approval.id} className="p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors border flex justify-between items-center">
                  <div>
                    <h4 className="font-semibold text-sm">{approval.name}</h4>
                    <p className="text-xs text-gray-500">{approval.type} - {approval.department}</p>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                     <Badge variant={getPriorityVariant(approval.priority)}>{approval.priority}</Badge>
                     <Button size="sm" variant="link" className="text-xs p-0 h-auto">Review</Button>
                  </div>
                </div>
              ))}
            </div>
             <Button variant="outline" className="w-full mt-4">
                View All Approvals
              </Button>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="border-0 shadow-md">
          <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Fast access to common administrative tasks.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {            [
              { to: "/students", label: "Manage Students", icon: Users, color: "blue" },
              { to: "/teachers", label: "Manage Teachers", icon: GraduationCap, color: "green" },
              { to: "/admin/users/create", label: "Add New User", icon: UserPlus, color: "blue" },
              { to: "/admin/reports", label: "View Reports", icon: BarChart3, color: "green" },
              { to: "/admin/settings", label: "System Settings", icon: Settings, color: "purple" },
              { to: "/admin/backup", label: "Data Backup", icon: DatabaseBackup, color: "orange" },
            ].map(action => (
              <Link key={action.to} to={action.to}>
                <Card className={`border-0 shadow-md hover:shadow-lg transition-shadow cursor-pointer bg-${action.color}-50 hover:bg-${action.color}-100`}>
                  <CardContent className="p-4 text-center flex flex-col items-center justify-center h-full min-h-[120px]">
                    <action.icon className={`h-8 w-8 text-${action.color}-600 mx-auto mb-2`} />
                    <p className={`text-sm font-medium text-${action.color}-700`}>{action.label}</p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </CardContent>
        </Card>
      </div>
  );
};

export default AdminDashboard;
