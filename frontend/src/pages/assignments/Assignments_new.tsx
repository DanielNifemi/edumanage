// // filepath: c:\Users\USER\PycharmProjects\edumanage\frontend\src\pages\assignments\Assignments.tsx
// import DashboardLayout from "@/components/layout/DashboardLayout";
// import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
// import { Button } from "@/components/ui/button";
// import { Input } from "@/components/ui/input";
// import { Badge } from "@/components/ui/badge";
// import { Progress } from "@/components/ui/progress";
// import { Label } from "@/components/ui/label";
// import { Textarea } from "@/components/ui/textarea";
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
// import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
// import { Alert, AlertDescription } from "@/components/ui/alert";
// import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
// import { 
//   Search, Filter, Calendar, Clock, FileText, CheckCircle, AlertTriangle, 
//   Plus, Edit, Trash2, Eye, Upload, Download, Star, User, BookOpen,
//   GraduationCap, Award, Target, TrendingUp, Users, MessageSquare
// } from "lucide-react";
// import { useState, useEffect, useCallback } from "react";
// import { assignmentsAPI, coursesAPI, studentsAPI, AssignmentData, AssignmentSubmissionData, CourseData, StudentData } from "@/lib/api";

// interface AssignmentFormData {
//   title: string;
//   description: string;
//   instructions: string;
//   course: string;
//   due_date: string;
//   total_points: number;
//   submission_type: 'file' | 'text' | 'url' | 'online';
//   allow_late_submission: boolean;
//   late_penalty_per_day: number;
// }

// interface SubmissionFormData {
//   submitted_text: string;
//   submitted_url: string;
//   submitted_file: File | null;
// }

// const Assignments = () => {
//   const [assignments, setAssignments] = useState<AssignmentData[]>([]);
//   const [submissions, setSubmissions] = useState<AssignmentSubmissionData[]>([]);
//   const [courses, setCourses] = useState<CourseData[]>([]);
//   const [students, setStudents] = useState<StudentData[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);
//   const [searchTerm, setSearchTerm] = useState("");
//   const [filterStatus, setFilterStatus] = useState<string>("all");
//   const [filterCourse, setFilterCourse] = useState<string>("all");
//   const [currentUserRole] = useState<'teacher' | 'student'>('student'); // This would come from auth context
//   const [selectedAssignment, setSelectedAssignment] = useState<AssignmentData | null>(null);
//   const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
//   const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
//   const [isSubmissionDialogOpen, setIsSubmissionDialogOpen] = useState(false);
//   const [isGradingDialogOpen, setIsGradingDialogOpen] = useState(false);
//   const [submissionToGrade, setSubmissionToGrade] = useState<AssignmentSubmissionData | null>(null);
//   const [activeTab, setActiveTab] = useState("overview");

//   const [assignmentForm, setAssignmentForm] = useState<AssignmentFormData>({
//     title: '',
//     description: '',
//     instructions: '',
//     course: '',
//     due_date: '',
//     total_points: 100,
//     submission_type: 'file',
//     allow_late_submission: false,
//     late_penalty_per_day: 0
//   });

//   const [submissionForm, setSubmissionForm] = useState<SubmissionFormData>({
//     submitted_text: '',
//     submitted_url: '',
//     submitted_file: null
//   });

//   const [gradeForm, setGradeForm] = useState({
//     grade: '',
//     feedback: ''
//   });

//   const fetchData = useCallback(async () => {
//     try {
//       setLoading(true);
//       setError(null);
      
//       const [assignmentsData, coursesData, studentsData] = await Promise.all([
//         currentUserRole === 'teacher' 
//           ? assignmentsAPI.getTeacherAssignments() 
//           : assignmentsAPI.getStudentAssignments(),
//         coursesAPI.getAll(),
//         studentsAPI.getAll()
//       ]);

//       setAssignments(assignmentsData);
//       setCourses(coursesData);
//       setStudents(studentsData);

//       // Fetch submissions for each assignment
//       const allSubmissions: AssignmentSubmissionData[] = [];
//       for (const assignment of assignmentsData) {
//         try {
//           const assignmentSubmissions = await assignmentsAPI.getSubmissions(assignment.id);
//           allSubmissions.push(...assignmentSubmissions);
//         } catch (err) {
//           console.error(`Error fetching submissions for assignment ${assignment.id}:`, err);
//         }
//       }
//       setSubmissions(allSubmissions);
//     } catch (err) {
//       console.error('Error fetching assignments data:', err);
//       setError('Failed to load assignments data. Please try again.');
//     } finally {
//       setLoading(false);
//     }
//   }, [currentUserRole]);

