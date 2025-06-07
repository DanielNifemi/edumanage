
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BarChart3, Download, FileText, Users, Calendar, TrendingUp } from "lucide-react";

const StaffReports = () => {
  const reportSummary = {
    totalStudents: 1250,
    activeTeachers: 85,
    coursesOffered: 156,
    attendanceRate: 94.2
  };

  const recentReports = [
    {
      id: 1,
      title: "Monthly Attendance Report",
      type: "Attendance",
      date: "2024-03-15",
      status: "Ready",
      downloadUrl: "#"
    },
    {
      id: 2,
      title: "Student Enrollment Summary",
      type: "Enrollment",
      date: "2024-03-14",
      status: "Ready",
      downloadUrl: "#"
    },
    {
      id: 3,
      title: "Teacher Performance Review",
      type: "Performance",
      date: "2024-03-13",
      status: "Processing",
      downloadUrl: "#"
    }
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Staff Reports</h1>
            <p className="text-gray-600">Generate and view institutional reports</p>
          </div>
          <div className="flex gap-2">
            <Select defaultValue="current">
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="current">Current Month</SelectItem>
                <SelectItem value="quarter">This Quarter</SelectItem>
                <SelectItem value="year">This Year</SelectItem>
              </SelectContent>
            </Select>
            <Button>Generate Report</Button>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Users className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Students</p>
                  <p className="text-2xl font-bold">{reportSummary.totalStudents}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <Users className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Active Teachers</p>
                  <p className="text-2xl font-bold">{reportSummary.activeTeachers}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <FileText className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Courses Offered</p>
                  <p className="text-2xl font-bold">{reportSummary.coursesOffered}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-orange-100 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Attendance Rate</p>
                  <p className="text-2xl font-bold">{reportSummary.attendanceRate}%</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="generated" className="space-y-4">
          <TabsList>
            <TabsTrigger value="generated">Generated Reports</TabsTrigger>
            <TabsTrigger value="scheduled">Scheduled Reports</TabsTrigger>
            <TabsTrigger value="templates">Report Templates</TabsTrigger>
          </TabsList>

          <TabsContent value="generated" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Recent Reports</CardTitle>
                <CardDescription>Download and view recently generated reports</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentReports.map((report) => (
                    <div key={report.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-4">
                        <div className="p-2 bg-gray-100 rounded">
                          <FileText className="h-5 w-5 text-gray-600" />
                        </div>
                        <div>
                          <h3 className="font-semibold">{report.title}</h3>
                          <p className="text-sm text-gray-600">
                            {report.type} • Generated on {report.date}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <Badge variant={report.status === 'Ready' ? 'default' : 'secondary'}>
                          {report.status}
                        </Badge>
                        {report.status === 'Ready' && (
                          <Button size="sm" variant="outline" className="flex items-center gap-1">
                            <Download className="h-3 w-3" />
                            Download
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="scheduled" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Scheduled Reports</CardTitle>
                <CardDescription>Automatically generated reports on schedule</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <Calendar className="h-5 w-5 text-blue-600" />
                      <div>
                        <h3 className="font-semibold">Weekly Attendance Summary</h3>
                        <p className="text-sm text-gray-600">Every Monday at 8:00 AM</p>
                      </div>
                    </div>
                    <Badge>Active</Badge>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <Calendar className="h-5 w-5 text-green-600" />
                      <div>
                        <h3 className="font-semibold">Monthly Financial Report</h3>
                        <p className="text-sm text-gray-600">First day of every month</p>
                      </div>
                    </div>
                    <Badge>Active</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="templates" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Report Templates</CardTitle>
                <CardDescription>Pre-configured report templates</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {[
                    { name: "Student Progress Report", icon: Users },
                    { name: "Attendance Analysis", icon: Calendar },
                    { name: "Course Enrollment", icon: FileText },
                    { name: "Teacher Performance", icon: BarChart3 },
                    { name: "Financial Summary", icon: TrendingUp },
                    { name: "Custom Report", icon: FileText }
                  ].map((template, index) => (
                    <div key={index} className="p-4 border rounded-lg hover:shadow-md transition-shadow cursor-pointer">
                      <div className="flex items-center gap-3 mb-3">
                        <template.icon className="h-5 w-5 text-blue-600" />
                        <h3 className="font-semibold">{template.name}</h3>
                      </div>
                      <Button size="sm" variant="outline" className="w-full">
                        Generate
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
};

export default StaffReports;
