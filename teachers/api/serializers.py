from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Teacher, Subject, Class, Lesson

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details in teacher context"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    teachers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'teachers_count']
        read_only_fields = ['id']
    
    def get_teachers_count(self, obj):
        return obj.teachers.count()


class ClassSerializer(serializers.ModelSerializer):
    """Serializer for Class model"""
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    teacher_id = serializers.CharField(source='teacher.teacher_id', read_only=True)
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher', 'teacher_name', 'teacher_id']
        read_only_fields = ['id']


class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for Teacher model"""
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Subject.objects.all(), source='subjects', write_only=True
    )
    full_name = serializers.SerializerMethodField()
    classes_taught = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'teacher_id', 'subjects', 'subject_ids',
            'qualification', 'department', 'years_of_experience',
            'date_joined', 'created_at', 'updated_at', 'full_name',
            'classes_taught'
        ]
        read_only_fields = ['id', 'teacher_id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_classes_taught(self, obj):
        return obj.classes.count()


class TeacherCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating teachers with user data"""
    user = UserSerializer()
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Subject.objects.all(), source='subjects'
    )
    
    class Meta:
        model = Teacher
        fields = [
            'user', 'subject_ids', 'qualification', 'department',
            'years_of_experience', 'date_joined'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        subjects = validated_data.pop('subjects', [])
        user = User.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, teacher_id='TEMP000', **validated_data)
        teacher.subjects.set(subjects)
        return teacher


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model"""
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'teacher', 'subject', 'class_group', 'date',
            'start_time', 'end_time', 'topic', 'youtube_link',
            'teacher_name', 'subject_name', 'class_name', 'duration'
        ]
        read_only_fields = ['id']
    
    def get_duration(self, obj):
        """Calculate lesson duration in minutes"""
        if obj.start_time and obj.end_time:
            from datetime import datetime, timedelta
            start = datetime.combine(datetime.today(), obj.start_time)
            end = datetime.combine(datetime.today(), obj.end_time)
            duration = end - start
            return int(duration.total_seconds() / 60)
        return None


class TeacherDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for teacher with related data"""
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    classes = ClassSerializer(many=True, read_only=True)
    recent_lessons = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'teacher_id', 'subjects', 'qualification',
            'department', 'years_of_experience', 'date_joined',
            'created_at', 'updated_at', 'full_name', 'classes',
            'recent_lessons'
        ]
        read_only_fields = ['id', 'teacher_id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_recent_lessons(self, obj):
        recent_lessons = obj.lesson_set.order_by('-date', '-start_time')[:5]
        return LessonSerializer(recent_lessons, many=True).data
