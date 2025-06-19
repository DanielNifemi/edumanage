import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from 'react-router-dom';
import { UserPlus, FileSpreadsheet, CalendarCheck2, Settings, HelpCircle, BarChart3 } from 'lucide-react';

// Mock Data Interfaces (Simplified for Staff)
interface StaffQuickLink {
  id: string;
  title: string;
  description: string;
  icon: React.ElementType;
  path: string;
  color: string; // Tailwind color class for icon and border
}

// Mock Data
const mockStaffLinks: StaffQuickLink[] = [
  { id: 'ql1', title: 'Student Enrollment', description: 'Manage student registration and records.', icon: UserPlus, path: '/staff/enrollment', color: 'text-blue-500 border-blue-500' },
  { id: 'ql2', title: 'Fee Management', description: 'Track payments and financial records.', icon: FileSpreadsheet, path: '/staff/fees', color: 'text-green-500 border-green-500' },
  { id: 'ql3', title: 'Event Scheduling', description: 'Organize and manage school events.', icon: CalendarCheck2, path: '/staff/events', color: 'text-purple-500 border-purple-500' },
  { id: 'ql4', title: 'Support Tickets', description: 'Address queries from students and staff.', icon: HelpCircle, path: '/staff/support', color: 'text-yellow-500 border-yellow-500' },
  { id: 'ql5', title: 'Reporting', description: 'Generate administrative reports.', icon: BarChart3, path: '/staff/reports', color: 'text-red-500 border-red-500' },
  { id: 'ql6', title: 'Profile Settings', description: 'Update your personal information.', icon: Settings, path: '/profile', color: 'text-teal-500 border-teal-500' },
];

const StaffDashboardPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="container mx-auto p-4 md:p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Staff Dashboard</h1>
      <p className="text-gray-600">Welcome! Access your tools and manage administrative tasks.</p>

      {/* Quick Links Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockStaffLinks.map(link => (
          <Card 
            key={link.id} 
            className={`shadow-lg hover:shadow-xl transition-shadow cursor-pointer border-l-4 ${link.color.split(' ')[1]}`}
            onClick={() => navigate(link.path)}
          >
            <CardHeader className="flex flex-row items-center gap-4 space-y-0">
              <link.icon className={`h-8 w-8 ${link.color.split(' ')[0]}`} />
              <CardTitle className={`text-lg ${link.color.split(' ')[0].replace('500','700')}`}>{link.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>{link.description}</CardDescription>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Placeholder for recent activity or important notices */}
      <Card className="shadow-lg">
        <CardHeader className="bg-gradient-to-r from-gray-100 to-gray-200 rounded-t-lg">
          <CardTitle className="text-gray-700">Notifications & Updates</CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <p className="text-center text-gray-500 py-8">No new notifications at this time.</p>
          {/* Example Notification Item */}
          {/* 
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-md">
            <h4 className="font-semibold text-blue-700">System Maintenance Scheduled</h4>
            <p className="text-sm text-blue-600">The system will be down for maintenance on June 15th from 2 AM to 4 AM.</p>
          </div> 
          */}
        </CardContent>
      </Card>
    </div>
  );
};

export default StaffDashboardPage;
