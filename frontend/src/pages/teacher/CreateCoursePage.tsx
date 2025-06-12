// filepath: c:\\Users\\USER\\PycharmProjects\\edumanage\\frontend\\src\\pages\\teacher\\CreateCoursePage.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { coursesAPI, CourseData } from '@/lib/api';
import { useAuth } from '@/contexts/useAuth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertTriangle, Loader2 } from 'lucide-react';

// Define specific types for form fields if not already in CourseData or if they differ
type CourseDifficulty = 'beginner' | 'intermediate' | 'advanced';
type CourseStatus = 'draft' | 'published' | 'archived';

const CreateCoursePage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [subject, setSubject] = useState(''); // Assuming subject is a string for now
  const [difficultyLevel, setDifficultyLevel] = useState<CourseDifficulty>('intermediate');
  const [status, setStatus] = useState<CourseStatus>('draft');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [maxStudents, setMaxStudents] = useState<number | ''>('');
  const [credits, setCredits] = useState<number | ''>('');
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!title.trim() || !subject.trim()) {
      setError('Title and Subject are required.');
      return;
    }
    if (!user || !user.id) {
        setError('User not authenticated. Cannot create course.');
        return;
    }

    setIsLoading(true);

    const courseData: Partial<CourseData> = {
      title: title.trim(),
      description: description.trim(),
      subject_id: subject.trim(), // Assuming backend handles subject as string or has a way to map it
      instructor_id: String(user.id), // API expects string, converting number to string
      difficulty_level: difficultyLevel,
      status: status,
      start_date: startDate || undefined,
      end_date: endDate || undefined,
      max_students: maxStudents === '' ? undefined : Number(maxStudents),
      credits: credits === '' ? undefined : Number(credits),
    };

    try {
      const newCourse = await coursesAPI.create(courseData as CourseData); // Cast to CourseData
      
      if (newCourse && newCourse.title) {
        // Sanitize the title for display in a template literal
        const displayTitle = String(newCourse.title)
          .replace(/\\/g, '\\\\') // Escape backslashes
          .replace(/`/g, '\\`')    // Escape backticks
          .replace(/\${/g, '\\${'); // Escape ${ sequence
        setSuccessMessage(`Course "${displayTitle}" created successfully!`);
      } else if (newCourse) { 
        setSuccessMessage(`Course (untitled) created successfully!`);
      } else {
        setSuccessMessage('Course creation status uncertain, please check the course list.');
        console.warn('newCourse object was not available or had no title after creation attempt.');
      }
      
      // Reset form or navigate
      setTitle('');
      setDescription('');
      setSubject('');
      setDifficultyLevel('intermediate');
      setStatus('draft');
      setStartDate('');
      setEndDate('');
      setMaxStudents('');
      setCredits('');
      // setTimeout(() => navigate('/teacher/courses'), 2000); // Optional: navigate after a delay
    } catch (err: unknown) {
      console.error('Error creating course:', err);
      if (err instanceof Error) {
        setError(`Failed to create course: ${err.message}`);
      } else {
        setError('An unknown error occurred while creating the course.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 md:p-6">
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl">Create New Course</CardTitle>
          <CardDescription>Fill in the details below to create a new course.</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6">
            {error && (
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            {successMessage && (
              <Alert variant="default" className="bg-green-100 border-green-400 text-green-700">
                <AlertDescription>{successMessage}</AlertDescription>
              </Alert>
            )}
            <div className="space-y-2">
              <Label htmlFor="title">Title <span className="text-red-500">*</span></Label>
              <Input id="title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g., Introduction to Algebra" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="subject">Subject <span className="text-red-500">*</span></Label>
              <Input id="subject" value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="e.g., Mathematics" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="A brief overview of the course content, objectives, and target audience." rows={4}/>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="difficultyLevel">Difficulty Level</Label>
                <Select value={difficultyLevel} onValueChange={(value) => setDifficultyLevel(value as any)}>
                  <SelectTrigger id="difficultyLevel">
                    <SelectValue placeholder="Select difficulty" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="beginner">Beginner</SelectItem>
                    <SelectItem value="intermediate">Intermediate</SelectItem>
                    <SelectItem value="advanced">Advanced</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select value={status} onValueChange={(value) => setStatus(value as any)}>
                  <SelectTrigger id="status">
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="published">Published</SelectItem>
                    <SelectItem value="archived">Archived</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="startDate">Start Date</Label>
                <Input id="startDate" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="endDate">End Date</Label>
                <Input id="endDate" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="maxStudents">Max Students</Label>
                <Input id="maxStudents" type="number" value={maxStudents} onChange={(e) => setMaxStudents(e.target.value === '' ? '' : Number(e.target.value))} placeholder="e.g., 30" min="0" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="credits">Credits</Label>
                <Input id="credits" type="number" value={credits} onChange={(e) => setCredits(e.target.value === '' ? '' : Number(e.target.value))} placeholder="e.g., 3" min="0" />
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button type="submit" disabled={isLoading} className="w-full md:w-auto">
              {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              {isLoading ? 'Creating Course...' : 'Create Course'}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
};

export default CreateCoursePage;
