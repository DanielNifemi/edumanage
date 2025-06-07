from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, UserProfile
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (minimal fields)"""
    role = serializers.CharField(source='userprofile.user_type', read_only=True)
    profile_created = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'is_active', 'date_joined', 'profile_created']
    
    def get_profile_created(self, obj):
        return hasattr(obj, 'userprofile')


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with profile information"""
    role = serializers.CharField(source='userprofile.user_type', read_only=True)
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role',
                 'phone_number', 'is_phone_verified', 'is_active', 'is_staff',
                 'date_joined', 'last_login', 'profile_data']
    
    def get_profile_data(self, obj):
        if hasattr(obj, 'userprofile'):
            profile = obj.userprofile
            data = {
                'user_type': profile.user_type,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at
            }
            
            # Add specific profile data based on user type
            if profile.user_type == 'student' and hasattr(obj, 'student'):
                data['student_id'] = obj.student.student_id
                # Use the user's date_joined as the admission_date for a student
                data['admission_date'] = obj.date_joined # Corrected: obj is the CustomUser instance
            elif profile.user_type == 'teacher' and hasattr(obj, 'teacher'):
                data['teacher_id'] = obj.teacher.teacher_id
                data['join_date'] = obj.teacher.date_joined
                data['subjects_count'] = obj.teacher.subjects.count()
            elif profile.user_type == 'staff' and hasattr(obj, 'staffprofile'):
                data['staff_id'] = obj.staffprofile.staff_id
                data['join_date'] = obj.staffprofile.date_joined
                data['department'] = obj.staffprofile.department.name if obj.staffprofile.department else None
            
            return data
        return None


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'phone_number', 'user_type']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Validate password strength
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user_type = validated_data.pop('user_type')
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        
        # Create UserProfile and specific profile
        profile = UserProfile.objects.create(user=user, user_type=user_type)
        profile.create_specific_profile()
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email']
        
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        
        # Validate password strength
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile management"""
    user = UserDetailSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'user_type', 'created_at', 'updated_at']


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
            
            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPES)
    
    # Role-specific fields (optional)
    student_id = serializers.CharField(required=False, allow_blank=True)
    employee_id = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    admin_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'user_type', 'student_id', 
                 'employee_id', 'department', 'admin_code']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Validate password strength
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        
        # Validate admin code if provided
        user_type = attrs.get('user_type')
        admin_code = attrs.get('admin_code')
        
        if user_type == 'admin' and admin_code:
            # You can add admin code validation logic here
            # For now, we'll accept any non-empty admin code
            if not admin_code.strip():
                raise serializers.ValidationError({'admin_code': 'Admin code is required for admin registration'})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user_type = validated_data.pop('user_type')
        
        # Extract role-specific fields
        student_id = validated_data.pop('student_id', '')
        employee_id = validated_data.pop('employee_id', '')
        department = validated_data.pop('department', '')
        admin_code = validated_data.pop('admin_code', '')
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Set admin privileges if admin user type
        if user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        
        # Create UserProfile
        profile = UserProfile.objects.create(user=user, user_type=user_type)        # Create specific profile with role-specific data
        if user_type == 'student':
            Student.objects.create(
                user=user,
                student_id=student_id or f"STU{user.id:06d}",
                grade='Not set',
                address='Not set',
                parent_name='Not set',
                parent_contact='Not set'
            )
        elif user_type == 'teacher':
            Teacher.objects.create(
                user=user,
                teacher_id=employee_id or f"TCH{user.id:06d}",
                qualification='Not set',
                years_of_experience=0,
                department=department or 'General'
            )
        elif user_type == 'staff':
            # Generate unique employee_id
            staff_employee_id = employee_id or f"EMP{user.id:06d}"
            StaffProfile.objects.create(
                user=user,
                staff_id=f"STF{user.id:06d}",
                position='Staff Member',
                employee_id=staff_employee_id,
                department=None  # Set to None since it's a ForeignKey
            )
        
        return user


class DashboardDataSerializer(serializers.Serializer):
    """Serializer for dashboard data"""
    user = UserDetailSerializer()
    stats = serializers.DictField()
    recent_activities = serializers.ListField()


class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics"""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    students_count = serializers.IntegerField()
    teachers_count = serializers.IntegerField()
    staff_count = serializers.IntegerField()
    admins_count = serializers.IntegerField()
    recent_registrations = serializers.IntegerField()