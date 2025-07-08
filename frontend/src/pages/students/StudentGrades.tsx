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
  TrendingUp, 
  BookOpen, 
  User,
  Award,
  FileText,
  Download,
  Eye
} from 'lucide-react';

interface Grade {
  id: string;
  assignment: string;
  course: string;
  instructor: string;
  category: 'homework' | 'quiz' | 'exam' | 'project' | 'participation';
  points: number;
  maxPoints: number;
  percentage: number;
  letterGrade: string;
  submissionDate: string;
  gradedDate: string;
  feedback?: string;
  weight: number; // percentage weight in final grade
}

interface CourseGrade {
  course: string;
  instructor: string;
  currentGrade: number;
  letterGrade: string;
  creditHours: number;
  assignments: Grade[];
}

const StudentGrades = () => {
  const [grades, setGrades] = useState<Grade[]>([]);
  const [courseGrades, setCourseGrades] = useState<CourseGrade[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [courseFilter, setCourseFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [viewMode, setViewMode] = useState<'assignments' | 'courses'>('assignments');
  const { toast } = useToast();

  // Mock data - replace with actual API call
  useEffect(() => {
    const loadGrades = async () => {
      try {
        setLoading(true);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockGrades: Grade[] = [
          {
            id: '1',
            assignment: 'Problem Set 4',
            course: 'Calculus I',
            instructor: 'Dr. Smith',
            category: 'homework',
            points: 85,
            maxPoints: 100,
            percentage: 85,
            letterGrade: 'B',
            submissionDate: '2025-07-01T23:59:00',
            gradedDate: '2025-07-03T10:00:00',
            feedback: 'Good work on integration problems. Watch your algebraic manipulation.',
            weight: 10,
          },
          {
            id: '2',
            assignment: 'Midterm Exam',
            course: 'Calculus I',
            instructor: 'Dr. Smith',
            category: 'exam',
            points: 78,
            maxPoints: 100,
            percentage: 78,
            letterGrade: 'C+',
            submissionDate: '2025-06-28T14:00:00',
            gradedDate: '2025-06-30T12:00:00',
            feedback: 'Review limits and derivatives. See me during office hours.',
            weight: 25,
          },
          {
            id: '3',
            assignment: 'Research Paper',
            course: 'World History',
            instructor: 'Prof. Johnson',
            category: 'project',
            points: 92,
            maxPoints: 100,
            percentage: 92,
            letterGrade: 'A-',
            submissionDate: '2025-07-05T23:59:00',
            gradedDate: '2025-07-07T16:00:00',
            feedback: 'Excellent research and analysis. Well-written and thoroughly sourced.',
            weight: 30,
          },
          {
            id: '4',
            assignment: 'Lab Report 3',
            course: 'Chemistry',
            instructor: 'Dr. Brown',
            category: 'homework',
            points: 88,
            maxPoints: 100,
            percentage: 88,
            letterGrade: 'B+',
            submissionDate: '2025-07-02T23:59:00',
            gradedDate: '2025-07-04T14:00:00',
            feedback: 'Good experimental design and data analysis.',
            weight: 15,
          },
          {
            id: '5',
            assignment: 'Weekly Quiz 5',
            course: 'Chemistry',
            instructor: 'Dr. Brown',
            category: 'quiz',
            points: 95,
            maxPoints: 100,
            percentage: 95,
            letterGrade: 'A',
            submissionDate: '2025-07-06T10:00:00',
            gradedDate: '2025-07-06T11:00:00',
            weight: 5,
          },
        ];
        
        setGrades(mockGrades);
        
        // Calculate course grades
        const courses = [...new Set(mockGrades.map(g => g.course))];
        const mockCourseGrades: CourseGrade[] = courses.map(course => {
          const courseAssignments = mockGrades.filter(g => g.course === course);
          const totalWeightedPoints = courseAssignments.reduce((sum, g) => sum + (g.percentage * g.weight), 0);
          const totalWeight = courseAssignments.reduce((sum, g) => sum + g.weight, 0);
          const currentGrade = totalWeight > 0 ? totalWeightedPoints / totalWeight : 0;
          
          return {
            course,
            instructor: courseAssignments[0].instructor,
            currentGrade: Math.round(currentGrade * 100) / 100,
            letterGrade: getLetterGrade(currentGrade),
            creditHours: 3, // Mock data
            assignments: courseAssignments,
          };
        });
        
        setCourseGrades(mockCourseGrades);
        
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to load grades. Please try again.',
          variant: 'destructive',
        });
      } finally {
        setLoading(false);
      }
    };

    loadGrades();
  }, [toast]);

  const getLetterGrade = (percentage: number): string => {
    if (percentage >= 97) return 'A+';
    if (percentage >= 93) return 'A';
    if (percentage >= 90) return 'A-';
    if (percentage >= 87) return 'B+';
    if (percentage >= 83) return 'B';
    if (percentage >= 80) return 'B-';
    if (percentage >= 77) return 'C+';
    if (percentage >= 73) return 'C';
    if (percentage >= 70) return 'C-';
    if (percentage >= 67) return 'D+';
    if (percentage >= 63) return 'D';
    if (percentage >= 60) return 'D-';
    return 'F';
  };

  const getGradeColor = (percentage: number): string => {
    if (percentage >= 90) return 'text-green-600';
    if (percentage >= 80) return 'text-blue-600';
    if (percentage >= 70) return 'text-yellow-600';
    if (percentage >= 60) return 'text-orange-600';
    return 'text-red-600';
  };

  const getCategoryColor = (category: string): string => {
    switch (category) {
      case 'homework': return 'bg-blue-100 text-blue-800';
      case 'quiz': return 'bg-purple-100 text-purple-800';
      case 'exam': return 'bg-red-100 text-red-800';
      case 'project': return 'bg-green-100 text-green-800';
      case 'participation': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredGrades = grades.filter(grade => {
    const matchesSearch = grade.assignment.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         grade.course.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         grade.instructor.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCourse = courseFilter === 'all' || grade.course === courseFilter;
    const matchesCategory = categoryFilter === 'all' || grade.category === categoryFilter;
    
    return matchesSearch && matchesCourse && matchesCategory;
  });

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const calculateGPA = (): number => {
    if (courseGrades.length === 0) return 0;
    
    const totalPoints = courseGrades.reduce((sum, course) => {
      const gradePoints = getGradePoints(course.letterGrade);
      return sum + (gradePoints * course.creditHours);
    }, 0);
    
    const totalCredits = courseGrades.reduce((sum, course) => sum + course.creditHours, 0);
    return totalCredits > 0 ? totalPoints / totalCredits : 0;
  };

  const getGradePoints = (letterGrade: string): number => {
    switch (letterGrade) {
      case 'A+': case 'A': return 4.0;
      case 'A-': return 3.7;
      case 'B+': return 3.3;
      case 'B': return 3.0;
      case 'B-': return 2.7;
      case 'C+': return 2.3;
      case 'C': return 2.0;
      case 'C-': return 1.7;
      case 'D+': return 1.3;
      case 'D': return 1.0;
      case 'D-': return 0.7;
      default: return 0.0;
    }
  };

  const uniqueCourses = [...new Set(grades.map(g => g.course))];

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
            <h1 className="text-3xl font-bold text-gray-900">My Grades</h1>
            <p className="text-gray-600 mt-1">
              Track your academic performance and progress
            </p>
          </div>
          <div className="flex gap-2">
            <Button 
              variant={viewMode === 'courses' ? 'default' : 'outline'} 
              size="sm"
              onClick={() => setViewMode('courses')}
            >
              Course View
            </Button>
            <Button 
              variant={viewMode === 'assignments' ? 'default' : 'outline'} 
              size="sm"
              onClick={() => setViewMode('assignments')}
            >
              Assignment View
            </Button>
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        {/* GPA Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Current GPA</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">
                {calculateGPA().toFixed(2)}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total Courses</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{courseGrades.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total Credits</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {courseGrades.reduce((sum, course) => sum + course.creditHours, 0)}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Average Grade</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {courseGrades.length > 0 
                  ? (courseGrades.reduce((sum, course) => sum + course.currentGrade, 0) / courseGrades.length).toFixed(1)
                  : 'N/A'}
                {courseGrades.length > 0 && '%'}
              </div>
            </CardContent>
          </Card>
        </div>

        {viewMode === 'courses' ? (
          // Course Grades View
          <div className="space-y-4">
            <h2 className="text-xl font-semibold mb-4">Course Grades</h2>
            {courseGrades.map((course, index) => (
              <Card key={index} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{course.course}</h3>
                        <Badge className={`${getGradeColor(course.currentGrade)} border-0 bg-opacity-20`}>
                          {course.letterGrade}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <User className="h-4 w-4" />
                          {course.instructor}
                        </div>
                        <div className="flex items-center gap-1">
                          <Award className="h-4 w-4" />
                          {course.creditHours} Credits
                        </div>
                        <div className="flex items-center gap-1">
                          <TrendingUp className="h-4 w-4" />
                          {course.currentGrade.toFixed(1)}%
                        </div>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-700">Recent Assignments:</h4>
                    {course.assignments.slice(0, 3).map((assignment) => (
                      <div key={assignment.id} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span className="text-sm">{assignment.assignment}</span>
                        <div className="flex items-center gap-2">
                          <Badge className={getCategoryColor(assignment.category)}>
                            {assignment.category}
                          </Badge>
                          <span className={`text-sm font-medium ${getGradeColor(assignment.percentage)}`}>
                            {assignment.percentage}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          // Assignment Grades View
          <>
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
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Filter by category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="homework">Homework</SelectItem>
                  <SelectItem value="quiz">Quiz</SelectItem>
                  <SelectItem value="exam">Exam</SelectItem>
                  <SelectItem value="project">Project</SelectItem>
                  <SelectItem value="participation">Participation</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Grades List */}
            <div className="space-y-4">
              {filteredGrades.length === 0 ? (
                <Card>
                  <CardContent className="text-center py-8">
                    <Award className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">No grades found matching your criteria.</p>
                  </CardContent>
                </Card>
              ) : (
                filteredGrades.map((grade) => (
                  <Card key={grade.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="text-lg font-semibold">{grade.assignment}</h3>
                            <Badge className={getCategoryColor(grade.category)}>
                              {grade.category}
                            </Badge>
                            <span className={`text-lg font-bold ${getGradeColor(grade.percentage)}`}>
                              {grade.letterGrade}
                            </span>
                          </div>
                          <div className="flex items-center gap-4 text-sm text-gray-600">
                            <div className="flex items-center gap-1">
                              <BookOpen className="h-4 w-4" />
                              {grade.course}
                            </div>
                            <div className="flex items-center gap-1">
                              <User className="h-4 w-4" />
                              {grade.instructor}
                            </div>
                            <div className="flex items-center gap-1">
                              <Calendar className="h-4 w-4" />
                              Graded: {formatDate(grade.gradedDate)}
                            </div>
                            <div className="flex items-center gap-1">
                              <Award className="h-4 w-4" />
                              {grade.points}/{grade.maxPoints} ({grade.percentage}%)
                            </div>
                          </div>
                        </div>
                        <Button variant="outline" size="sm">
                          <Eye className="h-4 w-4 mr-2" />
                          View Details
                        </Button>
                      </div>
                    </CardHeader>
                    {grade.feedback && (
                      <CardContent>
                        <Alert>
                          <FileText className="h-4 w-4" />
                          <AlertDescription>
                            <strong>Feedback:</strong> {grade.feedback}
                          </AlertDescription>
                        </Alert>
                      </CardContent>
                    )}
                  </Card>
                ))
              )}
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
};

export default StudentGrades;