//   useEffect(() => {
//     fetchData();
//   }, [fetchData]);

//   const handleCreateAssignment = async (e: React.FormEvent) => {
//     e.preventDefault();
//     try {
//       const courseId = parseInt(assignmentForm.course);
//       const course = courses.find(c => c.id === courseId);
      
//       if (!course) {
//         setError('Please select a valid course');
//         return;
//       }

//       const newAssignment = await assignmentsAPI.create({
//         ...assignmentForm,
//         course: courseId,
//         content: assignmentForm.description
//       });

//       setAssignments(prev => [...prev, newAssignment]);
//       setIsCreateDialogOpen(false);
//       setAssignmentForm({
//         title: '',
//         description: '',
//         instructions: '',
//         course: '',
//         due_date: '',
//         total_points: 100,
//         submission_type: 'file',
//         allow_late_submission: false,
//         late_penalty_per_day: 0
//       });
//     } catch (err) {
//       console.error('Error creating assignment:', err);
//       setError('Failed to create assignment. Please try again.');
//     }
//   };

//   const handleEditAssignment = async (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!selectedAssignment) return;

//     try {
//       const courseId = parseInt(assignmentForm.course);
//       const updatedAssignment = await assignmentsAPI.update(selectedAssignment.id, {
//         ...assignmentForm,
//         course: courseId,
//         content: assignmentForm.description
//       });

//       setAssignments(prev => prev.map(a => a.id === updatedAssignment.id ? updatedAssignment : a));
//       setIsEditDialogOpen(false);
//       setSelectedAssignment(null);
//     } catch (err) {
//       console.error('Error updating assignment:', err);
//       setError('Failed to update assignment. Please try again.');
//     }
//   };

//   const handleDeleteAssignment = async (assignmentId: number) => {
//     if (!confirm('Are you sure you want to delete this assignment?')) return;

//     try {
//       await assignmentsAPI.delete(assignmentId);
//       setAssignments(prev => prev.filter(a => a.id !== assignmentId));
//     } catch (err) {
//       console.error('Error deleting assignment:', err);
//       setError('Failed to delete assignment. Please try again.');
//     }
//   };

//   const handleSubmitAssignment = async (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!selectedAssignment) return;

//     try {
//       const submissionData = {
//         assignment: selectedAssignment.id,
//         ...submissionForm
//       };

//       await assignmentsAPI.submitAssignment(selectedAssignment.id, submissionData);
//       await fetchData(); // Refresh data to show updated submission
//       setIsSubmissionDialogOpen(false);
//       setSubmissionForm({
//         submitted_text: '',
//         submitted_url: '',
//         submitted_file: null
//       });
//     } catch (err) {
//       console.error('Error submitting assignment:', err);
//       setError('Failed to submit assignment. Please try again.');
//     }
//   };

//   const handleGradeSubmission = async (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!submissionToGrade) return;

//     try {
//       await assignmentsAPI.gradeSubmission(submissionToGrade.id, {
//         grade: parseFloat(gradeForm.grade),
//         feedback: gradeForm.feedback
//       });
      
//       await fetchData(); // Refresh data
//       setIsGradingDialogOpen(false);
//       setSubmissionToGrade(null);
//       setGradeForm({ grade: '', feedback: '' });
//     } catch (err) {
//       console.error('Error grading submission:', err);
//       setError('Failed to grade submission. Please try again.');
//     }
//   };

//   const openEditDialog = (assignment: AssignmentData) => {
//     setSelectedAssignment(assignment);
//     setAssignmentForm({
//       title: assignment.title,
//       description: assignment.content,
//       instructions: assignment.instructions,
//       course: assignment.course.toString(),
//       due_date: assignment.due_date.split('T')[0],
//       total_points: assignment.total_points,
//       submission_type: assignment.submission_type,
//       allow_late_submission: assignment.allow_late_submission,
//       late_penalty_per_day: assignment.late_penalty_per_day
//     });
//     setIsEditDialogOpen(true);
//   };

//   const openSubmissionDialog = (assignment: AssignmentData) => {
//     setSelectedAssignment(assignment);
//     setIsSubmissionDialogOpen(true);
//   };

