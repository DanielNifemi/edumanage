from rest_framework import serializers
from django.utils import timezone
from ..models import (
    Course, CourseEnrollment, CourseContent, Assignment, 
    AssignmentSubmission, CourseAnnouncement
)
from students.models import Student
from teachers.models import Teacher, Subject


class SubjectSimpleSerializer(serializers.ModelSerializer):
    """Simple serializer for subject information"""
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']


class TeacherSimpleSerializer(serializers.ModelSerializer):
    """Simple serializer for teacher information"""
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_id', 'full_name', 'department']


class StudentSimpleSerializer(serializers.ModelSerializer):
    """Simple serializer for student information"""
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'full_name', 'grade']


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for course list view"""
    subject = SubjectSimpleSerializer(read_only=True)
    instructor = TeacherSimpleSerializer(read_only=True)
    enrollment_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    completion_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'subject', 'instructor',
            'difficulty_level', 'status', 'start_date', 'end_date',
            'max_students', 'credits', 'enrollment_count', 'is_full',
            'completion_rate', 'thumbnail', 'created_at'
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for course with all information"""
    subject = SubjectSimpleSerializer(read_only=True)
    instructor = TeacherSimpleSerializer(read_only=True)
    prerequisites = CourseListSerializer(many=True, read_only=True)
    enrollment_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    completion_rate = serializers.ReadOnlyField()
    content_count = serializers.SerializerMethodField()
    assignment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'subject', 'instructor',
            'difficulty_level', 'status', 'start_date', 'end_date',
            'max_students', 'credits', 'prerequisites', 'enrollment_count',
            'is_full', 'completion_rate', 'content_count', 'assignment_count',
            'thumbnail', 'created_at', 'updated_at'
        ]
    
    def get_content_count(self, obj):
        return obj.contents.count()
    
    def get_assignment_count(self, obj):
        return Assignment.objects.filter(content__course=obj).count()


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating courses"""
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'subject', 'instructor',
            'difficulty_level', 'status', 'start_date', 'end_date',
            'max_students', 'credits', 'prerequisites', 'thumbnail'
        ]
    
    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] <= data['start_date']:
                raise serializers.ValidationError(
                    "End date must be after start date."
                )
        return data


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for course enrollments"""
    student = StudentSimpleSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    is_completed = serializers.ReadOnlyField()
    days_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseEnrollment
        fields = [
            'id', 'student', 'course', 'date_enrolled', 'is_active',
            'completion_date', 'final_grade', 'progress_percentage',
            'is_completed', 'days_enrolled'
        ]
    
    def get_days_enrolled(self, obj):
        return (timezone.now().date() - obj.date_enrolled.date()).days


class CourseEnrollmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating enrollments"""
    
    class Meta:
        model = CourseEnrollment
        fields = ['student', 'course']
    
    def validate(self, data):
        # Check if student is already enrolled
        if CourseEnrollment.objects.filter(
            student=data['student'], 
            course=data['course'],
            is_active=True
        ).exists():
            raise serializers.ValidationError(
                "Student is already enrolled in this course."
            )
        
        # Check if course is full
        if data['course'].is_full:
            raise serializers.ValidationError(
                "Course has reached maximum enrollment capacity."
            )
        
        return data


class CourseContentSerializer(serializers.ModelSerializer):
    """Serializer for course content"""
    estimated_duration_minutes = serializers.SerializerMethodField()
    has_assignment = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseContent
        fields = [
            'id', 'course', 'title', 'content_type', 'description',
            'content_url', 'file_upload', 'order', 'is_required',
            'estimated_duration', 'estimated_duration_minutes',
            'has_assignment', 'created_at', 'updated_at'
        ]
    
    def get_estimated_duration_minutes(self, obj):
        if obj.estimated_duration:
            return int(obj.estimated_duration.total_seconds() / 60)
        return None
    
    def get_has_assignment(self, obj):
        return hasattr(obj, 'assignment')


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for assignments"""
    content = CourseContentSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()
    submission_count = serializers.SerializerMethodField()
    graded_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'content', 'due_date', 'total_points', 'submission_type',
            'instructions', 'allow_late_submission', 'late_penalty_per_day',
            'is_overdue', 'submission_count', 'graded_count'
        ]
    
    def get_submission_count(self, obj):
        return obj.submissions.count()
    
    def get_graded_count(self, obj):
        return obj.submissions.filter(grade__isnull=False).count()


class AssignmentCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating assignments"""
    
    class Meta:
        model = Assignment
        fields = [
            'content', 'due_date', 'total_points', 'submission_type',
            'instructions', 'allow_late_submission', 'late_penalty_per_day'
        ]
    
    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Due date must be in the future."
            )
        return value


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for assignment submissions"""
    assignment = AssignmentSerializer(read_only=True)
    student = StudentSimpleSerializer(read_only=True)
    graded_by = TeacherSimpleSerializer(read_only=True)
    is_late = serializers.ReadOnlyField()
    is_graded = serializers.ReadOnlyField()
    days_since_submission = serializers.SerializerMethodField()
    
    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'student', 'submitted_file', 'submitted_text',
            'submitted_url', 'submitted_at', 'grade', 'feedback',
            'graded_by', 'graded_at', 'is_late', 'is_graded',
            'days_since_submission'
        ]
    
    def get_days_since_submission(self, obj):
        return (timezone.now().date() - obj.submitted_at.date()).days


class AssignmentSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating assignment submissions"""
    
    class Meta:
        model = AssignmentSubmission
        fields = [
            'assignment', 'submitted_file', 'submitted_text', 'submitted_url'
        ]
    
    def validate(self, data):
        assignment = data['assignment']
        
        # Check if assignment allows late submission
        if timezone.now() > assignment.due_date and not assignment.allow_late_submission:
            raise serializers.ValidationError(
                "This assignment no longer accepts submissions."
            )
        
        # Ensure at least one submission field is provided
        submission_fields = ['submitted_file', 'submitted_text', 'submitted_url']
        if not any(data.get(field) for field in submission_fields):
            raise serializers.ValidationError(
                "At least one submission field must be provided."
            )
        
        return data


class AssignmentGradingSerializer(serializers.ModelSerializer):
    """Serializer for grading assignments"""
    
    class Meta:
        model = AssignmentSubmission
        fields = ['grade', 'feedback']
    
    def validate_grade(self, value):
        if value < 0:
            raise serializers.ValidationError("Grade cannot be negative.")
        
        # Get the assignment from context or instance
        assignment = None
        if self.instance:
            assignment = self.instance.assignment
        elif 'assignment' in self.context:
            assignment = self.context['assignment']
        
        if assignment and value > assignment.total_points:
            raise serializers.ValidationError(
                f"Grade cannot exceed total points ({assignment.total_points})."
            )
        
        return value


class CourseAnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for course announcements"""
    created_by = TeacherSimpleSerializer(read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = CourseAnnouncement
        fields = [
            'id', 'course', 'course_title', 'title', 'content',
            'created_by', 'created_at', 'is_pinned'
        ]


class CourseStatsSerializer(serializers.Serializer):
    """Serializer for course statistics"""
    total_courses = serializers.IntegerField()
    active_courses = serializers.IntegerField()
    draft_courses = serializers.IntegerField()
    archived_courses = serializers.IntegerField()
    total_enrollments = serializers.IntegerField()
    total_students = serializers.IntegerField()
    average_completion_rate = serializers.FloatField()
    most_popular_courses = CourseListSerializer(many=True)
    recent_enrollments = CourseEnrollmentSerializer(many=True)
