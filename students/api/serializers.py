from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Student, AcademicRecord

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details in student context"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    user = UserSerializer(read_only=True)
    user_details = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'date_of_birth', 'grade', 
            'address', 'parent_name', 'parent_contact', 'user_details', 'full_name'
        ]
        read_only_fields = ['id', 'user']
    
    def get_user_details(self, obj):
        return {
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating students with user data"""
    user = UserSerializer()
    
    class Meta:
        model = Student
        fields = [
            'user', 'student_id', 'date_of_birth', 'grade',
            'address', 'parent_name', 'parent_contact'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class AcademicRecordSerializer(serializers.ModelSerializer):
    """Serializer for Academic Record model"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    
    class Meta:
        model = AcademicRecord
        fields = [
            'id', 'student', 'subject', 'grade', 'semester', 'year',
            'student_name', 'student_id'
        ]
        read_only_fields = ['id']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for student with academic records"""
    user = UserSerializer(read_only=True)
    academic_records = AcademicRecordSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'date_of_birth', 'grade',
            'address', 'parent_name', 'parent_contact', 'full_name',
            'academic_records'
        ]
        read_only_fields = ['id', 'user']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()