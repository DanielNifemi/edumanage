import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from 'react-router-dom';
import { Users, BookOpenText, BarChartBig, Settings2, Building, FileText, ShieldCheck } from 'lucide-react';

// Mock Data Interfaces (Simplified for Admin)
interface AdminStat {
  id: string;
  title: string;
  value: string | number;
  icon: React.ElementType;
  color: string;
  actionPath?: string;
  actionLabel?: string;
}

// Mock Data
const mockAdminStats: AdminStat[] = [
  { id: 's1', title: 'Total Users', value: 1250, icon: Users, color: 'text-blue-500', actionPath: '/admin/users', actionLabel: 'Manage Users' },
  { id: 's2', title: 'Active Courses', value: 78, icon: BookOpenText, color: 'text-green-500', actionPath: '/courses', actionLabel: 'View Courses' },
  { id: 's3', title: 'Teachers', value: 120, icon: Users, color: 'text-purple-500', actionPath: '/teachers', actionLabel: 'Manage Teachers' },
  { id: 's4', title: 'Students', value: 950, icon: Users, color: 'text-yellow-500', actionPath: '/students', actionLabel: 'Manage Students' },
  { id: 's5', title: 'Pending Approvals', value: 12, icon: ShieldCheck, color: 'text-red-500', actionPath: '/admin/approvals', actionLabel: 'Review' },
  { id: 's6', title: 'System Health', value: 'Optimal', icon: Settings2, color: 'text-teal-500', actionPath: '/admin/settings', actionLabel: 'Configure' },
];

const AdminDashboardPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="container mx-auto p-4 md:p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Administrator Dashboard</h1>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockAdminStats.slice(0, 6).map(stat => (
          <Card key={stat.id} className={`border-l-4 border-${stat.color.replace('text-','')} shadow-lg hover:shadow-xl transition-shadow`}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className={`text-sm font-medium ${stat.color.replace('500','700')}`}>{stat.title}</CardTitle>
              <stat.icon className={`h-5 w-5 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${stat.color.replace('500','900')}`}>{stat.value}</div>
              {stat.actionPath && stat.actionLabel && (
                <Button variant="link" size="sm" className="p-0 h-auto text-xs text-gray-500 hover:text-gray-700" onClick={() => navigate(stat.actionPath)}>
                  {stat.actionLabel}
                </Button>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Management Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-gray-700 to-gray-900 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><Users /> User Management</CardTitle>
            <CardDescription className="text-gray-300">Oversee all user accounts and roles.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-3">
            <Button className="w-full justify-start bg-slate-600 hover:bg-slate-700 text-white" onClick={() => navigate('/admin/users')}><Users className="mr-2 h-4 w-4"/> View All Users</Button>
            <Button className="w-full justify-start bg-slate-600 hover:bg-slate-700 text-white" onClick={() => navigate('/admin/users/new')}><PlusCircle className="mr-2 h-4 w-4"/> Add New User</Button>
            <Button className="w-full justify-start bg-slate-600 hover:bg-slate-700 text-white" onClick={() => navigate('/admin/roles')}><ShieldCheck className="mr-2 h-4 w-4"/> Manage Roles & Permissions</Button>
          </CardContent>
        </Card>

        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-indigo-600 to-purple-700 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><BookOpenText /> Academic Management</CardTitle>
            <CardDescription className="text-indigo-100">Manage courses, subjects, and academic structure.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-3">
            <Button className="w-full justify-start bg-indigo-500 hover:bg-indigo-600 text-white" onClick={() => navigate('/courses')}><BookOpenText className="mr-2 h-4 w-4"/> Manage Courses</Button>
            <Button className="w-full justify-start bg-indigo-500 hover:bg-indigo-600 text-white" onClick={() => navigate('/admin/subjects')}><FileText className="mr-2 h-4 w-4"/> Manage Subjects</Button>
            <Button className="w-full justify-start bg-indigo-500 hover:bg-indigo-600 text-white" onClick={() => navigate('/admin/semesters')}><CalendarDays className="mr-2 h-4 w-4"/> Academic Calendar</Button>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-red-500 to-orange-600 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><BarChartBig /> Reports & Analytics</CardTitle>
            <CardDescription className="text-red-100">View system-wide reports and statistics.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-3">
            <Button className="w-full justify-start bg-red-400 hover:bg-red-500 text-white" onClick={() => navigate('/admin/reports/enrollment')}><Users className="mr-2 h-4 w-4"/> Enrollment Statistics</Button>
            <Button className="w-full justify-start bg-red-400 hover:bg-red-500 text-white" onClick={() => navigate('/admin/reports/grading')}><ClipboardList className="mr-2 h-4 w-4"/> Grading Reports</Button>
            <Button className="w-full justify-start bg-red-400 hover:bg-red-500 text-white" onClick={() => navigate('/admin/reports/activity')}><Activity className="mr-2 h-4 w-4"/> User Activity Logs</Button>
          </CardContent>
        </Card>

        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-teal-500 to-cyan-600 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2"><Settings2 /> System Configuration</CardTitle>
            <CardDescription className="text-teal-100">Manage global settings and integrations.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-3">
            <Button className="w-full justify-start bg-teal-400 hover:bg-teal-500 text-white" onClick={() => navigate('/admin/settings/general')}><Settings className="mr-2 h-4 w-4"/> General Settings</Button>
            <Button className="w-full justify-start bg-teal-400 hover:bg-teal-500 text-white" onClick={() => navigate('/admin/settings/integrations')}><PlugZap className="mr-2 h-4 w-4"/> Integrations</Button>
            <Button className="w-full justify-start bg-teal-400 hover:bg-teal-500 text-white" onClick={() => navigate('/admin/settings/backup')}><DatabaseBackup className="mr-2 h-4 w-4"/> Backup & Restore</Button>
          </CardContent>
        </Card>
      </div>

    </div>
  );
};

export default AdminDashboardPage;
