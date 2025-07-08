import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
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
  Filter, 
  Calendar, 
  Clock, 
  BookOpen, 
  CheckCircle, 
  AlertCircle, 
  FileText,
  Download,
  Upload,
  Eye
} from 'lucide-react';

interface Assignment {
  id: string;
  title: string;
  course: string;
  instructor: string;
  dueDate: string;
  status: 'pending' | 'submitted' | 'graded' | 'overdue';
  priority: 'low' | 'medium' | 'high';
  points: number;
  maxPoints: number;
  description: string;
  attachments: string[];
  submissionDate?: string;
  grade?: number;
  feedback?: string;
}

const StudentAssignments = () => {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const { toast } = useToast();

  // Mock data - replace with actual API call
  useEffect(() => {
    const loadAssignments = async () => {
      try {
        setLoading(true);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockAssignments: Assignment[] = [
          {
            id: '1',
            title: 'Calculus Problem Set 5',
            course: 'Calculus I',
            instructor: 'Dr. Smith',
            dueDate: '2025-07-15T23:59:00',
            status: 'pending',
            priority: 'high',
            points: 0,
            maxPoints: 100,
            description: 'Solve problems 1-25 from Chapter 8. Show all work and include graphs where appropriate.',
            attachments: ['problem_set_5.pdf'],
          },
          {
            id: '2',
            title: 'World War II Research Paper',
            course: 'World History',
            instructor: 'Prof. Johnson',
            dueDate: '2025-07-20T23:59:00',
            status: 'submitted',
            priority: 'medium',
            points: 85,
            maxPoints: 100,
            description: 'Write a 5-page research paper on the impact of World War II on global politics.',
            attachments: ['research_guidelines.pdf', 'citation_format.pdf'],
            submissionDate: '2025-07-18T14:30:00',
          },
          {
            id: '3',
            title: 'Chemistry Lab Report',
            course: 'Chemistry',
            instructor: 'Dr. Brown',
            dueDate: '2025-07-12T23:59:00',
            status: 'graded',
            priority: 'medium',
            points: 92,
            maxPoints: 100,
            description: 'Complete analysis of the acid-base titration experiment conducted in class.',
            attachments: ['lab_template.docx'],
            submissionDate: '2025-07-11T16:45:00',
            grade: 92,
            feedback: 'Excellent work! Your calculations were accurate and your analysis was thorough.',
          },
          {
            id: '4',
            title: 'Literature Essay',
            course: 'English Literature',
            instructor: 'Ms. Davis',
            dueDate: '2025-07-08T23:59:00',
            status: 'overdue',
            priority: 'high',
            points: 0,
            maxPoints: 100,
            description: 'Analyze the themes of love and sacrifice in Romeo and Juliet.',
            attachments: ['essay_prompt.pdf'],
          },
        ];
        
        setAssignments(mockAssignments);
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to load assignments. Please try again.',
          variant: 'destructive',
        });
      } finally {
        setLoading(false);
      }
    };

    loadAssignments();
  }, [toast]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'submitted': return 'bg-blue-100 text-blue-800';
      case 'graded': return 'bg-green-100 text-green-800';
      case 'overdue': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <Clock className="h-4 w-4" />;
      case 'submitted': return <Upload className="h-4 w-4" />;
      case 'graded': return <CheckCircle className="h-4 w-4" />;
      case 'overdue': return <AlertCircle className="h-4 w-4" />;
      default: return <FileText className="h-4 w-4" />;
    }
  };

  const filteredAssignments = assignments.filter(assignment => {
    const matchesSearch = assignment.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         assignment.course.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         assignment.instructor.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || assignment.status === statusFilter;
    const matchesPriority = priorityFilter === 'all' || assignment.priority === priorityFilter;
    
    return matchesSearch && matchesStatus && matchesPriority;
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

  const handleSubmitAssignment = (assignmentId: string) => {
    // TODO: Implement assignment submission
    toast({
      title: 'Not Implemented',
      description: 'Assignment submission feature will be implemented soon.',
      variant: 'default',
    });
  };

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
            <h1 className="text-3xl font-bold text-gray-900">My Assignments</h1>
            <p className="text-gray-600 mt-1">
              Track and manage your course assignments
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total Assignments</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{assignments.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Pending</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">
                {assignments.filter(a => a.status === 'pending').length}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Submitted</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">
                {assignments.filter(a => a.status === 'submitted').length}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Average Grade</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {assignments.filter(a => a.grade).length > 0 
                  ? Math.round(assignments.filter(a => a.grade).reduce((sum, a) => sum + (a.grade || 0), 0) / assignments.filter(a => a.grade).length)
                  : 'N/A'}
                {assignments.filter(a => a.grade).length > 0 && '%'}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-6">
          <div className="flex-1 min-w-64">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search assignments..."
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
              <SelectItem value="pending">Pending</SelectItem>
              <SelectItem value="submitted">Submitted</SelectItem>
              <SelectItem value="graded">Graded</SelectItem>
              <SelectItem value="overdue">Overdue</SelectItem>
            </SelectContent>
          </Select>
          <Select value={priorityFilter} onValueChange={setPriorityFilter}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by priority" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Priorities</SelectItem>
              <SelectItem value="high">High Priority</SelectItem>
              <SelectItem value="medium">Medium Priority</SelectItem>
              <SelectItem value="low">Low Priority</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Assignments List */}
        <div className="space-y-4">
          {filteredAssignments.length === 0 ? (
            <Card>
              <CardContent className="text-center py-8">
                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No assignments found matching your criteria.</p>
              </CardContent>
            </Card>
          ) : (
            filteredAssignments.map((assignment) => (
              <Card key={assignment.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{assignment.title}</h3>
                        <Badge className={`${getStatusColor(assignment.status)} border-0`}>
                          {getStatusIcon(assignment.status)}
                          <span className="ml-1 capitalize">{assignment.status}</span>
                        </Badge>
                        <span className={`text-sm font-medium ${getPriorityColor(assignment.priority)}`}>
                          {assignment.priority.charAt(0).toUpperCase() + assignment.priority.slice(1)} Priority
                        </span>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <BookOpen className="h-4 w-4" />
                          {assignment.course}
                        </div>
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          Due: {formatDate(assignment.dueDate)}
                        </div>
                        {assignment.grade && (
                          <div className="flex items-center gap-1">
                            <CheckCircle className="h-4 w-4" />
                            Grade: {assignment.grade}/{assignment.maxPoints}
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        <Eye className="h-4 w-4 mr-2" />
                        View
                      </Button>
                      {assignment.status === 'pending' && (
                        <Button 
                          size="sm" 
                          onClick={() => handleSubmitAssignment(assignment.id)}
                        >
                          <Upload className="h-4 w-4 mr-2" />
                          Submit
                        </Button>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 mb-3">{assignment.description}</p>
                  {assignment.attachments.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3">
                      {assignment.attachments.map((attachment, index) => (
                        <Badge key={index} variant="secondary" className="cursor-pointer hover:bg-gray-300">
                          <Download className="h-3 w-3 mr-1" />
                          {attachment}
                        </Badge>
                      ))}
                    </div>
                  )}
                  {assignment.feedback && (
                    <Alert>
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        <strong>Feedback:</strong> {assignment.feedback}
                      </AlertDescription>
                    </Alert>
                  )}
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default StudentAssignments;