//   const openGradingDialog = (submission: AssignmentSubmissionData) => {
//     setSubmissionToGrade(submission);
//     setGradeForm({
//       grade: submission.grade?.toString() || '',
//       feedback: submission.feedback || ''
//     });
//     setIsGradingDialogOpen(true);
//   };

//   const filteredAssignments = assignments.filter(assignment => {
//     const matchesSearch = assignment.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
//                          assignment.content.toLowerCase().includes(searchTerm.toLowerCase());
//     const matchesStatus = filterStatus === "all" || getAssignmentStatus(assignment) === filterStatus;
//     const matchesCourse = filterCourse === "all" || assignment.course.toString() === filterCourse;
    
//     return matchesSearch && matchesStatus && matchesCourse;
//   });

//   const getAssignmentStatus = (assignment: AssignmentData) => {
//     const now = new Date();
//     const dueDate = new Date(assignment.due_date);
    
//     if (currentUserRole === 'student') {
//       const studentSubmission = submissions.find(s => 
//         s.assignment === assignment.id && s.student === 1 // This would be current student ID
//       );
      
//       if (studentSubmission) {
//         return studentSubmission.grade !== null ? 'graded' : 'submitted';
//       }
//       return now > dueDate ? 'overdue' : 'pending';
//     }
    
//     return 'active'; // For teachers, assignments are just active
//   };

//   const getStatusColor = (status: string) => {
//     switch (status) {
//       case 'pending': return 'bg-yellow-100 text-yellow-800';
//       case 'submitted': return 'bg-blue-100 text-blue-800';
//       case 'graded': return 'bg-green-100 text-green-800';
//       case 'overdue': return 'bg-red-100 text-red-800';
//       case 'active': return 'bg-purple-100 text-purple-800';
//       default: return 'bg-gray-100 text-gray-800';
//     }
//   };

//   const getStatusIcon = (status: string) => {
//     switch (status) {
//       case 'pending': return <Clock className="h-4 w-4" />;
//       case 'submitted': return <FileText className="h-4 w-4" />;
//       case 'graded': return <CheckCircle className="h-4 w-4" />;
//       case 'overdue': return <AlertTriangle className="h-4 w-4" />;
//       case 'active': return <BookOpen className="h-4 w-4" />;
//       default: return <AlertTriangle className="h-4 w-4" />;
//     }
//   };

//   const getDaysUntilDue = (dueDate: string) => {
//     const today = new Date();
//     const due = new Date(dueDate);
//     const diffTime = due.getTime() - today.getTime();
//     const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
//     if (diffDays < 0) return "Overdue";
//     if (diffDays === 0) return "Due today";
//     if (diffDays === 1) return "Due tomorrow";
//     return `${diffDays} days left`;
//   };

//   const getSubmissionStats = () => {
//     const totalAssignments = assignments.length;
//     const submittedCount = submissions.filter(s => s.student === 1).length; // Current student
//     const gradedCount = submissions.filter(s => s.student === 1 && s.grade !== null).length;
//     const pendingCount = totalAssignments - submittedCount;
    
//     return { totalAssignments, submittedCount, gradedCount, pendingCount };
//   };

//   const getTeacherStats = () => {
//     const totalAssignments = assignments.length;
//     const totalSubmissions = submissions.length;
//     const gradedSubmissions = submissions.filter(s => s.grade !== null).length;
//     const pendingGrading = totalSubmissions - gradedSubmissions;
    
//     return { totalAssignments, totalSubmissions, gradedSubmissions, pendingGrading };
//   };

//   if (loading) {
//     return (
//       <DashboardLayout>
//         <div className="p-6">
//           <div className="animate-pulse space-y-4">
//             <div className="h-8 bg-gray-200 rounded w-1/4"></div>
//             <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
//               {[...Array(4)].map((_, i) => (
//                 <div key={i} className="h-24 bg-gray-200 rounded"></div>
//               ))}
//             </div>
//             <div className="space-y-4">
//               {[...Array(3)].map((_, i) => (
//                 <div key={i} className="h-32 bg-gray-200 rounded"></div>
//               ))}
//             </div>
//           </div>
//         </div>
//       </DashboardLayout>
//     );
//   }

//   if (error) {
//     return (
//       <DashboardLayout>
//         <div className="p-6">
//           <Alert className="mb-6">
//             <AlertTriangle className="h-4 w-4" />
//             <AlertDescription>{error}</AlertDescription>
//           </Alert>
//           <Button onClick={fetchData} className="mt-4">
//             Try Again
//           </Button>
//         </div>
//       </DashboardLayout>
//     );
//   }

