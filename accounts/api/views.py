from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count
from accounts.models import CustomUser, UserProfile
from accounts.permissions import (
    IsOwnerOrAdmin, IsAdminUser as CustomIsAdminUser, 
    CanModifyOwnProfile, IsStaffOrAdmin
)
from .serializers import (
    UserListSerializer, UserDetailSerializer, UserCreateSerializer, 
    UserUpdateSerializer, ChangePasswordSerializer, UserProfileSerializer,
    LoginSerializer, RegisterSerializer, DashboardDataSerializer, 
    UserStatsSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    Provides CRUD operations for user management with role-based permissions
    """
    queryset = CustomUser.objects.all().select_related('userprofile')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_staff', 'userprofile__user_type']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login', 'username', 'email']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions required for this view.
        """
        if self.action == 'create':
            # Only admins can create users via API
            permission_classes = [CustomIsAdminUser]
        elif self.action in ['update', 'partial_update']:
            # Users can update their own profile, admins can update any
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'destroy':
            # Only admins can delete users
            permission_classes = [CustomIsAdminUser]
        elif self.action == 'list':
            # Only admins can list all users
            permission_classes = [CustomIsAdminUser]
        else:
            # For retrieve and other actions, users can view their own profile
            permission_classes = [IsOwnerOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        """
        queryset = super().get_queryset()
          # If user is admin, return all users
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        
        # Regular users can only see their own profile
        return queryset.filter(id=self.request.user.id)
    
    def perform_create(self, serializer):
        """Create user with automatic profile creation"""
        user = serializer.save()
        return user
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Change user password - only own password or admin"""
        user = self.get_object()
        
        # Check if user can change this password
        if not (request.user.is_staff or request.user.is_superuser or request.user == user):
            return Response(
                {'error': 'You can only change your own password'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[CustomIsAdminUser])
    def activate(self, request, pk=None):
        """Activate user account - admin only"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': 'User activated successfully'})
    
    @action(detail=True, methods=['post'], permission_classes=[CustomIsAdminUser])
    def deactivate(self, request, pk=None):
        """Deactivate user account - admin only"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated successfully'})
        
        user = self.get_object()
        if user == request.user:
            return Response(
                {'error': 'You cannot deactivate your own account'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated successfully'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff can view user statistics'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Calculate user statistics
        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        
        # Count by user types
        user_type_counts = UserProfile.objects.values('user_type').annotate(
            count=Count('user_type')
        )
        
        stats = {
            'total_users': total_users,
            'active_users': active_users,
            'students_count': next((item['count'] for item in user_type_counts if item['user_type'] == 'student'), 0),
            'teachers_count': next((item['count'] for item in user_type_counts if item['user_type'] == 'teacher'), 0),
            'staff_count': next((item['count'] for item in user_type_counts if item['user_type'] == 'staff'), 0),
            'admins_count': next((item['count'] for item in user_type_counts if item['user_type'] == 'admin'), 0),
            'recent_registrations': CustomUser.objects.filter(
                date_joined__gte=timezone.now() - timedelta(days=30)
            ).count(),
        }
        
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_users(self, request):
        """Get recently registered users"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff can view recent users'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        recent_users = CustomUser.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=7)
        ).order_by('-date_joined')[:10]
        
        serializer = UserListSerializer(recent_users, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profiles with role-based permissions
    """
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_type']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions required for this view.
        """
        if self.action in ['update', 'partial_update']:
            # Users can update their own profile, admins can update any
            permission_classes = [CanModifyOwnProfile]
        elif self.action in ['create', 'destroy']:
            # Only admins can create/delete profiles
            permission_classes = [CustomIsAdminUser]
        elif self.action == 'list':
            # Only admins can list all profiles
            permission_classes = [CustomIsAdminUser]
        else:
            # For retrieve, users can view their own profile
            permission_classes = [IsOwnerOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        """
        queryset = super().get_queryset()
        
        # If user is admin, return all profiles
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        
        # Regular users can only see their own profile
        return queryset.filter(user=self.request.user)


# Authentication API Views (function-based for specific auth operations)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """API endpoint for user login"""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user) # This handles session login
        
        # Generate JWT tokens for API authentication
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        user_data = UserDetailSerializer(user).data
        
        return Response({
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """API endpoint for user registration"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # No automatic session login here, as we want to rely on JWT for the auto-login via frontend
        # login(request, user) 
        
        # User is created, frontend will call login_view to get tokens
        user_data = UserDetailSerializer(user).data
        
        return Response({
            'user': user_data,
            'message': 'Registration successful. Please login.' # Modified message
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """API endpoint for user logout"""
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token_view(request):
    """API endpoint to get CSRF token"""
    return Response({'csrfToken': get_token(request)}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """API endpoint to get current authenticated user"""
    user_data = UserDetailSerializer(request.user).data
    return Response({'user': user_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request):
    """API endpoint to get current user profile"""
    if request.user.is_authenticated:
        user_data = UserDetailSerializer(request.user).data
        return Response({'user': user_data}, status=status.HTTP_200_OK)
    else:
        return Response({'user': None, 'authenticated': False}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """API endpoint to get dashboard data"""
    user = request.user
    
    # Basic stats based on user type
    stats = {}
    recent_activities = []
    
    try:
        user_profile = user.userprofile
        user_type = user_profile.user_type
        
        if user_type == 'student':
            from students.models import Student, AcademicRecord
            from courses.models import CourseEnrollment
            from attendance.models import Attendance
            
            student = Student.objects.filter(user=user).first()
            if student:
                enrollments_count = CourseEnrollment.objects.filter(student=student).count()
                attendance_records = Attendance.objects.filter(student=student)
                present_count = attendance_records.filter(status='present').count()
                total_attendance = attendance_records.count()
                attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
                
                stats = {
                    'enrolled_courses': enrollments_count,
                    'attendance_rate': f"{attendance_rate:.1f}%",
                    'academic_records': student.academicrecord_set.count(),
                    'recent_attendance': present_count,
                }
                recent_activities = [
                    'Attended Mathematics lecture',
                    'Submitted Physics assignment',
                    'Received grade for Chemistry quiz',
                    'Enrolled in new course'
                ]
        
        elif user_type == 'teacher':
            from teachers.models import Teacher, Lesson
            from courses.models import Course
            
            teacher = Teacher.objects.filter(user=user).first()
            if teacher:
                courses_taught = Course.objects.filter(teacher=teacher).count()
                lessons_count = Lesson.objects.filter(teacher=teacher).count()
                
                stats = {
                    'courses_taught': courses_taught,
                    'total_lessons': lessons_count,
                    'subjects_taught': teacher.subjects.count(),
                    'classes_assigned': teacher.classes.count(),
                }
                recent_activities = [
                    'Created new lesson plan for Mathematics',
                    'Graded Physics assignments',
                    'Updated class schedule',
                    'Conducted virtual lesson'
                ]
        
        elif user_type == 'staff':
            from staff.models import LeaveRequest, PerformanceEvaluation
            
            staff = user.staffprofile if hasattr(user, 'staffprofile') else None
            if staff:
                leave_requests = LeaveRequest.objects.filter(staff=staff)
                pending_leaves = leave_requests.filter(status='pending').count()
                evaluations = PerformanceEvaluation.objects.filter(staff=staff).count()
                
                stats = {
                    'pending_leave_requests': pending_leaves,
                    'total_leave_requests': leave_requests.count(),
                    'performance_evaluations': evaluations,
                    'department': staff.department.name if staff.department else 'Not assigned',
                }
                recent_activities = [
                    'Processed student enrollment requests',
                    'Updated staff records',
                    'Completed monthly reports',
                    'Attended departmental meeting'
                ]
        
        elif user_type == 'admin':
            stats = {
                'total_students': CustomUser.objects.filter(userprofile__user_type='student').count(),
                'total_teachers': CustomUser.objects.filter(userprofile__user_type='teacher').count(),
                'total_staff': CustomUser.objects.filter(userprofile__user_type='staff').count(),
                'recent_registrations': CustomUser.objects.filter(
                    date_joined__gte=timezone.now() - timedelta(days=7)
                ).count(),
            }
            recent_activities = [
                'System backup completed successfully',
                'New user registrations approved',
                'Monthly system reports generated',
                'Database maintenance completed'
            ]
    
    except Exception as e:
        # Handle missing profile gracefully
        stats = {'error': 'Profile data not available'}
        recent_activities = ['Complete profile setup required']
    
    response_data = {
        'user': UserDetailSerializer(user).data,
        'stats': stats,
        'recent_activities': recent_activities
    }
    
    return Response(response_data, status=status.HTTP_200_OK)