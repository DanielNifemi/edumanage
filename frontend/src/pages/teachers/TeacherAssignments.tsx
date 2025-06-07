
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar, Clock, Users, FileText, Plus, Eye } from "lucide-react";

const TeacherAssignments = () => {
  const assignments = [
    {
      id: 1,
      title: "JavaScript Fundamentals Quiz",
      course: "Web Development",
      dueDate: "2024-03-20",
      submissions: 18,
      totalStudents: 22,
      status: "Active",
      type: "Quiz"
    },
    {
      id: 2,
      title: "Database Design Project",
      course: "Data Structures",
      dueDate: "2024-03-25",
      submissions: 12,
      totalStudents: 25,
      status: "Active",
      type: "Project"
    },
    {
      id: 3,
      title: "Algorithm Analysis",
      course: "Computer Science 101",
      dueDate: "2024-03-15",
      submissions: 28,
      totalStudents: 28,
      status: "Completed",
      type: "Assignment"
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'bg-green-100 text-green-800';
      case 'Completed': return 'bg-blue-100 text-blue-800';
      case 'Overdue': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Assignments</h1>
            <p className="text-gray-600">Create and manage assignments for your classes</p>
          </div>
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Create Assignment
          </Button>
        </div>

        <Tabs defaultValue="all" className="space-y-4">
          <TabsList>
            <TabsTrigger value="all">All Assignments</TabsTrigger>
            <TabsTrigger value="active">Active</TabsTrigger>
            <TabsTrigger value="completed">Completed</TabsTrigger>
            <TabsTrigger value="grading">Need Grading</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="space-y-4">
            <div className="grid gap-4">
              {assignments.map((assignment) => (
                <Card key={assignment.id} className="border-0 shadow-md">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold">{assignment.title}</h3>
                          <Badge className={getStatusColor(assignment.status)}>
                            {assignment.status}
                          </Badge>
                          <Badge variant="outline">{assignment.type}</Badge>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-600">
                          <div className="flex items-center gap-2">
                            <FileText className="h-4 w-4" />
                            <span>{assignment.course}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Calendar className="h-4 w-4" />
                            <span>Due: {assignment.dueDate}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Users className="h-4 w-4" />
                            <span>{assignment.submissions}/{assignment.totalStudents} submitted</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Clock className="h-4 w-4" />
                            <span>Created 3 days ago</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline" className="flex items-center gap-1">
                          <Eye className="h-3 w-3" />
                          View
                        </Button>
                        <Button size="sm">Grade</Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="active">
            <div className="text-center py-8">
              <p className="text-gray-500">Active assignments will be shown here</p>
            </div>
          </TabsContent>

          <TabsContent value="completed">
            <div className="text-center py-8">
              <p className="text-gray-500">Completed assignments will be shown here</p>
            </div>
          </TabsContent>

          <TabsContent value="grading">
            <div className="text-center py-8">
              <p className="text-gray-500">Assignments needing grading will be shown here</p>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
};

export default TeacherAssignments;