//   const stats = currentUserRole === 'student' ? getSubmissionStats() : getTeacherStats();

//   return (
//     <DashboardLayout>
//       <div className="p-6">
//         <div className="flex justify-between items-center mb-6">
//           <div>
//             <h1 className="text-3xl font-bold text-gray-900">Assignment Management</h1>
//             <p className="text-gray-600 mt-1">
//               {currentUserRole === 'teacher' 
//                 ? 'Create, manage, and grade assignments' 
//                 : 'View assignments and submit your work'}
//             </p>
//           </div>
//           {currentUserRole === 'teacher' && (
//             <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
//               <DialogTrigger asChild>
//                 <Button>
//                   <Plus className="h-4 w-4 mr-2" />
//                   Create Assignment
//                 </Button>
//               </DialogTrigger>
//               <DialogContent className="max-w-2xl">
//                 <DialogHeader>
//                   <DialogTitle>Create New Assignment</DialogTitle>
//                   <DialogDescription>
//                     Create a new assignment for your students.
//                   </DialogDescription>
//                 </DialogHeader>
//                 <form onSubmit={handleCreateAssignment}>
//                   <div className="grid gap-4 py-4">
//                     <div className="grid grid-cols-4 items-center gap-4">
//                       <Label htmlFor="title" className="text-right">Title</Label>
//                       <Input
//                         id="title"
//                         value={assignmentForm.title}
//                         onChange={(e) => setAssignmentForm(prev => ({ ...prev, title: e.target.value }))}
//                         className="col-span-3"
//                         required
//                       />
//                     </div>
//                     <div className="grid grid-cols-4 items-center gap-4">
//                       <Label htmlFor="course" className="text-right">Course</Label>
//                       <Select
//                         value={assignmentForm.course}
//                         onValueChange={(value) => setAssignmentForm(prev => ({ ...prev, course: value }))}
//                       >
//                         <SelectTrigger className="col-span-3">
//                           <SelectValue placeholder="Select course" />
//                         </SelectTrigger>
//                         <SelectContent>
//                           {courses.map(course => (
//                             <SelectItem key={course.id} value={course.id.toString()}>
//                               {course.name}
//                             </SelectItem>
//                           ))}
//                         </SelectContent>
//                       </Select>
//                     </div>
//                     <div className="grid grid-cols-4 items-center gap-4">
//                       <Label htmlFor="due_date" className="text-right">Due Date</Label>
//                       <Input
//                         id="due_date"
//                         type="datetime-local"
//                         value={assignmentForm.due_date}
//                         onChange={(e) => setAssignmentForm(prev => ({ ...prev, due_date: e.target.value }))}
//                         className="col-span-3"
//                         required
//                       />
//                     </div>
//                     <div className="grid grid-cols-4 items-center gap-4">
//                       <Label htmlFor="total_points" className="text-right">Total Points</Label>
//                       <Input
//                         id="total_points"
//                         type="number"
//                         value={assignmentForm.total_points}
//                         onChange={(e) => setAssignmentForm(prev => ({ ...prev, total_points: parseInt(e.target.value) }))}
//                         className="col-span-3"
//                         required
//                       />
//                     </div>
//                     <div className="grid grid-cols-4 items-center gap-4">
//                       <Label htmlFor="submission_type" className="text-right">Submission Type</Label>
//                       <Select
//                         value={assignmentForm.submission_type}
//                         onValueChange={(value: 'file' | 'text' | 'url' | 'online') => 
//                           setAssignmentForm(prev => ({ ...prev, submission_type: value }))
//                         }
//                       >
//                         <SelectTrigger className="col-span-3">
//                           <SelectValue />
//                         </SelectTrigger>
//                         <SelectContent>
//                           <SelectItem value="file">File Upload</SelectItem>
//                           <SelectItem value="text">Text Submission</SelectItem>
//                           <SelectItem value="url">URL Submission</SelectItem>
//                           <SelectItem value="online">Online Quiz</SelectItem>
//                         </SelectContent>
//                       </Select>
//                     </div>
//                     <div className="grid grid-cols-4 items-start gap-4">
//                       <Label htmlFor="description" className="text-right">Description</Label>
//                       <Textarea
//                         id="description"
//                         value={assignmentForm.description}
//                         onChange={(e) => setAssignmentForm(prev => ({ ...prev, description: e.target.value }))}
//                         className="col-span-3"
//                         rows={3}
//                         required
//                       />
//                     </div>
//                     <div className="grid grid-cols-4 items-start gap-4">
//                       <Label htmlFor="instructions" className="text-right">Instructions</Label>
//                       <Textarea
//                         id="instructions"
//                         value={assignmentForm.instructions}
//                         onChange={(e) => setAssignmentForm(prev => ({ ...prev, instructions: e.target.value }))}
//                         className="col-span-3"
//                         rows={4}
//                       />
//                     </div>
//                   </div>
//                   <DialogFooter>
//                     <Button type="submit">Create Assignment</Button>
//                   </DialogFooter>
//                 </form>
//               </DialogContent>
//             </Dialog>
//           )}
//         </div>

