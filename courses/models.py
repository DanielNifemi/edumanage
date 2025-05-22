from django.db import models
from django.contrib.auth import get_user_model
from teachers.models import Teacher
from students.models import Student
from django.utils import timezone

User = get_user_model()

class Course(models.Model):
    SEMESTER_CHOICES = [
        ('FALL', 'Fall'),
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
    ]

    course_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses_taught')
    students = models.ManyToManyField(Student, through='CourseEnrollment', related_name='enrolled_courses')
    syllabus = models.FileField(upload_to='syllabi/', null=True, blank=True)
    virtual_classroom_link = models.URLField(null=True, blank=True)
    schedule = models.CharField(max_length=200)  # e.g., "Mon/Wed 10 AM"
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'semester', 'course_code']

    def __str__(self):
        return f"{self.course_code}: {self.name} - {self.instructor.user.get_full_name()}"

class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.course_code}"

class CourseContent(models.Model):
    CONTENT_TYPES = [
        ('MATERIAL', 'Course Material'),
        ('ASSIGNMENT', 'Assignment'),
        ('ANNOUNCEMENT', 'Announcement'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='course_contents/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)  # For assignments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course.course_code} - {self.title}"

class Assignment(models.Model):
    content = models.OneToOneField(CourseContent, on_delete=models.CASCADE)
    total_points = models.DecimalField(max_digits=5, decimal_places=2)
    submission_type = models.CharField(max_length=50)  # e.g., "file", "text", "link"
    
    def __str__(self):
        return f"{self.content.title} ({self.total_points} points)"

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='assignment_submissions/', null=True, blank=True)
    submitted_text = models.TextField(null=True, blank=True)
    submitted_url = models.URLField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.content.title}"
