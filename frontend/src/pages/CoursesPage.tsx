import React, { useEffect, useState, useCallback } from 'react';
import { coursesAPI, CourseData } from '@/lib/api';
import { useAuth } from '@/contexts/useAuth';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter, CardDescription } from '@/components/ui/card';
import { BookOpen, AlertTriangle, PlusCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const CoursesPage: React.FC = () => {
  const { user } = useAuth();
  const [courses, setCourses] = useState<CourseData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCourses = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await coursesAPI.getAll();
      setCourses(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      console.error("Error fetching courses:", err);
      setError('Failed to load courses. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCourses();
  }, [fetchCourses]);

  if (loading) {
    return <div className="p-6 text-center">Loading courses...</div>;
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert variant="destructive" className="mb-4">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button onClick={fetchCourses}>Try Again</Button>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Courses</h1>
        {user?.role === 'teacher' || user?.role === 'admin' ? (
          <Button asChild>
            <Link to="/courses/new"> {/* Assuming a route for creating new courses */}
              <PlusCircle className="h-4 w-4 mr-2" />
              Create Course
            </Link>
          </Button>
        ) : null}
      </div>

      {courses.length === 0 ? (
        <Card className="text-center">
          <CardHeader>
            <CardTitle>No Courses Found</CardTitle>
          </CardHeader>
          <CardContent>
            <BookOpen className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400">
              {user?.role === 'student' ? "You are not enrolled in any courses yet." : "No courses have been created yet."}
            </p>
            {(user?.role === 'teacher' || user?.role === 'admin') && (
                 <Button asChild className="mt-4">
                    <Link to="/courses/new">Create Your First Course</Link>
                 </Button>
            )}
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map(course => (
            <Card key={course.id} className="flex flex-col">
              <CardHeader>
                <CardTitle>{course.title}</CardTitle>
                <CardDescription>{course.subject_id} - {course.credits} credits</CardDescription> {/* Assuming subject_id can be used here or needs adjustment based on actual data/requirements */}
              </CardHeader>
              <CardContent className="flex-grow">
                <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3">{course.description}</p>
              </CardContent>
              <CardFooter>
                <Button asChild variant="outline" className="w-full">
                  <Link to={`/courses/${course.id}`}>View Details</Link>
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default CoursesPage;