//         {/* Stats Cards */}
//         <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
//           {currentUserRole === 'student' ? (
//             <>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Total Assignments</p>
//                       <p className="text-2xl font-bold text-gray-900">{stats.totalAssignments}</p>
//                     </div>
//                     <FileText className="h-8 w-8 text-blue-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Pending</p>
//                       <p className="text-2xl font-bold text-yellow-600">{stats.pendingCount}</p>
//                     </div>
//                     <Clock className="h-8 w-8 text-yellow-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Submitted</p>
//                       <p className="text-2xl font-bold text-blue-600">{stats.submittedCount}</p>
//                     </div>
//                     <CheckCircle className="h-8 w-8 text-blue-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Graded</p>
//                       <p className="text-2xl font-bold text-green-600">{stats.gradedCount}</p>
//                     </div>
//                     <Award className="h-8 w-8 text-green-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//             </>
//           ) : (
//             <>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Total Assignments</p>
//                       <p className="text-2xl font-bold text-gray-900">{stats.totalAssignments}</p>
//                     </div>
//                     <FileText className="h-8 w-8 text-blue-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Total Submissions</p>
//                       <p className="text-2xl font-bold text-purple-600">{stats.totalSubmissions}</p>
//                     </div>
//                     <Users className="h-8 w-8 text-purple-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Graded</p>
//                       <p className="text-2xl font-bold text-green-600">{stats.gradedSubmissions}</p>
//                     </div>
//                     <Award className="h-8 w-8 text-green-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//               <Card>
//                 <CardContent className="p-6">
//                   <div className="flex items-center justify-between">
//                     <div>
//                       <p className="text-sm font-medium text-gray-600">Pending Grading</p>
//                       <p className="text-2xl font-bold text-orange-600">{stats.pendingGrading}</p>
//                     </div>
//                     <Clock className="h-8 w-8 text-orange-600" />
//                   </div>
//                 </CardContent>
//               </Card>
//             </>
//           )}
//         </div>

//         {/* Tabs for different views */}
//         <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-6">
//           <TabsList>
//             <TabsTrigger value="overview">Overview</TabsTrigger>
//             {currentUserRole === 'teacher' && <TabsTrigger value="submissions">Submissions</TabsTrigger>}
//             {currentUserRole === 'student' && <TabsTrigger value="calendar">Calendar</TabsTrigger>}
//           </TabsList>

//           <TabsContent value="overview">
//             {/* Search and Filter */}
//             <div className="flex gap-4 mb-6">
//               <div className="relative flex-1">
//                 <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
//                 <Input
//                   placeholder="Search assignments..."
//                   value={searchTerm}
//                   onChange={(e) => setSearchTerm(e.target.value)}
//                   className="pl-10"
//                 />
//               </div>
//               <Select value={filterStatus} onValueChange={setFilterStatus}>
//                 <SelectTrigger className="w-40">
//                   <SelectValue placeholder="Filter by status" />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="all">All Status</SelectItem>
//                   <SelectItem value="pending">Pending</SelectItem>
//                   <SelectItem value="submitted">Submitted</SelectItem>
//                   <SelectItem value="graded">Graded</SelectItem>
//                   <SelectItem value="overdue">Overdue</SelectItem>
//                 </SelectContent>
//               </Select>
//               <Select value={filterCourse} onValueChange={setFilterCourse}>
//                 <SelectTrigger className="w-40">
//                   <SelectValue placeholder="Filter by course" />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="all">All Courses</SelectItem>
//                   {courses.map(course => (
//                     <SelectItem key={course.id} value={course.id.toString()}>
//                       {course.name}
//                     </SelectItem>
//                   ))}
//                 </SelectContent>
//               </Select>
//             </div>

