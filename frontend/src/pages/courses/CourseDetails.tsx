
import { useParams, Link } from "react-router-dom";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { BookOpen, Clock, Users, Star, Play, Download, ArrowLeft } from "lucide-react";

const CourseDetails = () => {
  const { id } = useParams();

  // Mock course data - replace with API call
  const course = {
    id: id,
    title: "Introduction to Computer Science",
    instructor: "Dr. Smith",
    department: "Computer Science",
    credits: 3,
    students: 45,
    duration: "15 weeks",
    difficulty: "Beginner",
    rating: 4.8,
    description: "This comprehensive course introduces fundamental concepts of programming and computer science. Students will learn problem-solving techniques, basic algorithms, and programming fundamentals using modern languages.",
    progress: 65,
    lessons: [
      { id: 1, title: "Introduction to Programming", duration: "45 min", completed: true },
      { id: 2, title: "Variables and Data Types", duration: "60 min", completed: true },
      { id: 3, title: "Control Structures", duration: "75 min", completed: false },
      { id: 4, title: "Functions and Methods", duration: "90 min", completed: false },
    ]
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Link to="/courses">
            <Button variant="outline" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Courses
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Course Info */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-2xl">{course.title}</CardTitle>
                    <CardDescription className="text-lg">
                      Instructor: {course.instructor}
                    </CardDescription>
                  </div>
                  <Badge variant="outline">{course.department}</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-6">{course.description}</p>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-1">
                      <BookOpen className="h-4 w-4 text-gray-500" />
                    </div>
                    <p className="font-medium">{course.credits}</p>
                    <p className="text-sm text-gray-600">Credits</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-1">
                      <Users className="h-4 w-4 text-gray-500" />
                    </div>
                    <p className="font-medium">{course.students}</p>
                    <p className="text-sm text-gray-600">Students</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-1">
                      <Clock className="h-4 w-4 text-gray-500" />
                    </div>
                    <p className="font-medium">{course.duration}</p>
                    <p className="text-sm text-gray-600">Duration</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-1">
                      <Star className="h-4 w-4 text-gray-500" />
                    </div>
                    <p className="font-medium">{course.rating}</p>
                    <p className="text-sm text-gray-600">Rating</p>
                  </div>
                </div>

                <div className="mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">Course Progress</span>
                    <span className="text-sm text-gray-600">{course.progress}%</span>
                  </div>
                  <Progress value={course.progress} />
                </div>
              </CardContent>
            </Card>

            {/* Lessons */}
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Course Content</CardTitle>
                <CardDescription>Lessons and materials</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {course.lessons.map((lesson) => (
                    <div key={lesson.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          lesson.completed ? 'bg-green-500 text-white' : 'bg-gray-300'
                        }`}>
                          {lesson.completed ? '✓' : lesson.id}
                        </div>
                        <div>
                          <h4 className="font-medium">{lesson.title}</h4>
                          <p className="text-sm text-gray-600">{lesson.duration}</p>
                        </div>
                      </div>
                      <Button size="sm" variant={lesson.completed ? "outline" : "default"}>
                        <Play className="h-4 w-4 mr-2" />
                        {lesson.completed ? 'Review' : 'Start'}
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card className="border-0 shadow-md">
              <CardContent className="p-6">
                <Button className="w-full mb-4">
                  Continue Learning
                </Button>
                <Button variant="outline" className="w-full mb-4">
                  <Download className="h-4 w-4 mr-2" />
                  Download Materials
                </Button>
                <Button variant="outline" className="w-full">
                  Contact Instructor
                </Button>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle>Course Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Completion Rate</span>
                    <span className="font-medium">85%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Average Grade</span>
                    <span className="font-medium">B+</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Time Remaining</span>
                    <span className="font-medium">8 weeks</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default CourseDetails;
