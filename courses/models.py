from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from students.models import Student
from teachers.models import Teacher, Subject

User = get_user_model()


class Course(models.Model):
    """Represents a course offering"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateField()
    end_date = models.DateField()
    max_students = models.PositiveIntegerField(default=30)
    credits = models.PositiveIntegerField(default=3)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='prerequisite_for')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Many-to-many relationship with students through enrollment
    students = models.ManyToManyField(Student, through='CourseEnrollment', related_name='enrolled_courses')
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['title', 'subject', 'instructor']
    
    def __str__(self):
        return f"{self.title} ({self.subject.code})"
    
    @property
    def enrollment_count(self):
        return self.enrollments.filter(is_active=True).count()
    
    @property
    def is_full(self):
        return self.enrollment_count >= self.max_students
    
    @property
    def completion_rate(self):
        total_enrolled = self.enrollment_count
        if total_enrolled == 0:
            return 0
        completed = self.enrollments.filter(is_active=True, completion_date__isnull=False).count()
        return round((completed / total_enrolled) * 100, 2)


class CourseEnrollment(models.Model):
    """Tracks student enrollment in courses"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    final_grade = models.CharField(max_length=2, blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-date_enrolled']
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
    @property
    def is_completed(self):
        return self.completion_date is not None


class CourseContent(models.Model):
    """Represents content items within a course"""
    CONTENT_TYPES = [
        ('lecture', 'Lecture'),
        ('video', 'Video'),
        ('reading', 'Reading Material'),
        ('assignment', 'Assignment'),
        ('quiz', 'Quiz'),
        ('discussion', 'Discussion'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    description = models.TextField(blank=True)
    content_url = models.URLField(blank=True, null=True)
    file_upload = models.FileField(upload_to='course_content/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)
    estimated_duration = models.DurationField(null=True, blank=True)  # in minutes
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Assignment(models.Model):
    """Represents assignments within course content"""
    SUBMISSION_TYPES = [
        ('file', 'File Upload'),
        ('text', 'Text Submission'),
        ('url', 'URL/Link'),
        ('multiple', 'Multiple Types'),
    ]
    
    content = models.OneToOneField(CourseContent, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    total_points = models.DecimalField(max_digits=5, decimal_places=2)
    submission_type = models.CharField(max_length=20, choices=SUBMISSION_TYPES)
    instructions = models.TextField()
    allow_late_submission = models.BooleanField(default=False)
    late_penalty_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Assignment: {self.content.title}"
    
    @property
    def is_overdue(self):
        return timezone.now() > self.due_date


class AssignmentSubmission(models.Model):
    """Tracks student submissions for assignments"""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='assignment_submissions/', blank=True, null=True)
    submitted_text = models.TextField(blank=True, null=True)
    submitted_url = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student} - {self.assignment.content.title}"
    
    @property
    def is_late(self):
        return self.submitted_at > self.assignment.due_date
    
    @property
    def is_graded(self):
        return self.grade is not None


class CourseAnnouncement(models.Model):
    """Course-specific announcements"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_pinned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
