
import React, { useState, useEffect } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useToast } from "@/hooks/use-toast";
import { Search, Filter, Users, Download, Plus, Edit, Trash2, Eye } from "lucide-react";
import { studentsAPI, StudentData } from "@/lib/api";

interface Student extends StudentData {
  id: string;
  full_name?: string;
  enrollment_date?: string;
  status?: string;
  grade_level?: string;
  gpa?: number;
  courses_count?: number;
  attendance_rate?: number;
}

const StudentsList = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);
  const [formData, setFormData] = useState<Partial<StudentData>>({});
  const { toast } = useToast();

  // Load students data
  useEffect(() => {
    loadStudents();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const loadStudents = async () => {
    try {
      setLoading(true);
      
      // Try to load from API first
      try {
        const data = await studentsAPI.getAll();
        setStudents(data);
      } catch (apiError) {
        // If API fails, use mock data
        console.log('API failed, using mock data:', apiError);
        
        // Mock data for development
        const mockStudents: Student[] = [
          {
            id: '1',
            username: 'john.doe',
            email: 'john.doe@school.edu',
            first_name: 'John',
            last_name: 'Doe',
            full_name: 'John Doe',
            student_id: 'STU001',
            grade_level: '10th Grade',
            enrollment_date: '2024-09-01',
            status: 'Active',
            gpa: 3.8,
            courses_count: 6,
            attendance_rate: 95,
            phone_number: '(555) 123-4567',
            parent_guardian: 'Jane Doe',
            address: '123 Main St, City, State 12345',
          },
          {
            id: '2',
            username: 'sarah.wilson',
            email: 'sarah.wilson@school.edu',
            first_name: 'Sarah',
            last_name: 'Wilson',
            full_name: 'Sarah Wilson',
            student_id: 'STU002',
            grade_level: '11th Grade',
            enrollment_date: '2023-09-01',
            status: 'Active',
            gpa: 3.9,
            courses_count: 7,
            attendance_rate: 98,
            phone_number: '(555) 234-5678',
            parent_guardian: 'Mike Wilson',
            address: '456 Oak Ave, City, State 12345',
          },
          {
            id: '3',
            username: 'alex.chen',
            email: 'alex.chen@school.edu',
            first_name: 'Alex',
            last_name: 'Chen',
            full_name: 'Alex Chen',
            student_id: 'STU003',
            grade_level: '12th Grade',
            enrollment_date: '2022-09-01',
            status: 'Active',
            gpa: 3.7,
            courses_count: 8,
            attendance_rate: 92,
            phone_number: '(555) 345-6789',
            parent_guardian: 'Lisa Chen',
            address: '789 Pine Rd, City, State 12345',
          },
          {
            id: '4',
            username: 'emma.taylor',
            email: 'emma.taylor@school.edu',
            first_name: 'Emma',
            last_name: 'Taylor',
            full_name: 'Emma Taylor',
            student_id: 'STU004',
            grade_level: '9th Grade',
            enrollment_date: '2024-09-01',
            status: 'Active',
            gpa: 3.6,
            courses_count: 5,
            attendance_rate: 94,
            phone_number: '(555) 456-7890',
            parent_guardian: 'Robert Taylor',
            address: '321 Elm St, City, State 12345',
          },
          {
            id: '5',
            username: 'michael.brown',
            email: 'michael.brown@school.edu',
            first_name: 'Michael',
            last_name: 'Brown',
            full_name: 'Michael Brown',
            student_id: 'STU005',
            grade_level: '10th Grade',
            enrollment_date: '2024-09-01',
            status: 'Inactive',
            gpa: 3.4,
            courses_count: 4,
            attendance_rate: 88,
            phone_number: '(555) 567-8901',
            parent_guardian: 'Susan Brown',
            address: '654 Maple Dr, City, State 12345',
          },
        ];
        
        setStudents(mockStudents);
        
        toast({
          title: "Info",
          description: "Using sample data. Connect to backend for real data.",
          variant: "default",
        });
      }
    } catch (error) {
      console.error('Error loading students:', error);
      toast({
        title: "Error",
        description: "Failed to load students data",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCreateStudent = async () => {
    try {
      await studentsAPI.create(formData);
      toast({
        title: "Success",
        description: "Student created successfully",
      });
      setIsCreateDialogOpen(false);
      setFormData({});
      loadStudents();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create student",
        variant: "destructive",
      });
    }
  };

  const handleUpdateStudent = async () => {
    if (!selectedStudent) return;
    try {
      await studentsAPI.update(selectedStudent.id, formData);
      toast({
        title: "Success",
        description: "Student updated successfully",
      });
      setIsEditDialogOpen(false);
      setFormData({});
      setSelectedStudent(null);
      loadStudents();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update student",
        variant: "destructive",
      });
    }
  };

  const handleDeleteStudent = async (studentId: string) => {
    if (!confirm("Are you sure you want to delete this student?")) return;
    try {
      await studentsAPI.delete(studentId);
      toast({
        title: "Success",
        description: "Student deleted successfully",
      });
      loadStudents();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete student",
        variant: "destructive",
      });
    }
  };

  const filteredStudents = students.filter(
    (student) =>
      student.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.first_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.last_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const openEditDialog = (student: Student) => {
    setSelectedStudent(student);
    setFormData({
      username: student.username,
      email: student.email,
      first_name: student.first_name,
      last_name: student.last_name,
      phone_number: student.phone_number,
      date_of_birth: student.date_of_birth,
      address: student.address,
      emergency_contact: student.emergency_contact,
      parent_guardian: student.parent_guardian,
      student_id: student.student_id,
      grade_level: student.grade_level,
    });
    setIsEditDialogOpen(true);
  };

  const openViewDialog = (student: Student) => {
    setSelectedStudent(student);
    setIsViewDialogOpen(true);
  };

  const openCreateDialog = () => {
    setFormData({});
    setIsCreateDialogOpen(true);
  };

  const getStatusBadge = (status?: string) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800">Active</Badge>;
      case 'inactive':
        return <Badge className="bg-red-100 text-red-800">Inactive</Badge>;
      case 'suspended':
        return <Badge className="bg-yellow-100 text-yellow-800">Suspended</Badge>;
      default:
        return <Badge className="bg-gray-100 text-gray-800">Active</Badge>;
    }
  };

  const renderStudentForm = (isEdit = false) => (
    <div className="grid gap-4 py-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="first_name">First Name</Label>
          <Input
            id="first_name"
            value={formData.first_name || ''}
            onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            placeholder="Enter first name"
          />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="last_name">Last Name</Label>
          <Input
            id="last_name"
            value={formData.last_name || ''}
            onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            placeholder="Enter last name"
          />
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            value={formData.username || ''}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            placeholder="Enter username"
          />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            value={formData.email || ''}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            placeholder="Enter email address"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="student_id">Student ID</Label>
          <Input
            id="student_id"
            value={formData.student_id || ''}
            onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
            placeholder="Enter student ID"
          />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="phone_number">Phone Number</Label>
          <Input
            id="phone_number"
            value={formData.phone_number || ''}
            onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
            placeholder="Enter phone number"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="date_of_birth">Date of Birth</Label>
          <Input
            id="date_of_birth"
            type="date"
            value={formData.date_of_birth || ''}
            onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
          />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="grade_level">Grade Level</Label>
          <Input
            id="grade_level"
            value={formData.grade_level || ''}
            onChange={(e) => setFormData({ ...formData, grade_level: e.target.value })}
            placeholder="Enter grade level"
          />
        </div>
      </div>

      <div className="grid gap-2">
        <Label htmlFor="address">Address</Label>
        <Input
          id="address"
          value={formData.address || ''}
          onChange={(e) => setFormData({ ...formData, address: e.target.value })}
          placeholder="Enter address"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="parent_guardian">Parent/Guardian</Label>
          <Input
            id="parent_guardian"
            value={formData.parent_guardian || ''}
            onChange={(e) => setFormData({ ...formData, parent_guardian: e.target.value })}
            placeholder="Enter parent/guardian name"
          />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="emergency_contact">Emergency Contact</Label>
          <Input
            id="emergency_contact"
            value={formData.emergency_contact || ''}
            onChange={(e) => setFormData({ ...formData, emergency_contact: e.target.value })}
            placeholder="Enter emergency contact"
          />
        </div>
      </div>
    </div>
  );

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Students</h1>
            <p className="text-gray-600">Manage and view all student information</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="flex items-center gap-2">
              <Download className="h-4 w-4" />
              Export
            </Button>
            <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
              <DialogTrigger asChild>
                <Button onClick={openCreateDialog} className="flex items-center gap-2">
                  <Plus className="h-4 w-4" />
                  Add Student
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Add New Student</DialogTitle>
                  <DialogDescription>
                    Create a new student profile with their basic information.
                  </DialogDescription>
                </DialogHeader>
                {renderStudentForm()}
                <DialogFooter>
                  <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={handleCreateStudent}>
                    Create Student
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              All Students ({filteredStudents.length})
            </CardTitle>
            <CardDescription>View and manage student profiles and academic information</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4 mb-6">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search students by name, email, or username..."
                  className="pl-10"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <Button variant="outline" className="flex items-center gap-2">
                <Filter className="h-4 w-4" />
                Filter
              </Button>
            </div>

            {loading ? (
              <div className="flex justify-center items-center py-8">
                <div className="text-gray-500">Loading students...</div>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Student ID</TableHead>
                      <TableHead>Grade Level</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Phone</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredStudents.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={7} className="text-center py-8 text-gray-500">
                          No students found. Click "Add Student" to get started.
                        </TableCell>
                      </TableRow>
                    ) : (
                      filteredStudents.map((student) => (
                        <TableRow key={student.id}>
                          <TableCell className="font-medium">
                            {student.first_name} {student.last_name}
                          </TableCell>
                          <TableCell>{student.email}</TableCell>
                          <TableCell>{student.student_id}</TableCell>
                          <TableCell>
                            <Badge variant="outline">{student.grade_level || 'N/A'}</Badge>
                          </TableCell>
                          <TableCell>{getStatusBadge(student.status)}</TableCell>
                          <TableCell>{student.phone_number || 'N/A'}</TableCell>
                          <TableCell className="text-right">
                            <div className="flex justify-end gap-2">
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => openViewDialog(student)}
                                className="h-8 w-8 p-0"
                              >
                                <Eye className="h-4 w-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => openEditDialog(student)}
                                className="h-8 w-8 p-0"
                              >
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => handleDeleteStudent(student.id)}
                                className="h-8 w-8 p-0 text-red-600 hover:text-red-700"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Edit Student Dialog */}
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Edit Student</DialogTitle>
              <DialogDescription>
                Update student information for {selectedStudent?.first_name} {selectedStudent?.last_name}.
              </DialogDescription>
            </DialogHeader>
            {renderStudentForm(true)}
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleUpdateStudent}>
                Update Student
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* View Student Dialog */}
        <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Student Details</DialogTitle>
              <DialogDescription>
                View complete information for {selectedStudent?.first_name} {selectedStudent?.last_name}.
              </DialogDescription>
            </DialogHeader>
            {selectedStudent && (
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Full Name</Label>
                    <p className="text-sm">{selectedStudent.first_name} {selectedStudent.last_name}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Email</Label>
                    <p className="text-sm">{selectedStudent.email}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Student ID</Label>
                    <p className="text-sm">{selectedStudent.student_id}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Phone Number</Label>
                    <p className="text-sm">{selectedStudent.phone_number || 'N/A'}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Date of Birth</Label>
                    <p className="text-sm">{selectedStudent.date_of_birth || 'N/A'}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Grade Level</Label>
                    <p className="text-sm">{selectedStudent.grade_level || 'N/A'}</p>
                  </div>
                </div>
                <div>
                  <Label className="text-sm font-medium text-gray-500">Address</Label>
                  <p className="text-sm">{selectedStudent.address || 'N/A'}</p>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Parent/Guardian</Label>
                    <p className="text-sm">{selectedStudent.parent_guardian || 'N/A'}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Emergency Contact</Label>
                    <p className="text-sm">{selectedStudent.emergency_contact || 'N/A'}</p>
                  </div>
                </div>
              </div>
            )}
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsViewDialogOpen(false)}>
                Close
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
};

export default StudentsList;
