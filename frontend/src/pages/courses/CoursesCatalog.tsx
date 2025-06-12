import React, { useState, useEffect } from "react";
// import DashboardLayout from "@/components/layout/DashboardLayout"; // Removed
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { Search, Filter, BookOpen, Clock, Users, Plus, Edit, Trash2, Eye, Calendar, GraduationCap } from "lucide-react";
import { coursesAPI } from "@/lib/api";
import { useNavigate } from "react-router-dom";

// Define interfaces for better type safety
interface Instructor {
  first_name: string;
  last_name: string;
}

interface Subject {
  id?: number | string;
  name: string;
}

interface Course {
  id: number; // Assuming ID is a number
  title: string;
  description: string;
  subject?: Subject | null;
  instructor?: Instructor | null;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  status: 'draft' | 'published' | 'archived';
  start_date?: string | null;
  end_date?: string | null;
  max_students?: number | null;
  credits?: number | null;
  enrollment_count?: number;
  completion_rate?: number; // Add if available and used
}

interface CourseEditFormData {
  title: string;
  description: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  status: 'draft' | 'published' | 'archived';
  start_date: string; // Will be '' if original is null/undefined
  end_date: string;   // Will be '' if original is null/undefined
  max_students: number;
  credits: number;
}

const CoursesCatalog = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);
  const [formData, setFormData] = useState<Partial<CourseEditFormData>>({});
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterDifficulty, setFilterDifficulty] = useState("all");
  const { toast } = useToast();

  // Fetch courses from API
  const fetchCourses = async () => {
    try {
      setLoading(true);
      const response = await coursesAPI.getAll();
      // Ensure that courses is always an array
      if (Array.isArray(response.results)) {
        setCourses(response.results);
      } else if (Array.isArray(response)) {
        setCourses(response);
      } else {
        setCourses([]); // Default to empty array if response structure is unexpected
        console.warn("API response for courses was not an array:", response);
        toast({
          title: "Warning",
          description: "Received unexpected data structure for courses.",
          variant: "default",
        });
      }
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast({
        title: "Error",
        description: "Failed to fetch courses. Please try again.",
        variant: "destructive",
      });
      setCourses([]); // Ensure courses is an array in case of error
    } finally {
      setLoading(false);
    }
  };

  // Update course
  const handleUpdateCourse = async () => {
    if (!selectedCourse || !formData) return; // Added !formData check for safety
    
    try {
      // Ensure all required fields for CourseEditFormData are present if API expects full object
      // For now, assuming API handles partial updates or formData is complete due to openEditDialog logic
      await coursesAPI.update(selectedCourse.id.toString(), formData as CourseEditFormData);
      await fetchCourses();
      setIsEditDialogOpen(false);
      setFormData({});
      setSelectedCourse(null);
      toast({
        title: "Success",
        description: "Course updated successfully.",
      });
    } catch (error) {
      console.error('Error updating course:', error);
      toast({
        title: "Error",
        description: "Failed to update course. Please try again.",
        variant: "destructive",
      });
    }
  };

  // Delete course
  const handleDeleteCourse = async (courseId: number) => {
    if (!confirm("Are you sure you want to delete this course?")) return;
    
    try {
      await coursesAPI.delete(courseId.toString());
      await fetchCourses();
      toast({
        title: "Success",
        description: "Course deleted successfully.",
      });
    } catch (error) {
      console.error('Error deleting course:', error);
      toast({
        title: "Error",
        description: "Failed to delete course. Please try again.",
        variant: "destructive",
      });
    }
  };

  // Open edit dialog
  const openEditDialog = (course: Course) => {
    setSelectedCourse(course);
    setFormData({
      title: course.title || '',
      description: course.description || '',
      difficulty_level: course.difficulty_level || 'beginner',
      status: course.status || 'draft',
      start_date: course.start_date || '',
      end_date: course.end_date || '',
      max_students: course.max_students ?? 30,
      credits: course.credits ?? 3,
    });
    setIsEditDialogOpen(true);
  };

  // Open view dialog
  const openViewDialog = (course: Course) => {
    setSelectedCourse(course);
    setIsViewDialogOpen(true);
  };

  // Filter courses based on search, status, and difficulty
  const filteredCourses = courses.filter((course: Course) => { // Added type for course
    const matchesSearch = !searchTerm || 
      (course.title?.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (course.description?.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (course.subject?.name?.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (course.instructor?.first_name?.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (course.instructor?.last_name?.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesStatus = filterStatus === "all" || course.status === filterStatus;
    const matchesDifficulty = filterDifficulty === "all" || course.difficulty_level === filterDifficulty;
    
    return matchesSearch && matchesStatus && matchesDifficulty;
  });

  // Get difficulty badge variant
  const getDifficultyBadgeVariant = (difficulty: 'beginner' | 'intermediate' | 'advanced' | undefined) => {
    switch (difficulty) {
      case 'beginner': return 'secondary';
      case 'intermediate': return 'default';
      case 'advanced': return 'destructive';
      default: return 'outline';
    }
  };

  // Get status badge variant
  const getStatusBadgeVariant = (status: 'draft' | 'published' | 'archived' | undefined) => {
    switch (status) {
      case 'published': return 'default';
      case 'draft': return 'secondary';
      case 'archived': return 'outline';
      default: return 'outline';
    }
  };

  useEffect(() => {
    fetchCourses();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    // <DashboardLayout> // Removed
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Course Catalog</h1>
            <p className="text-gray-600">Manage and browse available courses</p>
          </div>
          {/* Removed Dialog, DialogTrigger, DialogContent for Create Course */}
          <Button 
            className="flex items-center gap-2"
            onClick={() => navigate('/teacher/courses/new')} // Updated
          >
            <Plus className="h-4 w-4" />
            Create Course
          </Button>
        </div>

        {/* Search and Filters */}
        <Card className="border-0 shadow-md">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search courses..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="published">Published</SelectItem>
                  <SelectItem value="draft">Draft</SelectItem>
                  <SelectItem value="archived">Archived</SelectItem>
                </SelectContent>
              </Select>
              <Select value={filterDifficulty} onValueChange={setFilterDifficulty}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Filter by difficulty" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Levels</SelectItem>
                  <SelectItem value="beginner">Beginner</SelectItem>
                  <SelectItem value="intermediate">Intermediate</SelectItem>
                  <SelectItem value="advanced">Advanced</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Loading State */}
        {loading ? (
          <Card className="border-0 shadow-md">
            <CardContent className="p-12 text-center">
              <p className="text-gray-500">Loading courses...</p>
            </CardContent>
          </Card>
        ) : (
          <>
            {/* Courses Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCourses.map((course) => (
                <Card key={course.id} className="border-0 shadow-md hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex justify-between items-start mb-2">
                      <Badge variant="outline">
                        {course.subject?.name || 'General'}
                      </Badge>
                      <div className="flex gap-1">
                        <Badge variant={getDifficultyBadgeVariant(course.difficulty_level || 'beginner')}>
                          {course.difficulty_level?.charAt(0).toUpperCase() + course.difficulty_level?.slice(1)}
                        </Badge>
                        <Badge variant={getStatusBadgeVariant(course.status || 'draft')}>
                          {course.status?.charAt(0).toUpperCase() + course.status?.slice(1)}
                        </Badge>
                      </div>
                    </div>
                    <CardTitle className="text-xl line-clamp-2">{course.title}</CardTitle>
                    <CardDescription>
                      Instructor: {course.instructor ? `${course.instructor.first_name} ${course.instructor.last_name}` : 'TBA'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4 text-sm line-clamp-3">{course.description}</p>
                    
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-1">
                          <GraduationCap className="h-4 w-4 text-gray-500" />
                          <span>Credits</span>
                        </div>
                        <span className="font-medium">{course.credits || 3}</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-1">
                          <Users className="h-4 w-4 text-gray-500" />
                          <span>Enrolled</span>
                        </div>
                        <span className="font-medium">
                          {course.enrollment_count || 0}/{course.max_students || 30}
                        </span>
                      </div>
                      
                      {course.start_date && (
                        <div className="flex items-center justify-between text-sm">
                          <div className="flex items-center gap-1">
                            <Calendar className="h-4 w-4 text-gray-500" />
                            <span>Start Date</span>
                          </div>
                          <span className="font-medium">
                            {new Date(course.start_date).toLocaleDateString()}
                          </span>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex gap-2">
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => openViewDialog(course)}
                        className="flex items-center gap-1"
                      >
                        <Eye className="h-3 w-3" />
                        View
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => openEditDialog(course)}
                        className="flex items-center gap-1"
                      >
                        <Edit className="h-3 w-3" />
                        Edit
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => handleDeleteCourse(course.id)}
                        className="flex items-center gap-1 text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-3 w-3" />
                        Delete
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Empty State */}
            {filteredCourses.length === 0 && (
              <Card className="border-0 shadow-md">
                <CardContent className="p-12 text-center">
                  <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No courses found matching your criteria.</p>
                  {/* Updated this button as well to navigate, assuming it's for teachers */}
                  <Button 
                    className="mt-4" 
                    onClick={() => navigate('/teacher/courses/new')}
                  >
                    Create First Course
                  </Button>
                </CardContent>
              </Card>
            )}
          </>
        )}

        {/* Edit Dialog */}
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Edit Course</DialogTitle>
              <DialogDescription>
                Update course information. Changes will be reflected immediately.
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-title" className="text-right">
                  Title*
                </Label>
                <Input
                  id="edit-title"
                  value={formData.title || ''}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="col-span-3"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-description" className="text-right">
                  Description*
                </Label>
                <Textarea
                  id="edit-description"
                  value={formData.description || ''}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="col-span-3"
                  rows={3}
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-difficulty" className="text-right">
                  Difficulty
                </Label>
                <Select 
                  value={formData.difficulty_level || 'beginner'} 
                  onValueChange={(value) => setFormData({ ...formData, difficulty_level: value as 'beginner' | 'intermediate' | 'advanced' })}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="beginner">Beginner</SelectItem>
                    <SelectItem value="intermediate">Intermediate</SelectItem>
                    <SelectItem value="advanced">Advanced</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-status" className="text-right">
                  Status
                </Label>
                <Select 
                  value={formData.status || 'draft'} 
                  onValueChange={(value) => setFormData({ ...formData, status: value as 'draft' | 'published' | 'archived' })}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="published">Published</SelectItem>
                    <SelectItem value="archived">Archived</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-credits" className="text-right">
                  Credits
                </Label>
                <Input
                  id="edit-credits"
                  type="number"
                  value={formData.credits || ''}
                  onChange={(e) => {
                    const val = parseInt(e.target.value);
                    setFormData({ ...formData, credits: isNaN(val) ? 1 : Math.max(1, Math.min(val, 6)) }); // Ensure value is between 1 and 6, default to 1 if NaN
                  }}
                  className="col-span-3"
                  min="1"
                  max="6"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-max-students" className="text-right">
                  Max Students
                </Label>
                <Input
                  id="edit-max-students"
                  type="number"
                  value={formData.max_students || ''}
                  onChange={(e) => {
                    const val = parseInt(e.target.value);
                    setFormData({ ...formData, max_students: isNaN(val) ? 1 : Math.max(1, Math.min(val, 100)) }); // Ensure value is between 1 and 100, default to 1 if NaN
                  }}
                  className="col-span-3"
                  min="1"
                  max="100"
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="button" onClick={handleUpdateCourse}>
                Update Course
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* View Dialog */}
        <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>{selectedCourse?.title}</DialogTitle>
              <DialogDescription>
                Complete course information and statistics
              </DialogDescription>
            </DialogHeader>
            {selectedCourse && (
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-sm text-gray-700 mb-1">Description</h4>
                  <p className="text-sm text-gray-600">{selectedCourse.description || 'No description available'}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold text-sm text-gray-700 mb-1">Instructor</h4>
                    <p className="text-sm text-gray-600">
                      {selectedCourse.instructor ? 
                        `${selectedCourse.instructor.first_name} ${selectedCourse.instructor.last_name}` : 
                        'To be assigned'
                      }
                    </p>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-sm text-gray-700 mb-1">Subject</h4>
                    <p className="text-sm text-gray-600">
                      {selectedCourse.subject?.name || 'General'}
                    </p>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-sm text-gray-700 mb-1">Difficulty</h4>
                    <Badge variant={getDifficultyBadgeVariant(selectedCourse.difficulty_level || 'beginner')}>
                      {selectedCourse.difficulty_level?.charAt(0).toUpperCase() + selectedCourse.difficulty_level?.slice(1)}
                    </Badge>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-sm text-gray-700 mb-1">Status</h4>
                    <Badge variant={getStatusBadgeVariant(selectedCourse.status || 'draft')}>
                      {selectedCourse.status?.charAt(0).toUpperCase() + selectedCourse.status?.slice(1)}
                    </Badge>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-sm text-gray-700 mb-1">Credits</h4>
                    <p className="text-sm text-gray-600">{selectedCourse.credits || 3} credits</p>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-sm text-gray-700 mb-1">Enrollment</h4>
                    <p className="text-sm text-gray-600">
                      {selectedCourse.enrollment_count || 0} / {selectedCourse.max_students || 30} students
                    </p>
                  </div>
                  
                  {selectedCourse.start_date && (
                    <div>
                      <h4 className="font-semibold text-sm text-gray-700 mb-1">Start Date</h4>
                      <p className="text-sm text-gray-600">
                        {new Date(selectedCourse.start_date).toLocaleDateString()}
                      </p>
                    </div>
                  )}
                  
                  {selectedCourse.end_date && (
                    <div>
                      <h4 className="font-semibold text-sm text-gray-700 mb-1">End Date</h4>
                      <p className="text-sm text-gray-600">
                        {new Date(selectedCourse.end_date).toLocaleDateString()}
                      </p>
                    </div>
                  )}
                </div>
                
                {selectedCourse.completion_rate !== undefined && (
                  <div>
                    <h4 className="font-semibold text-sm text-gray-700 mb-1">Completion Rate</h4>
                    <p className="text-sm text-gray-600">{selectedCourse.completion_rate}%</p>
                  </div>
                )}
              </div>
            )}
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsViewDialogOpen(false)}>
                Close
              </Button>
              {selectedCourse && (
                <Button type="button" onClick={() => {
                  setIsViewDialogOpen(false);
                  openEditDialog(selectedCourse);
                }}>
                  Edit Course
                </Button>
              )}
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    // </DashboardLayout> // Removed
  );
};

export default CoursesCatalog;
