import { useState, useEffect, useCallback } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";
import { useToast } from "@/hooks/use-toast";
import { 
  Plus, Edit, Trash2, Eye, FileText, Clock, Users, 
  BookOpen, Target, CheckCircle, AlertTriangle, Calendar,
  GraduationCap, Award, TrendingUp, BarChart3, Settings
} from "lucide-react";
import { 
  examinationsAPI, 
  coursesAPI, 
  type ExamData, 
  type TestData, 
  type CourseData,
  type ExamResultData,
  type TestAttemptData
} from "@/lib/api";

interface Assessment {
  id: number;
  title: string;
  type: 'assignment' | 'test' | 'exam';
  course: number;
  course_title?: string;
  dueDate?: string;
  exam_date?: string;
  start_time?: string;
  end_time?: string;
  total_marks: number;
  total_points?: number;
  passing_marks?: number;
  duration?: number;
  status: 'draft' | 'published' | 'active' | 'completed';
  submissionsCount?: number;
  totalStudents?: number;
  gradedCount?: number;
  averageScore?: number;
  is_published: boolean;
  instructions?: string;
  created_at?: string;
  updated_at?: string;
}

interface AssessmentFormData {
  title: string;
  description: string;
  type: 'assignment' | 'test' | 'exam';
  course: number | string;
  dueDate?: string;
  exam_date?: string;
  start_time?: string;
  end_time?: string;
  total_marks: number;
  passing_marks: number;
  duration: number;
  instructions: string;
  max_attempts?: number;
  is_published: boolean;
}