//             {/* Assignments List */}
//             <div className="space-y-4">
//               {filteredAssignments.map((assignment) => {
//                 const status = getAssignmentStatus(assignment);
//                 const course = courses.find(c => c.id === assignment.course);
//                 const assignmentSubmissions = submissions.filter(s => s.assignment === assignment.id);
                
//                 return (
//                   <Card key={assignment.id} className="hover:shadow-md transition-shadow">
//                     <CardContent className="p-6">
//                       <div className="flex items-start justify-between">
//                         <div className="flex-1">
//                           <div className="flex items-center gap-3 mb-2">
//                             {getStatusIcon(status)}
//                             <h3 className="text-lg font-semibold text-gray-900">{assignment.title}</h3>
//                             <Badge className={getStatusColor(status)}>
//                               {status}
//                             </Badge>
//                             <Badge variant="outline">
//                               {assignment.total_points} pts
//                             </Badge>
//                           </div>
//                           <p className="text-blue-600 font-medium mb-1">{course?.name}</p>
//                           <p className="text-gray-600 text-sm mb-3">{assignment.content}</p>
                          
//                           <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
//                             <div className="flex items-center gap-1">
//                               <Calendar className="h-4 w-4" />
//                               Due: {new Date(assignment.due_date).toLocaleDateString()}
//                             </div>
//                             <div className="flex items-center gap-1">
//                               <Clock className="h-4 w-4" />
//                               {getDaysUntilDue(assignment.due_date)}
//                             </div>
//                             <div className="flex items-center gap-1">
//                               <FileText className="h-4 w-4" />
//                               {assignment.submission_type}
//                             </div>
//                             {currentUserRole === 'teacher' && (
//                               <div className="flex items-center gap-1">
//                                 <Users className="h-4 w-4" />
//                                 {assignmentSubmissions.length} submission(s)
//                               </div>
//                             )}
//                           </div>

//                           {assignment.instructions && (
//                             <div className="bg-gray-50 p-3 rounded-md mb-3">
//                               <p className="text-sm text-gray-700">{assignment.instructions}</p>
//                             </div>
//                           )}
//                         </div>
                        
//                         <div className="flex flex-col gap-2 ml-4">
//                           {currentUserRole === 'student' ? (
//                             <>
//                               {status === 'pending' && (
//                                 <Button 
//                                   size="sm" 
//                                   onClick={() => openSubmissionDialog(assignment)}
//                                 >
//                                   <Upload className="h-4 w-4 mr-2" />
//                                   Submit
//                                 </Button>
//                               )}
//                               {status === 'submitted' && (
//                                 <Button size="sm" variant="outline">
//                                   <Eye className="h-4 w-4 mr-2" />
//                                   View Submission
//                                 </Button>
//                               )}
//                               {status === 'graded' && (
//                                 <Button size="sm" variant="outline">
//                                   <MessageSquare className="h-4 w-4 mr-2" />
//                                   View Feedback
//                                 </Button>
//                               )}
//                             </>
//                           ) : (
//                             <>
//                               <Button 
//                                 size="sm" 
//                                 variant="outline" 
//                                 onClick={() => openEditDialog(assignment)}
//                               >
//                                 <Edit className="h-4 w-4 mr-2" />
//                                 Edit
//                               </Button>
//                               <Button 
//                                 size="sm" 
//                                 variant="outline" 
//                                 onClick={() => handleDeleteAssignment(assignment.id)}
//                               >
//                                 <Trash2 className="h-4 w-4 mr-2" />
//                                 Delete
//                               </Button>
//                               {assignmentSubmissions.length > 0 && (
//                                 <Button size="sm">
//                                   <Award className="h-4 w-4 mr-2" />
//                                   Grade ({assignmentSubmissions.length})
//                                 </Button>
//                               )}
//                             </>
//                           )}
//                         </div>
//                       </div>
//                     </CardContent>
//                   </Card>
//                 );
//               })}
//             </div>
//           </TabsContent>

//           {currentUserRole === 'teacher' && (
//             <TabsContent value="submissions">
//               <div className="space-y-4">
//                 {submissions.map((submission) => {
//                   const assignment = assignments.find(a => a.id === submission.assignment);
//                   const student = students.find(s => s.id === submission.student);
                  
