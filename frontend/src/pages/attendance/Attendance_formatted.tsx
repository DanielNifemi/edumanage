import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Calendar, TrendingUp, Clock, Users, CheckCircle, XCircle, AlertTriangle, Plus, UserCheck, Search, Calendar as CalendarIcon, BarChart3 } from "lucide-react";
import { useState, useEffect } from "react";
import { attendanceAPI, studentsAPI, AttendanceData, StudentData } from "@/lib/api";
import { toast } from "sonner";

interface AttendanceRecord {
  id: string;
  student: {
    id: string;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
  };
  date: string;
  is_present: boolean;
  notes?: string;
}

interface AttendanceStats {
  totalClasses: number;
  attended: number;
  absent: number;
  late: number;
  percentage: number;
}

interface AttendanceFormData {
  student_id: string;
  date: string;
  is_present: boolean;
  notes: string;
}

interface CourseAttendance {
  course: string;
  attended: number;
  total: number;
  percentage: number;
}

interface RecentAttendanceRecord {
  course: string;
  date: string;
  time: string;
  status: string;
}

const Attendance = () => {
  const [currentView, setCurrentView] = useState<'student' | 'teacher'>('student');
  const [attendanceRecords, setAttendanceRecords] = useState<AttendanceRecord[]>([]);
  const [students, setStudents] = useState<StudentData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedMonth] = useState(new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' }));
  const [attendanceStats, setAttendanceStats] = useState<AttendanceStats>({
    totalClasses: 0,
    attended: 0,
    absent: 0,
    late: 0,
    percentage: 0
  });

  // Dialog states
  const [showMarkDialog, setShowMarkDialog] = useState(false);
  const [showBulkDialog, setShowBulkDialog] = useState(false);
  const [showReportDialog, setShowReportDialog] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<StudentData | null>(null);

  // Form data
  const [formData, setFormData] = useState<AttendanceFormData>({
    student_id: "",
    date: new Date().toISOString().split('T')[0],
    is_present: true,
    notes: ""
  });

  const [bulkAttendanceDate, setBulkAttendanceDate] = useState(new Date().toISOString().split('T')[0]);
  const [bulkAttendanceData, setBulkAttendanceData] = useState<{ [key: string]: boolean }>({});

  // Mock data for demonstration
  const [courseAttendance] = useState<CourseAttendance[]>([
    { course: "Mathematics", attended: 18, total: 20, percentage: 90 },
    { course: "Physics", attended: 16, total: 18, percentage: 89 },
    { course: "Chemistry", attended: 14, total: 16, percentage: 88 },
    { course: "Biology", attended: 17, total: 19, percentage: 89 }
  ]);

  const [recentAttendance] = useState<RecentAttendanceRecord[]>([
    { course: "Mathematics", date: "2024-01-15", time: "09:00 AM", status: "present" },
    { course: "Physics", date: "2024-01-14", time: "11:00 AM", status: "present" },
    { course: "Chemistry", date: "2024-01-13", time: "02:00 PM", status: "late" },
    { course: "Biology", date: "2024-01-12", time: "10:00 AM", status: "present" },
    { course: "Mathematics", date: "2024-01-11", time: "09:00 AM", status: "absent" }
  ]);

  useEffect(() => {
    fetchData();
  }, [currentView, selectedDate]);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      if (currentView === 'teacher') {
        const [studentsResponse] = await Promise.all([
          studentsAPI.getAll()
        ]);
        setStudents(studentsResponse);
        
        // Initialize bulk attendance data
        const initialBulkData: { [key: string]: boolean } = {};
        studentsResponse.forEach((student: StudentData) => {
          initialBulkData[student.id || ''] = true;
        });
        setBulkAttendanceData(initialBulkData);
      } else {
        // For student view, fetch their attendance records
        setAttendanceRecords([]);
        calculateStats([]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to fetch attendance data');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (records: AttendanceRecord[]) => {
    const totalClasses = records.length || courseAttendance.reduce((sum, course) => sum + course.total, 0);
    const attended = records.filter(r => r.is_present).length || courseAttendance.reduce((sum, course) => sum + course.attended, 0);
    const absent = totalClasses - attended;
    const percentage = totalClasses > 0 ? (attended / totalClasses) * 100 : 0;
    
    setAttendanceStats({
      totalClasses,
      attended,
      absent,
      late: 0, // Would need additional status field in backend
      percentage: Math.round(percentage * 10) / 10
    });
  };

  const handleMarkAttendance = async () => {
    try {
      const attendanceData: AttendanceData = {
        student_id: formData.student_id,
        course_id: "1", // Would be dynamic based on current class
        date: formData.date,
        status: formData.is_present ? 'present' : 'absent',
        notes: formData.notes
      };

      await attendanceAPI.markAttendance(attendanceData);
      toast.success('Attendance marked successfully');
      setShowMarkDialog(false);
      setFormData({
        student_id: "",
        date: new Date().toISOString().split('T')[0],
        is_present: true,
        notes: ""
      });
      fetchData();
    } catch (error) {
      console.error('Error marking attendance:', error);
      toast.error('Failed to mark attendance');
    }
  };

  const handleBulkAttendance = async () => {
    try {
      const attendancePromises = Object.entries(bulkAttendanceData).map(([studentId, isPresent]) => {
        const attendanceData: AttendanceData = {
          student_id: studentId,
          course_id: "1", // Would be dynamic
          date: bulkAttendanceDate,
          status: isPresent ? 'present' : 'absent'
        };
        return attendanceAPI.markAttendance(attendanceData);
      });

      await Promise.all(attendancePromises);
      toast.success('Bulk attendance marked successfully');
      setShowBulkDialog(false);
      fetchData();
    } catch (error) {
      console.error('Error marking bulk attendance:', error);
      toast.error('Failed to mark bulk attendance');
    }
  };

  const filteredStudents = students.filter(student =>
    `${student.first_name} ${student.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredRecords = attendanceRecords.filter(record =>
    `${record.student.first_name} ${record.student.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.date.includes(searchTerm)
  );

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "present":
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "absent":
        return <XCircle className="h-4 w-4 text-red-500" />;
      case "late":
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "present": return "bg-green-100 text-green-800";
      case "absent": return "bg-red-100 text-red-800";
      case "late": return "bg-yellow-100 text-yellow-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getPercentageColor = (percentage: number) => {
    if (percentage >= 90) return "text-green-600";
    if (percentage >= 75) return "text-yellow-600";
    return "text-red-600";
  };

  useEffect(() => {
    // Calculate stats when course attendance data is available
    calculateStats([]);
  }, [courseAttendance]);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading attendance data...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header with View Toggle */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {currentView === 'student' ? 'My Attendance' : 'Manage Attendance'}
            </h1>
            <p className="text-gray-600">
              {currentView === 'student' 
                ? 'Track your class attendance and performance'
                : 'Mark and manage student attendance'
              }
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex bg-gray-100 rounded-lg p-1">
              <Button
                variant={currentView === 'student' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setCurrentView('student')}
              >
                Student View
              </Button>
              <Button
                variant={currentView === 'teacher' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setCurrentView('teacher')}
              >
                Teacher View
              </Button>
            </div>
            {currentView === 'teacher' && (
              <div className="flex gap-2">
                <Button onClick={() => setShowMarkDialog(true)} className="flex items-center gap-2">
                  <Plus className="h-4 w-4" />
                  Mark Attendance
                </Button>
                <Button onClick={() => setShowBulkDialog(true)} variant="outline" className="flex items-center gap-2">
                  <UserCheck className="h-4 w-4" />
                  Bulk Mark
                </Button>
                <Button onClick={() => setShowReportDialog(true)} variant="outline" className="flex items-center gap-2">
                  <BarChart3 className="h-4 w-4" />
                  Generate Report
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Overall Stats */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Classes</p>
                  <p className="text-2xl font-bold text-gray-900">{attendanceStats.totalClasses}</p>
                </div>
                <Users className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Attended</p>
                  <p className="text-2xl font-bold text-green-600">{attendanceStats.attended}</p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Absent</p>
                  <p className="text-2xl font-bold text-red-600">{attendanceStats.absent}</p>
                </div>
                <XCircle className="h-8 w-8 text-red-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Late</p>
                  <p className="text-2xl font-bold text-yellow-600">{attendanceStats.late}</p>
                </div>
                <Clock className="h-8 w-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-0 shadow-md">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Percentage</p>
                  <p className={`text-2xl font-bold ${getPercentageColor(attendanceStats.percentage)}`}>
                    {attendanceStats.percentage}%
                  </p>
                </div>
                <TrendingUp className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {currentView === 'student' ? (
          // Student View - Recent attendance and course breakdown
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Course Attendance Breakdown */}
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Course Attendance
                </CardTitle>
                <CardDescription>Your attendance percentage by subject</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {courseAttendance.map((course, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <h4 className="font-medium text-gray-900">{course.course}</h4>
                        <div className="text-right">
                          <span className={`font-semibold ${getPercentageColor(course.percentage)}`}>
                            {course.percentage}%
                          </span>
                          <p className="text-sm text-gray-500">
                            {course.attended}/{course.total} classes
                          </p>
                        </div>
                      </div>
                      <Progress value={course.percentage} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recent Attendance */}
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Recent Attendance
                </CardTitle>
                <CardDescription>Your latest class attendance records</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentAttendance.map((record, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        {getStatusIcon(record.status)}
                        <div>
                          <h5 className="font-medium text-gray-900">{record.course}</h5>
                          <p className="text-sm text-gray-500">
                            {new Date(record.date).toLocaleDateString()} at {record.time}
                          </p>
                        </div>
                      </div>
                      <Badge className={getStatusColor(record.status)}>
                        {record.status.charAt(0).toUpperCase() + record.status.slice(1)}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        ) : (
          // Teacher View - Student management and bulk actions
          <div className="space-y-6">
            {/* Search and Filters */}
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <UserCheck className="h-5 w-5" />
                  Student Attendance Management
                </CardTitle>
                <CardDescription>Mark and manage attendance for your students</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4 mb-6">
                  <div className="flex-1">
                    <Label htmlFor="search">Search Students</Label>
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="search"
                        placeholder="Search by name or email..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="date">Date</Label>
                    <Input
                      id="date"
                      type="date"
                      value={selectedDate}
                      onChange={(e) => setSelectedDate(e.target.value)}
                    />
                  </div>
                </div>

                {/* Students Table */}
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Student</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredStudents.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center py-8 text-gray-500">
                          {loading ? 'Loading students...' : 'No students found'}
                        </TableCell>
                      </TableRow>
                    ) : (
                      filteredStudents.map((student) => (
                        <TableRow key={student.id}>
                          <TableCell>
                            <div>
                              <p className="font-medium">{student.first_name} {student.last_name}</p>
                              <p className="text-sm text-gray-600">{student.student_id}</p>
                            </div>
                          </TableCell>
                          <TableCell>{student.email}</TableCell>
                          <TableCell>
                            <Badge className="bg-gray-100 text-gray-800">
                              Not Marked
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex gap-2">
                              <Button size="sm" onClick={() => {
                                setSelectedStudent(student);
                                setFormData(prev => ({ ...prev, student_id: student.id || '' }));
                                setShowMarkDialog(true);
                              }}>
                                Mark
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Monthly Calendar View */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CalendarIcon className="h-5 w-5" />
              Attendance Calendar
            </CardTitle>
            <CardDescription>Monthly view of attendance ({selectedMonth})</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-7 gap-2 mb-4">
              {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                <div key={day} className="p-2 text-center font-medium text-gray-600 bg-gray-50 rounded">
                  {day}
                </div>
              ))}
            </div>
            
            <div className="grid grid-cols-7 gap-2">
              {Array.from({ length: 31 }, (_, i) => i + 1).map((day) => {
                const hasClass = Math.random() > 0.3; // Mock data
                const status = hasClass ? (Math.random() > 0.9 ? 'absent' : Math.random() > 0.8 ? 'late' : 'present') : null;
                
                return (
                  <div
                    key={day}
                    className={`p-3 text-center rounded cursor-pointer transition-colors ${
                      !hasClass
                        ? 'text-gray-400'
                        : status === 'present'
                        ? 'bg-green-100 text-green-800 hover:bg-green-200'
                        : status === 'late'
                        ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                        : 'bg-red-100 text-red-800 hover:bg-red-200'
                    }`}
                  >
                    <div className="font-medium">{day}</div>
                    {hasClass && (
                      <div className="text-xs mt-1">
                        {status === 'present' ? '✓' : status === 'late' ? '⚠' : '✗'}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
            
            <div className="flex items-center gap-6 mt-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-100 rounded"></div>
                <span>Present</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-yellow-100 rounded"></div>
                <span>Late</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-red-100 rounded"></div>
                <span>Absent</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-gray-100 rounded"></div>
                <span>No Class</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Mark Attendance Dialog */}
        <Dialog open={showMarkDialog} onOpenChange={setShowMarkDialog}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Mark Attendance</DialogTitle>
              <DialogDescription>
                Mark attendance for {selectedStudent?.first_name} {selectedStudent?.last_name}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="attendance-date">Date</Label>
                <Input
                  id="attendance-date"
                  type="date"
                  value={formData.date}
                  onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
                />
              </div>
              <div>
                <Label htmlFor="attendance-status">Status</Label>
                <Select 
                  value={formData.is_present.toString()} 
                  onValueChange={(value) => setFormData(prev => ({ ...prev, is_present: value === 'true' }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="true">Present</SelectItem>
                    <SelectItem value="false">Absent</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="attendance-notes">Notes (Optional)</Label>
                <Textarea
                  id="attendance-notes"
                  placeholder="Add any notes..."
                  value={formData.notes}
                  onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                />
              </div>
              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={() => setShowMarkDialog(false)}>
                  Cancel
                </Button>
                <Button onClick={handleMarkAttendance}>
                  Mark Attendance
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>

        {/* Bulk Attendance Dialog */}
        <Dialog open={showBulkDialog} onOpenChange={setShowBulkDialog}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Bulk Mark Attendance</DialogTitle>
              <DialogDescription>
                Mark attendance for all students at once
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="bulk-date">Date</Label>
                <Input
                  id="bulk-date"
                  type="date"
                  value={bulkAttendanceDate}
                  onChange={(e) => setBulkAttendanceDate(e.target.value)}
                />
              </div>
              <div className="max-h-64 overflow-y-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Student</TableHead>
                      <TableHead>Present</TableHead>
                      <TableHead>Absent</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {students.map((student) => (
                      <TableRow key={student.id}>
                        <TableCell>
                          <div>
                            <p className="font-medium">{student.first_name} {student.last_name}</p>
                            <p className="text-sm text-gray-600">{student.student_id}</p>
                          </div>
                        </TableCell>
                        <TableCell>
                          <input
                            type="radio"
                            name={`attendance-${student.id}`}
                            checked={bulkAttendanceData[student.id || ''] === true}
                            onChange={() => setBulkAttendanceData(prev => ({ ...prev, [student.id || '']: true }))}
                          />
                        </TableCell>
                        <TableCell>
                          <input
                            type="radio"
                            name={`attendance-${student.id}`}
                            checked={bulkAttendanceData[student.id || ''] === false}
                            onChange={() => setBulkAttendanceData(prev => ({ ...prev, [student.id || '']: false }))}
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={() => setShowBulkDialog(false)}>
                  Cancel
                </Button>
                <Button onClick={handleBulkAttendance}>
                  Mark All Attendance
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>

        {/* Report Dialog */}
        <Dialog open={showReportDialog} onOpenChange={setShowReportDialog}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Generate Attendance Report</DialogTitle>
              <DialogDescription>
                Generate detailed attendance reports for analysis
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="report-start">Start Date</Label>
                <Input id="report-start" type="date" />
              </div>
              <div>
                <Label htmlFor="report-end">End Date</Label>
                <Input id="report-end" type="date" />
              </div>
              <div>
                <Label htmlFor="report-student">Student (Optional)</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a student or leave empty for all" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Students</SelectItem>
                    {students.map((student) => (
                      <SelectItem key={student.id} value={student.id || ''}>
                        {student.first_name} {student.last_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={() => setShowReportDialog(false)}>
                  Cancel
                </Button>
                <Button onClick={() => toast.success('Report generation feature coming soon!')}>
                  Generate Report
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
};

export default Attendance;
