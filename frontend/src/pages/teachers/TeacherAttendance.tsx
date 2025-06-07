
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar, Users, CheckCircle, XCircle, Clock } from "lucide-react";
import { useState } from "react";

const TeacherAttendance = () => {
  const [selectedClass, setSelectedClass] = useState("CS101");

  const classes = [
    { code: "CS101", name: "Computer Science 101" },
    { code: "CS201", name: "Data Structures" },
    { code: "CS305", name: "Web Development" }
  ];

  const attendanceData = [
    {
      date: "2024-03-15",
      present: 26,
      absent: 2,
      total: 28,
      percentage: 93
    },
    {
      date: "2024-03-13",
      present: 25,
      absent: 3,
      total: 28,
      percentage: 89
    },
    {
      date: "2024-03-11",
      present: 28,
      absent: 0,
      total: 28,
      percentage: 100
    }
  ];

  const students = [
    { id: 1, name: "Alice Johnson", status: "Present", email: "alice@school.edu" },
    { id: 2, name: "Bob Smith", status: "Present", email: "bob@school.edu" },
    { id: 3, name: "Charlie Brown", status: "Absent", email: "charlie@school.edu" },
    { id: 4, name: "Diana Ross", status: "Present", email: "diana@school.edu" },
    { id: 5, name: "Edward Norton", status: "Present", email: "edward@school.edu" }
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Attendance Management</h1>
            <p className="text-gray-600">Track and manage student attendance</p>
          </div>
          <Button>Take Attendance</Button>
        </div>

        {/* Class Selection */}
        <Card className="border-0 shadow-md">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium">Select Class:</label>
              <Select value={selectedClass} onValueChange={setSelectedClass}>
                <SelectTrigger className="w-64">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {classes.map((cls) => (
                    <SelectItem key={cls.code} value={cls.code}>
                      {cls.code} - {cls.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Attendance Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Average Attendance</p>
                  <p className="text-2xl font-bold text-green-600">94%</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Users className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Students</p>
                  <p className="text-2xl font-bold text-blue-600">28</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-orange-100 rounded-lg">
                  <Clock className="h-6 w-6 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Classes This Week</p>
                  <p className="text-2xl font-bold text-orange-600">3</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Attendance */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle>Recent Attendance</CardTitle>
            <CardDescription>Attendance records for the selected class</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {attendanceData.map((record, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-4">
                    <Calendar className="h-5 w-5 text-gray-500" />
                    <div>
                      <p className="font-medium">{record.date}</p>
                      <p className="text-sm text-gray-600">
                        {record.present} present, {record.absent} absent
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <Badge variant={record.percentage >= 90 ? "default" : "destructive"}>
                      {record.percentage}%
                    </Badge>
                    <Button size="sm" variant="outline">View Details</Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Today's Attendance */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle>Today's Attendance</CardTitle>
            <CardDescription>Mark attendance for today's class</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {students.map((student) => (
                <div key={student.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <p className="font-medium">{student.name}</p>
                    <p className="text-sm text-gray-600">{student.email}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant={student.status === 'Present' ? 'default' : 'destructive'}>
                      {student.status === 'Present' ? (
                        <CheckCircle className="h-3 w-3 mr-1" />
                      ) : (
                        <XCircle className="h-3 w-3 mr-1" />
                      )}
                      {student.status}
                    </Badge>
                    <Button size="sm" variant="outline">
                      {student.status === 'Present' ? 'Mark Absent' : 'Mark Present'}
                    </Button>
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

export default TeacherAttendance;