//                   return (
//                     <Card key={submission.id}>
//                       <CardContent className="p-6">
//                         <div className="flex items-start justify-between">
//                           <div className="flex-1">
//                             <h3 className="text-lg font-semibold text-gray-900 mb-2">
//                               {assignment?.title}
//                             </h3>
//                             <p className="text-blue-600 font-medium mb-1">
//                               Student: {student?.user?.first_name} {student?.user?.last_name}
//                             </p>
//                             <p className="text-gray-600 text-sm mb-3">
//                               Submitted: {new Date(submission.submitted_at).toLocaleDateString()}
//                             </p>
                            
//                             {submission.submitted_text && (
//                               <div className="bg-gray-50 p-3 rounded-md mb-3">
//                                 <p className="text-sm text-gray-700">{submission.submitted_text}</p>
//                               </div>
//                             )}
                            
//                             {submission.submitted_url && (
//                               <div className="mb-3">
//                                 <a 
//                                   href={submission.submitted_url} 
//                                   className="text-blue-600 hover:underline text-sm"
//                                   target="_blank"
//                                   rel="noopener noreferrer"
//                                 >
//                                   View Submitted URL
//                                 </a>
//                               </div>
//                             )}
//                           </div>
                          
//                           <div className="flex flex-col gap-2 ml-4">
//                             {submission.grade !== null ? (
//                               <Badge className="bg-green-100 text-green-800">
//                                 Grade: {submission.grade}/{assignment?.total_points}
//                               </Badge>
//                             ) : (
//                               <Button 
//                                 size="sm" 
//                                 onClick={() => openGradingDialog(submission)}
//                               >
//                                 <Star className="h-4 w-4 mr-2" />
//                                 Grade
//                               </Button>
//                             )}
//                             <Button size="sm" variant="outline">
//                               <Download className="h-4 w-4 mr-2" />
//                               Download
//                             </Button>
//                           </div>
//                         </div>
//                       </CardContent>
//                     </Card>
//                   );
//                 })}
//               </div>
//             </TabsContent>
//           )}
//         </Tabs>

//         {/* Edit Assignment Dialog */}
//         <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
//           <DialogContent className="max-w-2xl">
//             <DialogHeader>
//               <DialogTitle>Edit Assignment</DialogTitle>
//               <DialogDescription>
//                 Update the assignment details.
//               </DialogDescription>
//             </DialogHeader>
//             <form onSubmit={handleEditAssignment}>
//               <div className="grid gap-4 py-4">
//                 <div className="grid grid-cols-4 items-center gap-4">
//                   <Label htmlFor="edit-title" className="text-right">Title</Label>
//                   <Input
//                     id="edit-title"
//                     value={assignmentForm.title}
//                     onChange={(e) => setAssignmentForm(prev => ({ ...prev, title: e.target.value }))}
//                     className="col-span-3"
//                     required
//                   />
//                 </div>
//                 <div className="grid grid-cols-4 items-center gap-4">
//                   <Label htmlFor="edit-course" className="text-right">Course</Label>
//                   <Select
//                     value={assignmentForm.course}
//                     onValueChange={(value) => setAssignmentForm(prev => ({ ...prev, course: value }))}
//                   >
//                     <SelectTrigger className="col-span-3">
//                       <SelectValue placeholder="Select course" />
//                     </SelectTrigger>
//                     <SelectContent>
//                       {courses.map(course => (
//                         <SelectItem key={course.id} value={course.id.toString()}>
//                           {course.name}
//                         </SelectItem>
//                       ))}
//                     </SelectContent>
//                   </Select>
//                 </div>
//                 <div className="grid grid-cols-4 items-center gap-4">
//                   <Label htmlFor="edit-due_date" className="text-right">Due Date</Label>
//                   <Input
//                     id="edit-due_date"
//                     type="datetime-local"
//                     value={assignmentForm.due_date}
//                     onChange={(e) => setAssignmentForm(prev => ({ ...prev, due_date: e.target.value }))}
//                     className="col-span-3"
//                     required
//                   />
//                 </div>
//                 <div className="grid grid-cols-4 items-start gap-4">
//                   <Label htmlFor="edit-description" className="text-right">Description</Label>
//                   <Textarea
//                     id="edit-description"
//                     value={assignmentForm.description}
//                     onChange={(e) => setAssignmentForm(prev => ({ ...prev, description: e.target.value }))}
//                     className="col-span-3"
//                     rows={3}
//                     required
//                   />
//                 </div>
//               </div>
//               <DialogFooter>
//                 <Button type="submit">Update Assignment</Button>
//               </DialogFooter>
//             </form>
//           </DialogContent>
//         </Dialog>

