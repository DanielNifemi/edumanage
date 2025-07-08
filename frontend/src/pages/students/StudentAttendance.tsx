import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useToast } from '@/hooks/use-toast';
import { 
  Search, 
  Calendar, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  User,
  BookOpen,
  TrendingUp,
  Download,
  Filter
} from 'lucide-react';

interface AttendanceRecord {
  id: string;
  date: string;
  course: string;
  instructor: string;
  status: 'present' | 'absent' | 'late' | 'excused';
  notes?: string;
  duration: number; // in minutes
}

interface AttendanceSummary {
  totalClasses: number;
  present: number;
  absent: number;
  late: number;
  excused: number;
  attendanceRate: number;
}

const StudentAttendance = () => {
  const [attendance, setAttendance] = useState<AttendanceRecord[]>([]);
  const [summary, setSummary] = useState<AttendanceSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [courseFilter, setCourseFilter] = useState('all');
  const [dateRange, setDateRange] = useState('30'); // days
  const { toast } = useToast();

  // Mock data - replace with actual API call
  useEffect(() => {
    const loadAttendance = async () => {
      try {
        setLoading(true);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockAttendance: AttendanceRecord[] = [
          {
            id: '1',
            date: '2025-07-07T09:00:00',
            course: 'Calculus I',
            instructor: 'Dr. Smith',
            status: 'present',
            duration: 90,
          },
          {
            id: '2',
            date: '2025-07-07T14:00:00',
            course: 'World History',
            instructor: 'Prof. Johnson',
            status: 'late',
            notes: 'Arrived 15 minutes late',
            duration: 75,
          },
          {
            id: '3',
            date: '2025-07-06T10:00:00',
            course: 'Chemistry',
            instructor: 'Dr. Brown',
            status: 'present',
            duration: 120,
          },
          {
            id: '4',
            date: '2025-07-06T13:00:00',
            course: 'English Literature',
            instructor: 'Ms. Davis',
            status: 'absent',
            notes: 'Sick leave',
            duration: 90,
          },
          {
            id: '5',
            date: '2025-07-05T09:00:00',
            course: 'Calculus I',
            instructor: 'Dr. Smith',
            status: 'present',
            duration: 90,
          },
          {
            id: '6',
            date: '2025-07-05T14:00:00',
            course: 'World History',
            instructor: 'Prof. Johnson',
            status: 'excused',
            notes: 'Medical appointment',
            duration: 90,
          },
        ];
        
        setAttendance(mockAttendance);
        
        // Calculate summary
        const totalClasses = mockAttendance.length;
        const present = mockAttendance.filter(a => a.status === 'present').length;
        const absent = mockAttendance.filter(a => a.status === 'absent').length;
        const late = mockAttendance.filter(a => a.status === 'late').length;
        const excused = mockAttendance.filter(a => a.status === 'excused').length;
        
        setSummary({
          totalClasses,
          present,
          absent,
          late,
          excused,
          attendanceRate: ((present + late + excused) / totalClasses) * 100,
        });
        
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to load attendance data. Please try again.',
          variant: 'destructive',
        });
      } finally {
        setLoading(false);
      }
    };

    loadAttendance();
  }, [toast]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'present': return 'bg-green-100 text-green-800';
      case 'absent': return 'bg-red-100 text-red-800';
      case 'late': return 'bg-yellow-100 text-yellow-800';
      case 'excused': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'present': return <CheckCircle className="h-4 w-4" />;
      case 'absent': return <AlertCircle className="h-4 w-4" />;
      case 'late': return <Clock className="h-4 w-4" />;
      case 'excused': return <User className="h-4 w-4" />;
      default: return <Calendar className="h-4 w-4" />;
    }
  };

  const filteredAttendance = attendance.filter(record => {
    const matchesSearch = record.course.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         record.instructor.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || record.status === statusFilter;
    const matchesCourse = courseFilter === 'all' || record.course === courseFilter;
    
    return matchesSearch && matchesStatus && matchesCourse;
  });

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const uniqueCourses = [...new Set(attendance.map(a => a.course))];

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="h-32 bg-gray-200 rounded"></div>
            <div className="h-32 bg-gray-200 rounded"></div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Attendance</h1>
            <p className="text-gray-600 mt-1">
              Track your class attendance and punctuality
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export Report
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Total Classes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary.totalClasses}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Present</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">{summary.present}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Absent</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-red-600">{summary.absent}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Late</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-yellow-600">{summary.late}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Attendance Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <div className="text-2xl font-bold text-blue-600">
                    {summary.attendanceRate.toFixed(1)}%
                  </div>
                  <TrendingUp className="h-5 w-5 text-blue-600" />
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Attendance Rate Alert */}
        {summary && summary.attendanceRate < 80 && (
          <Alert className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              <strong>Attendance Warning:</strong> Your attendance rate is below 80%. 
              Please consult with your academic advisor if you need assistance.
            </AlertDescription>
          </Alert>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-6">
          <div className="flex-1 min-w-64">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search courses or instructors..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="present">Present</SelectItem>
              <SelectItem value="absent">Absent</SelectItem>
              <SelectItem value="late">Late</SelectItem>
              <SelectItem value="excused">Excused</SelectItem>
            </SelectContent>
          </Select>
          <Select value={courseFilter} onValueChange={setCourseFilter}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by course" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Courses</SelectItem>
              {uniqueCourses.map(course => (
                <SelectItem key={course} value={course}>{course}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Attendance Records */}
        <div className="space-y-4">
          {filteredAttendance.length === 0 ? (
            <Card>
              <CardContent className="text-center py-8">
                <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No attendance records found matching your criteria.</p>
              </CardContent>
            </Card>
          ) : (
            filteredAttendance.map((record) => (
              <Card key={record.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{record.course}</h3>
                        <Badge className={`${getStatusColor(record.status)} border-0`}>
                          {getStatusIcon(record.status)}
                          <span className="ml-1 capitalize">{record.status}</span>
                        </Badge>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <User className="h-4 w-4" />
                          {record.instructor}
                        </div>
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {formatDate(record.date)}
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          {formatDuration(record.duration)}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                {record.notes && (
                  <CardContent>
                    <Alert>
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        <strong>Notes:</strong> {record.notes}
                      </AlertDescription>
                    </Alert>
                  </CardContent>
                )}
              </Card>
            ))
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default StudentAttendance;
