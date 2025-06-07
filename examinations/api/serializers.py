from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Exam, ExamResult
from students.models import Student
from teachers.models import Teacher

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


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for Exam model"""
    created_by_name = serializers.CharField(source='created_by.user.get_full_name', read_only=True)
    student_count = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'date', 'subject', 'created_by',
            'created_by_name', 'student_count', 'average_score'
        ]
        read_only_fields = ['id']
    
    def get_student_count(self, obj):
        return obj.students.count()
    
    def get_average_score(self, obj):
        results = obj.examresult_set.filter(is_graded=True)
        if results:
            return round(sum(result.score for result in results) / len(results), 2)
        return None


class ExamResultSerializer(serializers.ModelSerializer):
    """Serializer for Exam Result model"""
    exam_name = serializers.CharField(source='exam.name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    graded_by_name = serializers.CharField(source='graded_by.user.get_full_name', read_only=True)
    grade_letter = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamResult
        fields = [
            'id', 'exam', 'student', 'score', 'is_graded',
            'graded_by', 'grade_comment', 'exam_name', 'student_name',
            'student_id', 'graded_by_name', 'grade_letter'
        ]
        read_only_fields = ['id']
    
    def get_grade_letter(self, obj):
        """Convert score to letter grade"""
        if obj.score >= 90:
            return 'A'
        elif obj.score >= 80:
            return 'B'
        elif obj.score >= 70:
            return 'C'
        elif obj.score >= 60:
            return 'D'
        else:
            return 'F'


class ExamDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for exam with results"""
    created_by = TeacherBasicSerializer(read_only=True)
    results = ExamResultSerializer(source='examresult_set', many=True, read_only=True)
    statistics = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'date', 'subject', 'created_by',
            'results', 'statistics'
        ]
        read_only_fields = ['id']
    
    def get_statistics(self, obj):
        results = obj.examresult_set.filter(is_graded=True)
        if not results:
            return None
            
        scores = [result.score for result in results]
        return {
            'total_students': len(scores),
            'average_score': round(sum(scores) / len(scores), 2) if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'lowest_score': min(scores) if scores else 0,
            'pass_rate': len([s for s in scores if s >= 60]) / len(scores) * 100 if scores else 0
        }


class ExamCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating exams"""
    student_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all(), source='students', write_only=True
    )
    
    class Meta:
        model = Exam
        fields = ['name', 'date', 'subject', 'created_by', 'student_ids']
    
    def create(self, validated_data):
        students = validated_data.pop('students', [])
        exam = Exam.objects.create(**validated_data)
        
        # Create exam results for all students
        exam_results = []
        for student in students:
            exam_results.append(
                ExamResult(exam=exam, student=student, score=0, is_graded=False)
            )
        ExamResult.objects.bulk_create(exam_results)
        
        return exam


class BulkGradeSerializer(serializers.Serializer):
    """Serializer for bulk grading"""
    results = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    graded_by = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    
    def update_grades(self):
        graded_by = self.validated_data['graded_by']
        results_data = self.validated_data['results']
        
        updated_results = []
        for result_data in results_data:
            try:
                result = ExamResult.objects.get(id=result_data['id'])
                result.score = int(result_data['score'])
                result.grade_comment = result_data.get('grade_comment', '')
                result.graded_by = graded_by
                result.is_graded = True
                updated_results.append(result)
            except (ExamResult.DoesNotExist, ValueError):
                continue
        
        ExamResult.objects.bulk_update(
            updated_results, 
            ['score', 'grade_comment', 'graded_by', 'is_graded']
        )
        return updated_results


class BulkGradingSerializer(serializers.Serializer):
    """Serializer for bulk grading operations"""
    exam_results = serializers.ListField(
        child=serializers.DictField(), 
        help_text="List of exam result updates"
    )
    
    def validate_exam_results(self, value):
        """Validate exam results data"""
        if not value:
            raise serializers.ValidationError("At least one exam result must be provided")
        
        required_fields = ['result_id', 'score']
        for result_data in value:
            for field in required_fields:
                if field not in result_data:
                    raise serializers.ValidationError(f"Field '{field}' is required for each result")
            
            try:
                float(result_data['score'])
            except (ValueError, TypeError):
                raise serializers.ValidationError("Score must be a valid number")
        
        return value


class ExamResultDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for exam results with complete information"""
    exam = ExamSerializer(read_only=True)
    student = StudentBasicSerializer(read_only=True)
    graded_by = TeacherBasicSerializer(read_only=True)
    grade_letter = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamResult
        fields = [
            'id', 'exam', 'student', 'score', 'is_graded',
            'graded_by', 'grade_comment', 'grade_letter', 'percentage'
        ]
        read_only_fields = ['id']
    
    def get_grade_letter(self, obj):
        """Convert score to letter grade"""
        if obj.score >= 90:
            return 'A'
        elif obj.score >= 80:
            return 'B'
        elif obj.score >= 70:
            return 'C'
        elif obj.score >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_percentage(self, obj):
        """Get percentage score - assuming max score is 100"""
        return obj.score


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
    top_performers = serializers.SerializerMethodField()  # Changed to avoid circular reference
    
    def get_top_performers(self, obj):
        # Return basic info instead of full serializer to avoid circular import
        return obj.get('top_performers', [])