//         {/* Submission Dialog */}
//         <Dialog open={isSubmissionDialogOpen} onOpenChange={setIsSubmissionDialogOpen}>
//           <DialogContent className="max-w-2xl">
//             <DialogHeader>
//               <DialogTitle>Submit Assignment</DialogTitle>
//               <DialogDescription>
//                 Submit your work for "{selectedAssignment?.title}"
//               </DialogDescription>
//             </DialogHeader>
//             <form onSubmit={handleSubmitAssignment}>
//               <div className="grid gap-4 py-4">
//                 {selectedAssignment?.submission_type === 'text' && (
//                   <div className="grid grid-cols-4 items-start gap-4">
//                     <Label htmlFor="submitted_text" className="text-right">Text Submission</Label>
//                     <Textarea
//                       id="submitted_text"
//                       value={submissionForm.submitted_text}
//                       onChange={(e) => setSubmissionForm(prev => ({ ...prev, submitted_text: e.target.value }))}
//                       className="col-span-3"
//                       rows={6}
//                       required
//                     />
//                   </div>
//                 )}
                
//                 {selectedAssignment?.submission_type === 'url' && (
//                   <div className="grid grid-cols-4 items-center gap-4">
//                     <Label htmlFor="submitted_url" className="text-right">URL</Label>
//                     <Input
//                       id="submitted_url"
//                       type="url"
//                       value={submissionForm.submitted_url}
//                       onChange={(e) => setSubmissionForm(prev => ({ ...prev, submitted_url: e.target.value }))}
//                       className="col-span-3"
//                       placeholder="https://..."
//                       required
//                     />
//                   </div>
//                 )}
                
//                 {selectedAssignment?.submission_type === 'file' && (
//                   <div className="grid grid-cols-4 items-center gap-4">
//                     <Label htmlFor="submitted_file" className="text-right">File</Label>
//                     <Input
//                       id="submitted_file"
//                       type="file"
//                       onChange={(e) => setSubmissionForm(prev => ({ 
//                         ...prev, 
//                         submitted_file: e.target.files?.[0] || null 
//                       }))}
//                       className="col-span-3"
//                       required
//                     />
//                   </div>
//                 )}
//               </div>
//               <DialogFooter>
//                 <Button type="submit">Submit Assignment</Button>
//               </DialogFooter>
//             </form>
//           </DialogContent>
//         </Dialog>

//         {/* Grading Dialog */}
//         <Dialog open={isGradingDialogOpen} onOpenChange={setIsGradingDialogOpen}>
//           <DialogContent className="max-w-2xl">
//             <DialogHeader>
//               <DialogTitle>Grade Submission</DialogTitle>
//               <DialogDescription>
//                 Grade the student's submission and provide feedback.
//               </DialogDescription>
//             </DialogHeader>
//             <form onSubmit={handleGradeSubmission}>
//               <div className="grid gap-4 py-4">
//                 <div className="grid grid-cols-4 items-center gap-4">
//                   <Label htmlFor="grade" className="text-right">Grade</Label>
//                   <Input
//                     id="grade"
//                     type="number"
//                     step="0.1"
//                     min="0"
//                     max={assignments.find(a => a.id === submissionToGrade?.assignment)?.total_points || 100}
//                     value={gradeForm.grade}
//                     onChange={(e) => setGradeForm(prev => ({ ...prev, grade: e.target.value }))}
//                     className="col-span-3"
//                     required
//                     placeholder={`Out of ${assignments.find(a => a.id === submissionToGrade?.assignment)?.total_points || 100}`}
//                   />
//                 </div>
//                 <div className="grid grid-cols-4 items-start gap-4">
//                   <Label htmlFor="feedback" className="text-right">Feedback</Label>
//                   <Textarea
//                     id="feedback"
//                     value={gradeForm.feedback}
//                     onChange={(e) => setGradeForm(prev => ({ ...prev, feedback: e.target.value }))}
//                     className="col-span-3"
//                     rows={4}
//                     placeholder="Provide feedback to the student..."
//                   />
//                 </div>
//               </div>
//               <DialogFooter>
//                 <Button type="submit">Submit Grade</Button>
//               </DialogFooter>
//             </form>
//           </DialogContent>
//         </Dialog>
//       </div>
//     </DashboardLayout>
//   );
// };

// export default Assignments;
