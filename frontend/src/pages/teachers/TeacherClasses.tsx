
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import { Users, Calendar, Clock, BookOpen, Plus } from "lucide-react";

const TeacherClasses = () => {
  const classes = [
    {
      id: 1,
      name: "Computer Science 101",
      code: "CS101",
      students: 28,
      maxStudents: 30,
      schedule: "Mon, Wed, Fri - 9:00 AM",
      room: "Room 204",
      semester: "Fall 2024",
      progress: 65,
      nextClass: "2024-03-15 09:00",
      status: "Active"
    },
    {
      id: 2,
      name: "Data Structures",
      code: "CS201",
      students: 25,
      maxStudents: 30,
      schedule: "Tue, Thu - 2:00 PM",
      room: "Room 301",
      semester: "Fall 2024",
      progress: 45,
      nextClass: "2024-03-16 14:00",
      status: "Active"
    },
    {
      id: 3,
      name: "Web Development",
      code: "CS305",
      students: 22,
      maxStudents: 25,
      schedule: "Mon, Wed - 11:00 AM",
      room: "Lab 102",
      semester: "Fall 2024",
      progress: 30,
      nextClass: "2024-03-15 11:00",
      status: "Active"
    }
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Classes</h1>
            <p className="text-gray-600">Manage your teaching schedule and classes</p>
          </div>
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            New Class
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {classes.map((classItem) => (
            <Card key={classItem.id} className="border-0 shadow-md hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-lg">{classItem.name}</CardTitle>
                    <CardDescription className="font-medium text-blue-600">
                      {classItem.code}
                    </CardDescription>
                  </div>
                  <Badge variant="secondary">{classItem.status}</Badge>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <Users className="h-4 w-4 text-gray-500" />
                    <span>{classItem.students}/{classItem.maxStudents}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-gray-500" />
                    <span>{classItem.room}</span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="h-4 w-4 text-gray-500" />
                    <span>{classItem.schedule}</span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Course Progress</span>
                    <span>{classItem.progress}%</span>
                  </div>
                  <Progress value={classItem.progress} className="h-2" />
                </div>
                
                <div className="flex gap-2 pt-2">
                  <Button size="sm" className="flex-1">
                    View Details
                  </Button>
                  <Button size="sm" variant="outline">
                    Attendance
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default TeacherClasses;
