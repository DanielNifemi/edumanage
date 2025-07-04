from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import (
    Exam, ExamResult, Test, Question, Answer, 
    TestAttempt, StudentAnswer
)
from students.models import Student
from teachers.models import Teacher
from courses.models import Course

User = get_user_model()


class TeacherBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for teacher in exam context"""
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_id', 'full_name']
        read_only_fields = ['id', 'teacher_id']


class StudentBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for student in exam context"""
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'full_name']
        read_only_fields = ['id', 'student_id']


class CourseBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for course in exam context"""
    class Meta:
        model = Course
        fields = ['id', 'title', 'code']
        read_only_fields = ['id']


# Enhanced Exam Serializers
class ExamSerializer(serializers.ModelSerializer):
    """Enhanced serializer for Exam model"""
    created_by_name = serializers.CharField(source='created_by.user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.title', read_only=True)
    student_count = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    is_active = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'description', 'exam_type', 'course', 'course_name',
            'subject', 'created_by', 'created_by_name', 'date', 'start_time', 
            'end_time', 'duration_minutes', 'max_marks', 'passing_marks',
            'instructions', 'allow_late_submission', 'late_penalty_percent',
            'randomize_questions', 'show_results_immediately', 'status',
            'student_count', 'average_score', 'is_active', 'is_upcoming', 
            'is_completed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_student_count(self, obj):
        return obj.students.count()
    
    def get_average_score(self, obj):
        results = obj.results.filter(is_graded=True)
        if results.exists():
            scores = [result.score for result in results if result.score is not None]
            return round(sum(scores) / len(scores), 2) if scores else None
        return None
class ExamResultSerializer(serializers.ModelSerializer):
    """Enhanced serializer for Exam Result model"""
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    graded_by_name = serializers.CharField(source='graded_by.user.get_full_name', read_only=True)
    is_passed = serializers.ReadOnlyField()
    
    class Meta:
        model = ExamResult
        fields = [
            'id', 'exam', 'student', 'score', 'percentage', 'grade_letter',
            'is_graded', 'graded_by', 'graded_at', 'grade_comment', 'teacher_feedback',
            'started_at', 'submitted_at', 'time_taken_minutes', 'is_submitted',
            'is_late', 'attempt_number', 'exam_title', 'student_name',
            'student_id', 'graded_by_name', 'is_passed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'percentage', 'grade_letter', 'is_passed', 'created_at', 'updated_at']


class ExamCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating exams"""
    student_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all(), write_only=True
    )
    
    class Meta:
        model = Exam
        fields = [
            'title', 'description', 'exam_type', 'course', 'subject',
            'date', 'start_time', 'end_time', 'duration_minutes',
            'max_marks', 'passing_marks', 'instructions',
            'allow_late_submission', 'late_penalty_percent',
            'randomize_questions', 'show_results_immediately',
            'status', 'student_ids'
        ]
    
    def create(self, validated_data):
        student_ids = validated_data.pop('student_ids', [])
        exam = Exam.objects.create(**validated_data)
        
        # Create exam results for selected students
        exam_results = []
        for student in student_ids:
            exam_results.append(
                ExamResult(exam=exam, student=student)
            )
        ExamResult.objects.bulk_create(exam_results)
        
        return exam


# Test/Quiz Serializers
class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for answer choices"""
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'order', 'image']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for test questions"""
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'points', 'order',
            'image', 'explanation', 'is_required', 'time_limit_seconds',
            'answers'
        ]
        read_only_fields = ['id']


