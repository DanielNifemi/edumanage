import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BarChart3, Download, TrendingUp, Users, BookOpen, GraduationCap } from "lucide-react";

const AdminReports = () => {
  const reportData = {
    students: {
      total: 1250,
      active: 1180,
      inactive: 70,
      newThisMonth: 45
    },
    teachers: {
      total: 85,
      active: 82,
      onLeave: 3
    },
    courses: {
      total: 156,
      active: 142,
      completed: 14
    },
    attendance: {
      average: 94.2,
      trend: "up"
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
            <p className="text-gray-600">Comprehensive insights and data analysis</p>
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
            <Button className="flex items-center gap-2">
              <Download className="h-4 w-4" />
              Export
            </Button>
          </div>
        </div>

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Users className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Students</p>
                  <p className="text-2xl font-bold">{reportData.students.total}</p>
                  <p className="text-xs text-green-600">+{reportData.students.newThisMonth} this month</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <GraduationCap className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Active Teachers</p>
                  <p className="text-2xl font-bold">{reportData.teachers.active}</p>
                  <p className="text-xs text-gray-500">{reportData.teachers.onLeave} on leave</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <BookOpen className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Active Courses</p>
                  <p className="text-2xl font-bold">{reportData.courses.active}</p>
                  <p className="text-xs text-gray-500">{reportData.courses.completed} completed</p>
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
                  <p className="text-sm text-gray-600">Avg Attendance</p>
                  <p className="text-2xl font-bold">{reportData.attendance.average}%</p>
                  <p className="text-xs text-green-600">↗ 2.3% from last month</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="enrollment" className="space-y-4">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="enrollment">Enrollment</TabsTrigger>
            <TabsTrigger value="attendance">Attendance</TabsTrigger>
            <TabsTrigger value="performance">Performance</TabsTrigger>
            <TabsTrigger value="financial">Financial</TabsTrigger>
          </TabsList>

          <TabsContent value="enrollment" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Student Enrollment Trends</CardTitle>
                <CardDescription>Monthly enrollment statistics and trends</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
                  <div className="text-center">
                    <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">Enrollment chart would be displayed here</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="attendance" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Attendance Analytics</CardTitle>
                <CardDescription>Attendance patterns and insights</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-green-100 rounded-lg">
          <h3 className="font-semibold text-green-800">Excellent ({'>'}95%)</h3>
          <p className="text-3xl font-bold text-green-600">68%</p>
          <p className="text-sm text-green-600">of students</p>
        </div>
        <div className="p-4 bg-yellow-100 rounded-lg">
          <h3 className="font-semibold text-yellow-800">Good (85-95%)</h3>
          <p className="text-3xl font-bold text-yellow-600">24%</p>
          <p className="text-sm text-yellow-600">of students</p>
        </div>
        <div className="p-4 bg-red-100 rounded-lg">
          <h3 className="font-semibold text-red-800">Needs Attention ({'<'}85%)</h3>
          <p className="text-3xl font-bold text-red-600">8%</p>
          <p className="text-sm text-red-600">of students</p>
        </div>
      </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="performance" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Academic Performance</CardTitle>
                <CardDescription>Grade distribution and performance metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                    {['A', 'B', 'C', 'D', 'F'].map((grade, index) => (
                      <div key={grade} className="p-4 bg-gray-50 rounded-lg text-center">
                        <h3 className="font-semibold text-gray-800">Grade {grade}</h3>
                        <p className="text-2xl font-bold text-blue-600">
                          {[25, 35, 25, 10, 5][index]}%
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="financial" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Financial Overview</CardTitle>
                <CardDescription>Revenue and financial metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h3 className="font-semibold text-blue-800">Total Revenue</h3>
                    <p className="text-2xl font-bold text-blue-600">$2.4M</p>
                    <p className="text-sm text-blue-600">This year</p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <h3 className="font-semibold text-green-800">Outstanding Fees</h3>
                    <p className="text-2xl font-bold text-green-600">$125K</p>
                    <p className="text-sm text-green-600">5.2% of total</p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <h3 className="font-semibold text-purple-800">Monthly Growth</h3>
                    <p className="text-2xl font-bold text-purple-600">+12%</p>
                    <p className="text-sm text-purple-600">vs last month</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
};

export default AdminReports;
