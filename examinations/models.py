from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from students.models import Student
from teachers.models import Teacher
from courses.models import Course


class Exam(models.Model):
    """Enhanced Exam model for comprehensive assessment management"""
    EXAM_TYPES = [
        ('exam', 'Final Exam'),
        ('midterm', 'Midterm Exam'),
        ('test', 'Test/Quiz'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('practical', 'Practical Exam'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='test')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    subject = models.CharField(max_length=100)  # Keep for backward compatibility
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='created_exams')
    
    # Scheduling
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    
    # Grading
    max_marks = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    
    # Instructions and settings
    instructions = models.TextField(blank=True)
    allow_late_submission = models.BooleanField(default=False)
    late_penalty_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    randomize_questions = models.BooleanField(default=False)
    show_results_immediately = models.BooleanField(default=False)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    students = models.ManyToManyField(Student, through='ExamResult', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
    @property
    def is_active(self):
        now = timezone.now()
        exam_start = timezone.datetime.combine(self.date, self.start_time)
        exam_end = timezone.datetime.combine(self.date, self.end_time)
        return exam_start <= now <= exam_end
    
    @property
    def is_upcoming(self):
        now = timezone.now()
        exam_start = timezone.datetime.combine(self.date, self.start_time)
        return now < exam_start
    
    @property
    def is_completed(self):
        now = timezone.now()
        exam_end = timezone.datetime.combine(self.date, self.end_time)
        return now > exam_end


class ExamResult(models.Model):
    """Enhanced ExamResult model for detailed grading"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    
    # Scores and grading
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade_letter = models.CharField(max_length=2, blank=True)
    is_graded = models.BooleanField(default=False)
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_exams')
    graded_at = models.DateTimeField(null=True, blank=True)
    
    # Feedback and comments
    grade_comment = models.TextField(blank=True)
    teacher_feedback = models.TextField(blank=True)
    
    # Submission tracking
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_taken_minutes = models.PositiveIntegerField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    
    # Additional metadata
    attempt_number = models.PositiveIntegerField(default=1)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['exam', 'student']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.title}"
    
    def save(self, *args, **kwargs):
        # Calculate percentage if score is provided
        if self.score is not None and self.exam.max_marks > 0:
            self.percentage = (self.score / self.exam.max_marks) * 100
            
        # Calculate letter grade based on percentage
        if self.percentage is not None:
            if self.percentage >= 90:
                self.grade_letter = 'A+'
            elif self.percentage >= 85:
                self.grade_letter = 'A'
            elif self.percentage >= 80:
                self.grade_letter = 'A-'
            elif self.percentage >= 75:
                self.grade_letter = 'B+'
            elif self.percentage >= 70:
                self.grade_letter = 'B'
            elif self.percentage >= 65:
                self.grade_letter = 'B-'
            elif self.percentage >= 60:
                self.grade_letter = 'C+'
            elif self.percentage >= 55:
                self.grade_letter = 'C'
            elif self.percentage >= 50:
                self.grade_letter = 'C-'
            else:
                self.grade_letter = 'F'
        
        # Prevent students from changing their exam scores (security measure)
        if self.pk:
            try:
                original_instance = ExamResult.objects.get(pk=self.pk)
                if original_instance.score != self.score and not self.graded_by:
                    self.score = original_instance.score
            except ExamResult.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    @property
    def is_passed(self):
        return self.score is not None and self.score >= self.exam.passing_marks


class Test(models.Model):
    """Specific model for tests/quizzes with questions"""
    TEST_TYPES = [
        ('quiz', 'Quiz'),
        ('test', 'Test'),
        ('practice', 'Practice Test'),
        ('assessment', 'Assessment'),
    ]
    
    QUESTION_DISPLAY = [
        ('all', 'All at Once'),
        ('one', 'One at a Time'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    test_type = models.CharField(max_length=20, choices=TEST_TYPES, default='test')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='created_tests')
    
    # Timing and availability
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()
    time_limit_minutes = models.PositiveIntegerField(help_text="Time limit in minutes")
    
    # Settings
    max_attempts = models.PositiveIntegerField(default=1)
    shuffle_questions = models.BooleanField(default=False)
    shuffle_answers = models.BooleanField(default=False)
    question_display = models.CharField(max_length=10, choices=QUESTION_DISPLAY, default='all')
    show_correct_answers = models.BooleanField(default=False)
    show_feedback = models.BooleanField(default=True)
    
    # Grading
    total_points = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    passing_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Status
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
    @property
    def is_available(self):
        now = timezone.now()
        return self.available_from <= now <= self.available_until
    
    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    """Question model for tests"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('matching', 'Matching'),
        ('fill_blank', 'Fill in the Blank'),
    ]
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    order = models.PositiveIntegerField(default=0)
    
    # Optional question image
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    
    # Explanation for the correct answer
    explanation = models.TextField(blank=True)
    
    # Additional settings
    is_required = models.BooleanField(default=True)
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['test', 'order']
        unique_together = ['test', 'order']
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."


class Answer(models.Model):
    """Answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    # Optional answer image
    image = models.ImageField(upload_to='answer_images/', blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.answer_text[:30]}..."


class TestAttempt(models.Model):
    """Student test attempts"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_attempts')
    
    # Timing
    started_at = models.DateTimeField()
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_taken_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Scoring
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_graded = models.BooleanField(default=False)
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_submitted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField()
    
    # Additional data
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['test', 'student', 'attempt_number']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.test.title} (Attempt {self.attempt_number})"
    
    @property
    def is_passed(self):
        return self.score is not None and self.score >= self.test.passing_score


class StudentAnswer(models.Model):
    """Student answers for test questions"""
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='student_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(blank=True)  # For short answer, essay questions
    
    # Grading (for manually graded questions)
    points_earned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    teacher_feedback = models.TextField(blank=True)
    is_graded = models.BooleanField(default=False)
    
    # Timing
    time_spent_seconds = models.PositiveIntegerField(null=True, blank=True)
    answered_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.student.user.get_full_name()} - Q{self.question.order}"
    
    @property
    def is_correct(self):
        if self.selected_answer:
            return self.selected_answer.is_correct
        return False