const TeacherAssessments = () => {
  const { toast } = useToast();
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [filteredAssessments, setFilteredAssessments] = useState<Assessment[]>([]);
  const [courses, setCourses] = useState<CourseData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filters and search
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterCourse, setFilterCourse] = useState("all");
  
  // Dialogs
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isGradingDialogOpen, setIsGradingDialogOpen] = useState(false);
  const [selectedAssessment, setSelectedAssessment] = useState<Assessment | null>(null);
  
  // Form data
  const [formData, setFormData] = useState<AssessmentFormData>({
    title: '',
    description: '',
    type: 'assignment',
    course: '',
    exam_date: '',
    start_time: '',
    end_time: '',
    total_marks: 100,
    passing_marks: 50,
    duration: 60,
    instructions: '',
    max_attempts: 1,
    is_published: false
  });

  const loadAssessments = useCallback(async () => {
    try {
      setLoading(true);
      const [examsData, testsData] = await Promise.all([
        examinationsAPI.getExams(),
        examinationsAPI.getTests()
      ]);

      // Transform and combine exam and test data
      const transformedExams: Assessment[] = examsData.map((exam: ExamData) => ({
        id: exam.id!,
        title: exam.title,
        type: 'exam' as const,
        course: exam.course,
        course_title: exam.course_title,
        dueDate: exam.exam_date,
        exam_date: exam.exam_date,
        start_time: exam.start_time,
        end_time: exam.end_time,
        total_marks: exam.total_marks,
        total_points: exam.total_marks,
        passing_marks: exam.passing_marks,
        duration: exam.duration,
        status: exam.is_published ? 'published' : 'draft',
        submissionsCount: 0, // Default values for display
        totalStudents: 0,
        gradedCount: 0,
        is_published: exam.is_published,
        instructions: exam.instructions,
        created_at: exam.created_at,
        updated_at: exam.updated_at
      }));

      const transformedTests: Assessment[] = testsData.map((test: TestData) => ({
        id: test.id!,
        title: test.title,
        type: 'test' as const,
        course: test.course,
        course_title: test.course_title,
        total_marks: test.total_marks,
        total_points: test.total_marks,
        passing_marks: test.passing_marks,
        duration: test.duration,
        status: test.is_published ? 'published' : 'draft',
        submissionsCount: 0, // Default values for display
        totalStudents: 0,
        gradedCount: 0,
        is_published: test.is_published,
        instructions: test.instructions,
        created_at: test.created_at,
        updated_at: test.updated_at
      }));

      const combinedAssessments = [...transformedExams, ...transformedTests];
      setAssessments(combinedAssessments);
      setError(null);
    } catch (err) {
      console.error('Error loading assessments:', err);
      setError('Failed to load assessments');
      toast({
        title: "Error",
        description: "Failed to load assessments. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const loadCourses = useCallback(async () => {
    try {
      const coursesData = await coursesAPI.getAll();
      setCourses(coursesData);
    } catch (err) {
      console.error('Error loading courses:', err);
      toast({
        title: "Error",
        description: "Failed to load courses.",
        variant: "destructive",
      });
    }
  }, [toast]);

  // Load data on component mount
  useEffect(() => {
    loadAssessments();
    loadCourses();
  }, [loadAssessments, loadCourses]);

  useEffect(() => {
    // Filter assessments based on search and filters
    const filtered = assessments.filter(assessment => {
      const matchesSearch = assessment.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           (assessment.course_title || '').toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = filterType === "all" || assessment.type === filterType;
      const matchesStatus = filterStatus === "all" || assessment.status === filterStatus;
      const matchesCourse = filterCourse === "all" || assessment.course.toString() === filterCourse;
      
      return matchesSearch && matchesType && matchesStatus && matchesCourse;
    });
    
    setFilteredAssessments(filtered);
  }, [assessments, searchTerm, filterType, filterStatus, filterCourse]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'published': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-gray-100 text-gray-800';
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'assignment': return <FileText className="h-4 w-4" />;
      case 'test': return <BookOpen className="h-4 w-4" />;
      case 'exam': return <GraduationCap className="h-4 w-4" />;
      default: return <FileText className="h-4 w-4" />;
    }
  };

  // CRUD Operations
  const handleCreateAssessment = async () => {
    try {
      if (!formData.title || !formData.course) {
        toast({
          title: "Error",
          description: "Please fill in all required fields.",
          variant: "destructive",
        });
        return;
      }

      let createdAssessment;
      if (formData.type === 'exam') {
        const examData: ExamData = {
          title: formData.title,
          description: formData.description,
          course: Number(formData.course),
          total_marks: formData.total_marks,
          passing_marks: formData.passing_marks,
          duration: formData.duration,
          exam_date: formData.exam_date || '',
          start_time: formData.start_time || '',
          end_time: formData.end_time || '',
          is_published: formData.is_published,
          instructions: formData.instructions
        };
        createdAssessment = await examinationsAPI.createExam(examData);
      } else {
        const testData: TestData = {
          title: formData.title,
          description: formData.description,
          course: Number(formData.course),
          total_marks: formData.total_marks,
          passing_marks: formData.passing_marks,
          duration: formData.duration,
          max_attempts: formData.max_attempts || 1,
          is_published: formData.is_published,
          instructions: formData.instructions
        };
        createdAssessment = await examinationsAPI.createTest(testData);
      }

      toast({
        title: "Success",
        description: `${formData.type.charAt(0).toUpperCase() + formData.type.slice(1)} created successfully.`,
      });

      setIsCreateDialogOpen(false);
      resetForm();
      loadAssessments(); // Reload the list
    } catch (err) {
      console.error('Error creating assessment:', err);
      toast({
        title: "Error",
        description: "Failed to create assessment. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleUpdateAssessment = async () => {
    try {
      if (!selectedAssessment || !formData.title || !formData.course) {
        toast({
          title: "Error",
          description: "Please fill in all required fields.",
          variant: "destructive",
        });
        return;
      }

      if (selectedAssessment.type === 'exam') {
        const examData: Partial<ExamData> = {
          title: formData.title,
          description: formData.description,
          course: Number(formData.course),
          total_marks: formData.total_marks,
          passing_marks: formData.passing_marks,
          duration: formData.duration,
          exam_date: formData.exam_date || '',
          start_time: formData.start_time || '',
          end_time: formData.end_time || '',
          is_published: formData.is_published,
          instructions: formData.instructions
        };
        await examinationsAPI.updateExam(selectedAssessment.id, examData);
      } else {
        const testData: Partial<TestData> = {
          title: formData.title,
          description: formData.description,
          course: Number(formData.course),
          total_marks: formData.total_marks,
          passing_marks: formData.passing_marks,
          duration: formData.duration,
          max_attempts: formData.max_attempts || 1,
          is_published: formData.is_published,
          instructions: formData.instructions
        };
        await examinationsAPI.updateTest(selectedAssessment.id, testData);
      }

      toast({
        title: "Success",
        description: `${selectedAssessment.type.charAt(0).toUpperCase() + selectedAssessment.type.slice(1)} updated successfully.`,
      });

      setIsEditDialogOpen(false);
      setSelectedAssessment(null);
      resetForm();
      loadAssessments(); // Reload the list
    } catch (err) {
      console.error('Error updating assessment:', err);
      toast({
        title: "Error",
        description: "Failed to update assessment. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleDeleteAssessment = async (assessment: Assessment) => {
    try {
      if (assessment.type === 'exam') {
        await examinationsAPI.deleteExam(assessment.id);
      } else {
        await examinationsAPI.deleteTest(assessment.id);
      }

      toast({
        title: "Success",
        description: `${assessment.type.charAt(0).toUpperCase() + assessment.type.slice(1)} deleted successfully.`,
      });

      loadAssessments(); // Reload the list
    } catch (err) {
      console.error('Error deleting assessment:', err);
      toast({
        title: "Error",
        description: "Failed to delete assessment. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handlePublishAssessment = async (assessment: Assessment) => {
    try {
      if (assessment.type === 'exam') {
        await examinationsAPI.publishExam(assessment.id);
      } else {
        await examinationsAPI.publishTest(assessment.id);
      }

      toast({
        title: "Success",
        description: `${assessment.type.charAt(0).toUpperCase() + assessment.type.slice(1)} published successfully.`,
      });

      loadAssessments(); // Reload the list
    } catch (err) {
      console.error('Error publishing assessment:', err);
      toast({
        title: "Error",
        description: "Failed to publish assessment. Please try again.",
        variant: "destructive",
      });
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      type: 'assignment',
      course: '',
      exam_date: '',
      start_time: '',
      end_time: '',
      total_marks: 100,
      passing_marks: 50,
      duration: 60,
      instructions: '',
      max_attempts: 1,
      is_published: false
    });
  };

  const openEditDialog = (assessment: Assessment) => {
    setSelectedAssessment(assessment);
    setFormData({
      title: assessment.title,
      description: assessment.instructions || '',
      type: assessment.type,
      course: assessment.course,
      exam_date: assessment.exam_date || '',
      start_time: assessment.start_time || '',
      end_time: assessment.end_time || '',
      total_marks: assessment.total_marks,
      passing_marks: assessment.passing_marks || 50,
      duration: assessment.duration || 60,
      instructions: assessment.instructions || '',
      max_attempts: 1,
      is_published: assessment.is_published
    });
    setIsEditDialogOpen(true);
  };

  // Grading and analytics
  const openGradingDialog = (assessment: Assessment) => {
    setSelectedAssessment(assessment);
    setIsGradingDialogOpen(true);
  };

  const getSubmissionProgress = (assessment: Assessment) => {
    const submissions = assessment.submissionsCount || 0;
    const total = assessment.totalStudents || 0;
    return total > 0 ? (submissions / total) * 100 : 0;
  };

  const getGradingProgress = (assessment: Assessment) => {
    const submissions = assessment.submissionsCount || 0;
    const graded = assessment.gradedCount || 0;
    return submissions > 0 ? (graded / submissions) * 100 : 0;
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-32 bg-gray-200 rounded"></div>
              ))}
            </div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-40 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <Alert className="mb-6">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      </DashboardLayout>
    );
  }

  // Calculate statistics
  const totalAssessments = assessments.length;
  const activeAssessments = assessments.filter(a => a.status === 'active').length;
  const totalSubmissions = assessments.reduce((sum, a) => sum + (a.submissionsCount || 0), 0);
  const pendingGrading = assessments.reduce((sum, a) => sum + ((a.submissionsCount || 0) - (a.gradedCount || 0)), 0);

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Assessment Management</h1>
            <p className="text-gray-600 mt-1">Create and manage assignments, tests, and exams</p>
          </div>
          <Button onClick={() => setIsCreateDialogOpen(true)} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Create Assessment
          </Button>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <FileText className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Assessments</p>
                  <p className="text-2xl font-bold">{totalAssessments}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Active</p>
                  <p className="text-2xl font-bold">{activeAssessments}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Users className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Submissions</p>
                  <p className="text-2xl font-bold">{totalSubmissions}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <Award className="h-6 w-6 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Pending Grading</p>
                  <p className="text-2xl font-bold">{pendingGrading}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters and Search */}
        <Card>
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <div>
                <Label htmlFor="search">Search</Label>
                <Input
                  id="search"
                  placeholder="Search assessments..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              
              <div>
                <Label>Type</Label>
                <Select value={filterType} onValueChange={setFilterType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="assignment">Assignments</SelectItem>
                    <SelectItem value="test">Tests</SelectItem>
                    <SelectItem value="exam">Exams</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label>Status</Label>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="published">Published</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label>Course</Label>
                <Select value={filterCourse} onValueChange={setFilterCourse}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Courses</SelectItem>
                    {courses.map(course => (
                      <SelectItem key={course.id} value={course.id!.toString()}>
                        {course.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div className="flex items-end">
                <Button 
                  variant="outline" 
                  onClick={() => {
                    setSearchTerm('');
                    setFilterType('all');
                    setFilterStatus('all');
                    setFilterCourse('all');
                  }}
                >
                  Clear Filters
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Assessments List */}
        <div className="space-y-4">
          {filteredAssessments.map((assessment) => (
            <Card key={assessment.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      {getTypeIcon(assessment.type)}
                      <h3 className="text-lg font-semibold">{assessment.title}</h3>
                      <Badge className={getStatusColor(assessment.status)}>
                        {assessment.status}
                      </Badge>
                      <Badge variant="outline" className="capitalize">
                        {assessment.type}
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-600 mb-4">
                      <div className="flex items-center gap-2">
                        <BookOpen className="h-4 w-4" />
                        <span>{assessment.course_title || `Course ${assessment.course}`}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        <span>
                          {assessment.dueDate 
                            ? `Due: ${new Date(assessment.dueDate).toLocaleDateString()}`
                            : assessment.exam_date 
                            ? `Exam: ${new Date(assessment.exam_date).toLocaleDateString()}`
                            : 'No date set'
                          }
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Target className="h-4 w-4" />
                        <span>{assessment.total_marks || assessment.total_points} marks</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Users className="h-4 w-4" />
                        <span>{assessment.submissionsCount}/{assessment.totalStudents} submitted</span>
                      </div>
                    </div>

                    {/* Progress Bars */}
                    <div className="space-y-2">
                      <div>
                        <div className="flex justify-between text-xs text-gray-600 mb-1">
                          <span>Submission Progress</span>
                          <span>{Math.round(getSubmissionProgress(assessment))}%</span>
                        </div>
                        <Progress value={getSubmissionProgress(assessment)} className="h-2" />
                      </div>
                      
                      {(assessment.submissionsCount || 0) > 0 && (
                        <div>
                          <div className="flex justify-between text-xs text-gray-600 mb-1">
                            <span>Grading Progress</span>
                            <span>{Math.round(getGradingProgress(assessment))}%</span>
                          </div>
                          <Progress value={getGradingProgress(assessment)} className="h-2" />
                        </div>
                      )}
                    </div>
                    
                    {assessment.averageScore && (
                      <div className="mt-2 text-sm text-gray-600">
                        Average Score: <span className="font-medium">{assessment.averageScore?.toFixed(1)}/{assessment.total_marks || assessment.total_points}</span>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-col gap-2 ml-4">
                    <Button size="sm" variant="outline" className="flex items-center gap-1">
                      <Eye className="h-3 w-3" />
                      View
                    </Button>
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="flex items-center gap-1"
                      onClick={() => openEditDialog(assessment)}
                    >
                      <Edit className="h-3 w-3" />
                      Edit
                    </Button>
                    {assessment.status === 'draft' && (
                      <Button 
                        size="sm" 
                        className="flex items-center gap-1"
                        onClick={() => handlePublishAssessment(assessment)}
                      >
                        <CheckCircle className="h-3 w-3" />
                        Publish
                      </Button>
                    )}
                    <Button 
                      size="sm" 
                      variant="destructive" 
                      className="flex items-center gap-1"
                      onClick={() => handleDeleteAssessment(assessment)}
                    >
                      <Trash2 className="h-3 w-3" />
                      Delete
                    </Button>
                    {(assessment.submissionsCount || 0) > 0 && (
                      <Button 
                        size="sm" 
                        className="flex items-center gap-1"
                        onClick={() => openGradingDialog(assessment)}
                      >
                        <Award className="h-3 w-3" />
                        Grade
                      </Button>
                    )}
                    <Button size="sm" variant="outline" className="flex items-center gap-1">
                      <BarChart3 className="h-3 w-3" />
                      Analytics
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
          
          {filteredAssessments.length === 0 && (
            <Card>
              <CardContent className="p-12 text-center">
                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No assessments found</h3>
                <p className="text-gray-600 mb-4">
                  {searchTerm || filterType !== 'all' || filterStatus !== 'all' || filterCourse !== 'all'
                    ? 'Try adjusting your filters to see more results.'
                    : 'Create your first assessment to get started.'
                  }
                </p>
                <Button onClick={() => setIsCreateDialogOpen(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create Assessment
                </Button>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Create Assessment Dialog */}
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Create New Assessment</DialogTitle>
              <DialogDescription>
                Create a new assignment, test, or exam for your students.
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={(e) => { e.preventDefault(); handleCreateAssessment(); }} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="title">Title *</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="type">Type *</Label>
                  <Select value={formData.type} onValueChange={(value: 'assignment' | 'test' | 'exam') => setFormData(prev => ({ ...prev, type: value }))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="assignment">Assignment</SelectItem>
                      <SelectItem value="test">Test/Quiz</SelectItem>
                      <SelectItem value="exam">Exam</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  rows={3}
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="course">Course *</Label>
                  <Select value={formData.course.toString()} onValueChange={(value) => setFormData(prev => ({ ...prev, course: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select course" />
                    </SelectTrigger>
                    <SelectContent>
                      {courses.map(course => (
                        <SelectItem key={course.id} value={course.id!.toString()}>
                          {course.title}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label htmlFor="totalMarks">Total Marks *</Label>
                  <Input
                    id="totalMarks"
                    type="number"
                    min="1"
                    value={formData.total_marks}
                    onChange={(e) => setFormData(prev => ({ ...prev, total_marks: parseInt(e.target.value) }))}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="passingMarks">Passing Marks *</Label>
                  <Input
                    id="passingMarks"
                    type="number"
                    min="1"
                    value={formData.passing_marks}
                    onChange={(e) => setFormData(prev => ({ ...prev, passing_marks: parseInt(e.target.value) }))}
                    required
                  />
                </div>
              </div>
              
              {formData.type === 'exam' && (
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="examDate">Exam Date *</Label>
                    <Input
                      id="examDate"
                      type="date"
                      value={formData.exam_date}
                      onChange={(e) => setFormData(prev => ({ ...prev, exam_date: e.target.value }))}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="startTime">Start Time *</Label>
                    <Input
                      id="startTime"
                      type="time"
                      value={formData.start_time}
                      onChange={(e) => setFormData(prev => ({ ...prev, start_time: e.target.value }))}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="endTime">End Time *</Label>
                    <Input
                      id="endTime"
                      type="time"
                      value={formData.end_time}
                      onChange={(e) => setFormData(prev => ({ ...prev, end_time: e.target.value }))}
                      required
                    />
                  </div>
                </div>
              )}
              
              <div>
                <Label htmlFor="instructions">Instructions</Label>
                <Textarea
                  id="instructions"
                  value={formData.instructions}
                  onChange={(e) => setFormData(prev => ({ ...prev, instructions: e.target.value }))}
                  rows={4}
                  placeholder="Provide detailed instructions for students..."
                />
              </div>
              
              {(formData.type === 'test' || formData.type === 'exam') && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="duration">Duration (minutes)</Label>
                    <Input
                      id="duration"
                      type="number"
                      min="5"
                      value={formData.duration}
                      onChange={(e) => setFormData(prev => ({ ...prev, duration: parseInt(e.target.value) }))}
                    />
                  </div>
                  
                  {formData.type === 'test' && (
                    <div>
                      <Label htmlFor="maxAttempts">Max Attempts</Label>
                      <Input
                        id="maxAttempts"
                        type="number"
                        min="1"
                        value={formData.max_attempts}
                        onChange={(e) => setFormData(prev => ({ ...prev, max_attempts: parseInt(e.target.value) }))}
                      />
                    </div>
                  )}
                </div>
              )}
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="isPublished"
                  checked={formData.is_published}
                  onChange={(e) => setFormData(prev => ({ ...prev, is_published: e.target.checked }))}
                  className="rounded"
                  title="Publish assessment immediately"
                />
                <Label htmlFor="isPublished">Publish immediately</Label>
              </div>
              
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit">Create Assessment</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>

        {/* Edit Assessment Dialog */}
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Edit {selectedAssessment?.type ? selectedAssessment.type.charAt(0).toUpperCase() + selectedAssessment.type.slice(1) : 'Assessment'}</DialogTitle>
              <DialogDescription>
                Update the details of this {selectedAssessment?.type || 'assessment'}.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={(e) => { e.preventDefault(); handleUpdateAssessment(); }} className="space-y-4">
              <div>
                <Label htmlFor="editTitle">Title *</Label>
                <Input
                  id="editTitle"
                  value={formData.title}
                  onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                  placeholder="Enter assessment title"
                  required
                />
              </div>
              
              <div>
                <Label htmlFor="editDescription">Description</Label>
                <Textarea
                  id="editDescription"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Brief description of the assessment"
                  rows={3}
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="editType">Type *</Label>
                  <Select value={formData.type} onValueChange={(value: 'assignment' | 'test' | 'exam') => setFormData(prev => ({ ...prev, type: value }))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="assignment">Assignment</SelectItem>
                      <SelectItem value="test">Test</SelectItem>
                      <SelectItem value="exam">Exam</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label htmlFor="editCourse">Course *</Label>
                  <Select value={formData.course.toString()} onValueChange={(value) => setFormData(prev => ({ ...prev, course: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select course" />
                    </SelectTrigger>
                    <SelectContent>
                      {courses.map(course => (
                        <SelectItem key={course.id} value={course.id!.toString()}>
                          {course.title}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="editTotalMarks">Total Marks *</Label>
                  <Input
                    id="editTotalMarks"
                    type="number"
                    min="1"
                    value={formData.total_marks}
                    onChange={(e) => setFormData(prev => ({ ...prev, total_marks: parseInt(e.target.value) }))}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="editPassingMarks">Passing Marks *</Label>
                  <Input
                    id="editPassingMarks"
                    type="number"
                    min="1"
                    value={formData.passing_marks}
                    onChange={(e) => setFormData(prev => ({ ...prev, passing_marks: parseInt(e.target.value) }))}
                    required
                  />
                </div>
              </div>
              
              {formData.type === 'exam' && (
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="editExamDate">Exam Date *</Label>
                    <Input
                      id="editExamDate"
                      type="date"
                      value={formData.exam_date}
                      onChange={(e) => setFormData(prev => ({ ...prev, exam_date: e.target.value }))}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="editStartTime">Start Time *</Label>
                    <Input
                      id="editStartTime"
                      type="time"
                      value={formData.start_time}
                      onChange={(e) => setFormData(prev => ({ ...prev, start_time: e.target.value }))}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="editEndTime">End Time *</Label>
                    <Input
                      id="editEndTime"
                      type="time"
                      value={formData.end_time}
                      onChange={(e) => setFormData(prev => ({ ...prev, end_time: e.target.value }))}
                      required
                    />
                  </div>
                </div>
              )}
              
              <div>
                <Label htmlFor="editInstructions">Instructions</Label>
                <Textarea
                  id="editInstructions"
                  value={formData.instructions}
                  onChange={(e) => setFormData(prev => ({ ...prev, instructions: e.target.value }))}
                  rows={4}
                  placeholder="Provide detailed instructions for students..."
                />
              </div>
              
              {(formData.type === 'test' || formData.type === 'exam') && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="editDuration">Duration (minutes)</Label>
                    <Input
                      id="editDuration"
                      type="number"
                      min="5"
                      value={formData.duration}
                      onChange={(e) => setFormData(prev => ({ ...prev, duration: parseInt(e.target.value) }))}
                    />
                  </div>
                  
                  {formData.type === 'test' && (
                    <div>
                      <Label htmlFor="editMaxAttempts">Max Attempts</Label>
                      <Input
                        id="editMaxAttempts"
                        type="number"
                        min="1"
                        value={formData.max_attempts}
                        onChange={(e) => setFormData(prev => ({ ...prev, max_attempts: parseInt(e.target.value) }))}
                      />
                    </div>
                  )}
                </div>
              )}
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="editIsPublished"
                  checked={formData.is_published}
                  onChange={(e) => setFormData(prev => ({ ...prev, is_published: e.target.checked }))}
                  className="rounded"
                  title="Mark assessment as published"
                />
                <Label htmlFor="editIsPublished">Published</Label>
              </div>
              
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit">Update Assessment</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
};

export default TeacherAssessments;
