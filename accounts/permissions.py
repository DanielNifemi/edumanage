"""
Custom permission classes for role-based access control in EduManage system.
Defines specific permissions for Students, Teachers, Staff, and Admins.
"""

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class IsOwnerOrAdmin(BasePermission):
    """
    Permission that allows access only to object owners or admin users.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can access everything
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Check if the object has a 'user' field and if it matches the requesting user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if the object itself is the user
        if hasattr(obj, 'username'):  # User model
            return obj == request.user
            
        return False


class IsAdminUser(BasePermission):
    """
    Permission that allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)


class IsStudentUser(BasePermission):
    """
    Permission that allows access only to users with student role.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        try:
            user_profile = request.user.userprofile
            return user_profile.user_type == 'student'
        except:
            return False


class IsTeacherUser(BasePermission):
    """
    Permission that allows access only to users with teacher role.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        try:
            user_profile = request.user.userprofile
            return user_profile.user_type == 'teacher'
        except:
            return False


class IsStaffUser(BasePermission):
    """
    Permission that allows access only to users with staff role.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        try:
            user_profile = request.user.userprofile
            return user_profile.user_type == 'staff'
        except:
            return False


class IsTeacherOrAdmin(BasePermission):
    """
    Permission that allows access to teachers and admin users.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin users always have access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            return user_profile.user_type == 'teacher'
        except:
            return False


class IsStaffOrAdmin(BasePermission):
    """
    Permission that allows access to staff and admin users.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin users always have access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            return user_profile.user_type == 'staff'
        except:
            return False


class IsStudentOrTeacherOrAdmin(BasePermission):
    """
    Permission that allows access to students, teachers, and admin users.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin users always have access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            return user_profile.user_type in ['student', 'teacher']
        except:
            return False


class ReadOnlyForStudents(BasePermission):
    """
    Permission that allows read-only access for students, full access for others.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin users always have full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            # Students can only read
            if user_profile.user_type == 'student':
                return request.method in permissions.SAFE_METHODS
            # Teachers and staff have full access
            return user_profile.user_type in ['teacher', 'staff']
        except:
            return False


class CanModifyOwnProfile(BasePermission):
    """
    Permission that allows users to modify their own profile only.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can modify any profile
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Users can only modify their own profile
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class TeacherCanViewOwnStudents(BasePermission):
    """
    Permission that allows teachers to view only their own students.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin users can view all students
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            return user_profile.user_type in ['teacher', 'staff']
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        # Admin users can view any student
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Teachers can view students in their classes
        try:
            user_profile = request.user.userprofile
            if user_profile.user_type == 'teacher':
                teacher = request.user.teacher
                # Check if student is enrolled in any of teacher's courses
                return obj.courseenrollment_set.filter(
                    course__instructor=teacher
                ).exists()
        except:
            pass
        
        return False


class CanAccessAttendance(BasePermission):
    """
    Permission for accessing attendance records.
    Students can view own attendance, Teachers can manage attendance for their classes.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin and staff have full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            
            # Students can view their own attendance
            if user_profile.user_type == 'student' and request.method in permissions.SAFE_METHODS:
                return True
            
            # Teachers can manage attendance for their classes
            if user_profile.user_type == 'teacher':
                return True
                
            # Staff can manage all attendance
            if user_profile.user_type == 'staff':
                return True
                
        except:
            pass
        
        return False


class CanAccessExaminations(BasePermission):
    """
    Permission for accessing examinations.
    Students can view own results, Teachers can manage their exams.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin and staff have full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            
            # Students can view exams and their results
            if user_profile.user_type == 'student' and request.method in permissions.SAFE_METHODS:
                return True
            
            # Teachers can create and manage exams
            if user_profile.user_type == 'teacher':
                return True
                
            # Staff can manage all exams
            if user_profile.user_type == 'staff':
                return True
                
        except:
            pass
        
        return False


class CanAccessSchedules(BasePermission):
    """
    Permission for accessing schedules.
    Students and Teachers can view, Staff and Admin can manage.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin and staff have full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            
            # Students can view schedules
            if user_profile.user_type == 'student' and request.method in permissions.SAFE_METHODS:
                return True
            
            # Teachers can view and manage schedules for their classes
            if user_profile.user_type == 'teacher':
                return True
                
            # Staff can manage all schedules
            if user_profile.user_type == 'staff':
                return True
                
        except:
            pass
        
        return False


class CanAccessDiscipline(BasePermission):
    """
    Permission for accessing discipline records.
    Students can view own records, Teachers and Staff can manage.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Admin and staff have full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            
            # Students can view their own records only
            if user_profile.user_type == 'student' and request.method in permissions.SAFE_METHODS:
                return True
            
            # Teachers can create and view discipline records
            if user_profile.user_type == 'teacher':
                return True
                
            # Staff can manage all discipline records
            if user_profile.user_type == 'staff':
                return True
                
        except:
            pass
        
        return False


class CanAccessCommunication(BasePermission):
    """
    Permission for accessing communication (messages, notifications).
    All authenticated users can access communication features.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # All authenticated users can access communication
        return True


class CanManageStaff(BasePermission):
    """
    Permission for staff management operations.
    """
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        
        # Only admin users can manage staff
        return request.user.is_staff or request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        # Admin users can manage all staff
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Staff can view their own profile
        if hasattr(obj, 'user') and request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        
        return False


# Role-based permission mapping for easy access
ROLE_PERMISSIONS = {
    'student': {
        'read_only': [
            'attendance', 'examinations', 'courses', 'schedules', 
            'communication', 'students'  # Can view own profile
        ],
        'no_access': [
            'staff', 'discipline', 'teachers'  # Cannot access these modules
        ],
        'own_data_only': [
            'students', 'communication'  # Can only access own data
        ]
    },
    'teacher': {
        'full_access': [
            'attendance', 'examinations', 'courses', 'schedules',
            'communication', 'discipline', 'teachers'
        ],
        'read_only': [
            'staff'  # Can view staff but not modify
        ],
        'limited_access': [
            'students'  # Can view students in their classes only
        ]
    },
    'staff': {
        'full_access': [
            'attendance', 'examinations', 'courses', 'schedules',
            'communication', 'discipline', 'staff', 'students'
        ],
        'read_only': [
            'teachers'  # Can view teachers but not modify
        ]
    },
    'admin': {
        'full_access': [
            'attendance', 'examinations', 'courses', 'schedules',
            'communication', 'discipline', 'staff', 'students', 
            'teachers', 'accounts'
        ]
    }
}
