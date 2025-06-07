from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import StaffProfile, Department, Role, LeaveRequest, PerformanceEvaluation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details in staff context"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    staff_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'staff_count']
        read_only_fields = ['id']
    
    def get_staff_count(self, obj):
        return obj.staffprofile_set.count()


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model"""
    staff_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'staff_count']
        read_only_fields = ['id']
    
    def get_staff_count(self, obj):
        return obj.staffprofile_set.count()


class StaffProfileSerializer(serializers.ModelSerializer):
    """Serializer for StaffProfile model"""
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StaffProfile
        fields = [
            'id', 'user', 'staff_id', 'department', 'role', 'position',
            'employee_id', 'date_of_birth', 'date_joined', 'phone_number',
            'address', 'created_at', 'updated_at', 'department_name',
            'role_name', 'full_name'
        ]
        read_only_fields = ['id', 'staff_id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()


class StaffProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating staff profiles with user data"""
    user = UserSerializer()
    
    class Meta:
        model = StaffProfile
        fields = [
            'user', 'department', 'role', 'position', 'employee_id',
            'date_of_birth', 'date_joined', 'phone_number', 'address'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        staff_profile = StaffProfile.objects.create(user=user, **validated_data)
        return staff_profile


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Serializer for LeaveRequest model"""
    staff_name = serializers.CharField(source='staff.user.get_full_name', read_only=True)
    staff_id = serializers.CharField(source='staff.staff_id', read_only=True)
    duration_days = serializers.SerializerMethodField()
    
    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'staff', 'leave_type', 'start_date', 'end_date',
            'reason', 'status', 'staff_name', 'staff_id', 'duration_days'
        ]
        read_only_fields = ['id']
    
    def get_duration_days(self, obj):
        """Calculate leave duration in days"""
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days + 1
        return None


class PerformanceEvaluationSerializer(serializers.ModelSerializer):
    """Serializer for PerformanceEvaluation model"""
    staff_name = serializers.CharField(source='staff.user.get_full_name', read_only=True)
    staff_id = serializers.CharField(source='staff.staff_id', read_only=True)
    evaluator_name = serializers.CharField(source='evaluator.get_full_name', read_only=True)
    rating_display = serializers.SerializerMethodField()
    
    class Meta:
        model = PerformanceEvaluation
        fields = [
            'id', 'staff', 'evaluator', 'date', 'rating', 'comments',
            'staff_name', 'staff_id', 'evaluator_name', 'rating_display'
        ]
        read_only_fields = ['id']
    
    def get_rating_display(self, obj):
        """Get rating with description"""
        rating_descriptions = {
            1: "Poor",
            2: "Below Average", 
            3: "Average",
            4: "Good",
            5: "Excellent"
        }
        return f"{obj.rating}/5 - {rating_descriptions.get(obj.rating, 'Unknown')}"


class StaffProfileDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for staff profile with related data"""
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    recent_leave_requests = serializers.SerializerMethodField()
    recent_evaluations = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StaffProfile
        fields = [
            'id', 'user', 'staff_id', 'department', 'role', 'position',
            'employee_id', 'date_of_birth', 'date_joined', 'phone_number',
            'address', 'created_at', 'updated_at', 'full_name',
            'recent_leave_requests', 'recent_evaluations'
        ]
        read_only_fields = ['id', 'staff_id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_recent_leave_requests(self, obj):
        recent_requests = obj.leaverequest_set.order_by('-start_date')[:5]
        return LeaveRequestSerializer(recent_requests, many=True).data
    
    def get_recent_evaluations(self, obj):
        recent_evaluations = obj.performanceevaluation_set.order_by('-date')[:3]
        return PerformanceEvaluationSerializer(recent_evaluations, many=True).data