class TestSerializer(serializers.ModelSerializer):
    """Serializer for Test model"""
    created_by_name = serializers.CharField(source='created_by.user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.title', read_only=True)
    question_count = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Test
        fields = [
            'id', 'title', 'description', 'test_type', 'course', 'course_name',
            'created_by', 'created_by_name', 'available_from', 'available_until',
            'time_limit_minutes', 'max_attempts', 'shuffle_questions',
            'shuffle_answers', 'question_display', 'show_correct_answers',
            'show_feedback', 'total_points', 'passing_score', 'is_published',
            'question_count', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']


class TestDetailSerializer(TestSerializer):
    """Detailed serializer for test with questions"""
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta(TestSerializer.Meta):
        fields = TestSerializer.Meta.fields + ['questions']


class StudentAnswerSerializer(serializers.ModelSerializer):
    """Serializer for student answers"""
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    is_correct = serializers.ReadOnlyField()
    
    class Meta:
        model = StudentAnswer
        fields = [
            'id', 'question', 'question_text', 'selected_answer', 'text_answer',
            'points_earned', 'teacher_feedback', 'is_graded', 'is_correct',
            'time_spent_seconds', 'answered_at'
        ]
        read_only_fields = ['id', 'answered_at']


class TestAttemptSerializer(serializers.ModelSerializer):
    """Serializer for test attempts"""
    test_title = serializers.CharField(source='test.title', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    is_passed = serializers.ReadOnlyField()
    
    class Meta:
        model = TestAttempt
        fields = [
            'id', 'test', 'student', 'test_title', 'student_name',
            'started_at', 'submitted_at', 'time_taken_seconds',
            'score', 'percentage', 'is_graded', 'graded_by', 'graded_at',
            'is_submitted', 'is_completed', 'attempt_number', 'is_passed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TestAttemptDetailSerializer(TestAttemptSerializer):
    """Detailed serializer for test attempts with answers"""
    student_answers = StudentAnswerSerializer(many=True, read_only=True)
    
    class Meta(TestAttemptSerializer.Meta):
        fields = TestAttemptSerializer.Meta.fields + ['student_answers']


# Grading Serializers
class BulkGradeExamSerializer(serializers.Serializer):
    """Serializer for bulk grading exams"""
    exam_results = serializers.ListField(
        child=serializers.DictField(), 
        help_text="List of exam result updates with result_id, score, and optional comments"
    )
    
    def validate_exam_results(self, value):
        if not value:
            raise serializers.ValidationError("At least one exam result must be provided")
        
        for result_data in value:
            if 'result_id' not in result_data:
                raise serializers.ValidationError("result_id is required for each result")
            if 'score' not in result_data:
                raise serializers.ValidationError("score is required for each result")
            
            try:
                float(result_data['score'])
            except (ValueError, TypeError):
                raise serializers.ValidationError("Score must be a valid number")
        
        return value


class BulkGradeTestSerializer(serializers.Serializer):
    """Serializer for bulk grading test answers"""
    student_answers = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of student answer updates with answer_id, points_earned, and optional feedback"
    )
    
    def validate_student_answers(self, value):
        if not value:
            raise serializers.ValidationError("At least one student answer must be provided")
        
        for answer_data in value:
            if 'answer_id' not in answer_data:
                raise serializers.ValidationError("answer_id is required for each answer")
            if 'points_earned' not in answer_data:
                raise serializers.ValidationError("points_earned is required for each answer")
            
            try:
                float(answer_data['points_earned'])
            except (ValueError, TypeError):
                raise serializers.ValidationError("Points earned must be a valid number")
        
        return value


# Statistics Serializers
class ExamStatsSerializer(serializers.Serializer):
    """Serializer for exam statistics"""
    total_exams = serializers.IntegerField()
    exams_this_month = serializers.IntegerField()
    total_students_examined = serializers.IntegerField()
    average_score = serializers.FloatField()
    highest_score = serializers.FloatField()
    lowest_score = serializers.FloatField()
    pass_rate = serializers.FloatField()
    recent_exams = ExamSerializer(many=True)
    
    
class TestStatsSerializer(serializers.Serializer):
    """Serializer for test statistics"""
    total_tests = serializers.IntegerField()
    tests_this_month = serializers.IntegerField()
    total_attempts = serializers.IntegerField()
    average_score = serializers.FloatField()
    completion_rate = serializers.FloatField()
    recent_tests = TestSerializer(many=True)
