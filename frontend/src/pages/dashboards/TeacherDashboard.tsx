import { Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Users, BookOpen, ClipboardCheck, Calendar, PlusCircle, Megaphone, FilePenLine, ArrowRight, GraduationCap, CalendarDays } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import DashboardLayout from "@/components/layout/DashboardLayout";

const TeacherDashboard = () => {
  const { user } = useAuth();

  const myClasses = [
    { id: 1, name: "Calculus I - Section A", students: 28, schedule: "MWF 9:00 AM", room: "Math 101", courseLink: "/teacher/courses/1/details" },
    { id: 2, name: "Calculus I - Section B", students: 25, schedule: "MWF 11:00 AM", room: "Math 102", courseLink: "/teacher/courses/2/details" },
    { id: 3, name: "Statistics", students: 32, schedule: "TTh 2:00 PM", room: "Math 201", courseLink: "/teacher/courses/3/details" },
  ];

  const pendingTasks = [
    { id: 1, task: "Grade Midterm Exams", class: "Calculus I - Section A", due: "Today", priority: "high" as const },
    { id: 2, task: "Prepare Quiz Questions", class: "Statistics", due: "Tomorrow", priority: "medium" as const },
    { id: 3, task: "Update Lesson Plans", class: "Calculus I - Section B", due: "Friday", priority: "low" as const },
  ];

  const todaySchedule = [
    { time: "9:00 AM", class: "Calculus I - Section A", room: "Math 101", type: "lecture" as const },
    { time: "11:00 AM", class: "Calculus I - Section B", room: "Math 102", type: "lecture" as const },
    { time: "2:00 PM", class: "Office Hours", room: "Math 205", type: "office" as const },
  ];

  const quickStatsData = [
    { label: "Total Students", value: myClasses.reduce((acc, item) => acc + item.students, 0).toString(), icon: Users, color: "blue" },
    { label: "Courses Taught", value: myClasses.length.toString(), icon: BookOpen, color: "green" },
    { label: "Pending Tasks", value: pendingTasks.length.toString(), icon: ClipboardCheck, color: "orange" },
    { label: "Classes Today", value: todaySchedule.filter(s => s.type === 'lecture').length.toString(), icon: CalendarDays, color: "purple" },
  ];

  const getPriorityVariant = (priority: 'high' | 'medium' | 'low') => {
    if (priority === 'high') return 'destructive';
    if (priority === 'medium') return 'secondary';
    return 'outline';
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Good morning, Professor {user?.last_name || 'Teacher'}! 📚
          </h1>
          <p className="text-blue-100">
            You have {todaySchedule.filter(s => s.type === 'lecture').length} classes today and {pendingTasks.length} tasks pending. Ready to inspire minds?
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickStatsData.map((stat, index) => (
            <Card key={index} className="border-0 shadow-md">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-500">{stat.label}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                  </div>
                  <div className={`w-12 h-12 bg-${stat.color}-100 rounded-lg flex items-center justify-center`}>
                    <stat.icon className={`h-6 w-6 text-${stat.color}-600`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Today's Schedule */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Today's Schedule
              </CardTitle>
              <CardDescription>Your classes and commitments</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {todaySchedule.length > 0 ? todaySchedule.map((item) => (
                  <div key={item.time + item.class} className="flex items-center justify-between p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-semibold text-sm">{item.time}</p>
                      <p className="text-xs text-gray-600">{item.class} - {item.room}</p>
                    </div>
                    <Badge variant={item.type === 'lecture' ? 'default' : 'secondary'} className="capitalize text-xs">{item.type}</Badge>
                  </div>
                )) : <p className="text-sm text-gray-500">No classes or commitments scheduled for today.</p>}
              </div>
              <Button variant="outline" className="w-full mt-4">
                View Full Schedule
              </Button>
            </CardContent>
          </Card>

          {/* Pending Tasks */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ClipboardCheck className="h-5 w-5" />
                Pending Tasks
              </CardTitle>
              <CardDescription>Items requiring your attention</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {pendingTasks.length > 0 ? pendingTasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-semibold text-sm">{task.task}</p>
                      <p className="text-xs text-gray-600">{task.class} - Due: {task.due}</p>
                    </div>
                    <Badge variant={getPriorityVariant(task.priority)} className="capitalize text-xs">{task.priority}</Badge>
                  </div>
                )) : <p className="text-sm text-gray-500">No pending tasks.</p>}
              </div>
              <Button variant="outline" className="w-full mt-4">
                View All Tasks
              </Button>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Common tasks and shortcuts</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Link to="/teacher/courses/new">
                  <Button variant="outline" className="w-full justify-start">
                    <GraduationCap className="mr-2 h-4 w-4" /> Create New Course
                  </Button>
                </Link>
                <Link to="/teacher/assignments/new">
                  <Button variant="outline" className="w-full justify-start">
                    <PlusCircle className="mr-2 h-4 w-4" /> Create Assignment
                  </Button>
                </Link>
                <Link to="/teacher/announcements/new">
                  <Button variant="outline" className="w-full justify-start">
                    <Megaphone className="mr-2 h-4 w-4" /> Post Announcement
                  </Button>
                </Link>
                <Link to="/teacher/grades">
                  <Button variant="outline" className="w-full justify-start">
                    <FilePenLine className="mr-2 h-4 w-4" /> View/Enter Grades
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* My Classes */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              My Classes
            </CardTitle>
            <CardDescription>Overview of your current courses</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {myClasses.map((classItem) => (
                <Card key={classItem.id} className="shadow-sm hover:shadow-md transition-shadow">
                  <CardHeader>
                    <CardTitle className="text-lg">{classItem.name}</CardTitle>
                    <CardDescription>{classItem.schedule} - {classItem.room}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">Students: {classItem.students}</p>
                  </CardContent>
                  <div className="p-4 pt-0">
                    <Link to={classItem.courseLink || "#"}>
                      <Button variant="outline" className="w-full text-sm">
                        View Details <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default TeacherDashboard;
