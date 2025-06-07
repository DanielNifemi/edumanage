from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, CanManageStaff, 
    IsTeacherOrAdmin, ReadOnlyForStudents
)
from ..models import StaffProfile, Department, Role, LeaveRequest, PerformanceEvaluation
from .serializers import (
    StaffProfileSerializer, StaffProfileCreateSerializer, StaffProfileDetailSerializer,
    DepartmentSerializer, RoleSerializer, LeaveRequestSerializer, PerformanceEvaluationSerializer
)


class StaffProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing staff profiles with role-based permissions
    - Admins: Full access to all staff profiles
    - Staff: Can view all staff, update own profile only
    - Teachers: Read-only access to staff profiles
    - Students: No access to staff profiles
    """
    queryset = StaffProfile.objects.select_related('user', 'department', 'role')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'role', 'position']
    search_fields = ['user__first_name', 'user__last_name', 'staff_id', 'employee_id']
    ordering_fields = ['user__first_name', 'user__last_name', 'staff_id', 'date_joined']
    ordering = ['user__first_name']
    
    def get_permissions(self):
        """
        Role-based permissions for staff management
        """
        # Use the CanManageStaff permission which restricts access appropriately
        permission_classes = [CanManageStaff]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Admin users can see all staff
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all staff profiles
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can view staff profiles (read-only)
            elif user_profile.user_type == 'teacher':
                return queryset
            
            # Students have no access
            elif user_profile.user_type == 'student':
                return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StaffProfileCreateSerializer
        elif self.action == 'retrieve':
            return StaffProfileDetailSerializer
        return StaffProfileSerializer
    
    @action(detail=True, methods=['get'])
    def leave_requests(self, request, pk=None):
        """Get all leave requests for a specific staff member"""
        staff = self.get_object()
        requests = staff.leaverequest_set.all().order_by('-start_date')
        serializer = LeaveRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def evaluations(self, request, pk=None):
        """Get all performance evaluations for a specific staff member"""
        staff = self.get_object()
        evaluations = staff.performanceevaluation_set.all().order_by('-date')
        serializer = PerformanceEvaluationSerializer(evaluations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """Get staff by department"""
        department = request.query_params.get('department', '')
        if not department:
            return Response({'error': 'Department parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        staff = self.get_queryset().filter(department__name__icontains=department)
        serializer = self.get_serializer(staff, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get staff statistics"""
        total_staff = self.get_queryset().count()
        departments = self.get_queryset().values_list('department__name', flat=True).distinct().count()
        roles = self.get_queryset().values_list('role__name', flat=True).distinct().count()
        
        return Response({
            'total_staff': total_staff,
            'total_departments': departments,
            'total_roles': roles,
            'recent_staff': StaffProfileSerializer(
                self.get_queryset().order_by('-created_at')[:5], many=True
            ).data
        })


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing departments with role-based permissions
    - Admins: Full access to departments
    - Staff: Full access to departments
    - Teachers: Read-only access to departments
    - Students: No access to departments
    """
    queryset = Department.objects.prefetch_related('staffprofile_set')
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Role-based permissions for department management
        """
        if self.action in ['create', 'destroy']:
            # Only admins can create/delete departments
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Staff and admins can update departments
            permission_classes = [IsStaffOrAdmin]
        else:
            # Teachers have read-only access, students no access
            permission_classes = [IsTeacherOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def staff(self, request, pk=None):
        """Get all staff in a specific department"""
        department = self.get_object()
        staff = department.staffprofile_set.all()
        serializer = StaffProfileSerializer(staff, many=True)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing roles with role-based permissions
    - Admins: Full access to roles
    - Staff: Full access to roles
    - Teachers: Read-only access to roles
    - Students: No access to roles
    """
    queryset = Role.objects.prefetch_related('staffprofile_set')
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Role-based permissions for role management
        """
        if self.action in ['create', 'destroy']:
            # Only admins can create/delete roles
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Staff and admins can update roles
            permission_classes = [IsStaffOrAdmin]
        else:
            # Teachers have read-only access, students no access
            permission_classes = [IsTeacherOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def staff(self, request, pk=None):
        """Get all staff with a specific role"""
        role = self.get_object()
        staff = role.staffprofile_set.all()
        serializer = StaffProfileSerializer(staff, many=True)
        return Response(serializer.data)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing leave requests with role-based permissions
    - Admins: Full access to all leave requests
    - Staff: Can view all, create own, approve/reject others
    - Teachers: Read-only access to leave requests
    - Students: No access to leave requests
    """
    queryset = LeaveRequest.objects.select_related('staff__user')
    serializer_class = LeaveRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['staff', 'leave_type', 'status']
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'reason']
    ordering_fields = ['start_date', 'end_date', 'status']
    ordering = ['-start_date']
    
    def get_permissions(self):
        """
        Role-based permissions for leave request management
        """
        if self.action in ['create']:
            # Staff can create their own leave requests
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Staff can update their own requests, admins can update any
            permission_classes = [IsOwnerOrAdmin]
        elif self.action in ['approve', 'reject']:
            # Only admins and senior staff can approve/reject
            permission_classes = [IsStaffOrAdmin]
        else:
            # Teachers have read-only access, students no access
            permission_classes = [IsTeacherOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Admin users can see all leave requests
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all leave requests
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can view leave requests (read-only)
            elif user_profile.user_type == 'teacher':
                return queryset
            
            # Students have no access
            elif user_profile.user_type == 'student':
                return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending leave requests"""
        pending_requests = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def approved(self, request):
        """Get all approved leave requests"""
        approved_requests = self.get_queryset().filter(status='approved')
        serializer = self.get_serializer(approved_requests, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a leave request"""
        leave_request = self.get_object()
        leave_request.status = 'approved'
        leave_request.save()
        return Response({'status': 'Leave request approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a leave request"""
        leave_request = self.get_object()
        leave_request.status = 'rejected'
        leave_request.save()
        return Response({'status': 'Leave request rejected'})
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get leave request statistics"""
        total_requests = self.get_queryset().count()
        pending_count = self.get_queryset().filter(status='pending').count()
        approved_count = self.get_queryset().filter(status='approved').count()
        rejected_count = self.get_queryset().filter(status='rejected').count()
        
        return Response({
            'total_requests': total_requests,
            'pending': pending_count,
            'approved': approved_count,
            'rejected': rejected_count
        })


class PerformanceEvaluationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing performance evaluations with role-based permissions
    - Admins: Full access to all evaluations
    - Staff: Can view all, create evaluations for others
    - Teachers: Read-only access to evaluations
    - Students: No access to evaluations
    """
    queryset = PerformanceEvaluation.objects.select_related('staff__user', 'evaluator')
    serializer_class = PerformanceEvaluationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['staff', 'evaluator', 'rating']
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'comments']
    ordering_fields = ['date', 'rating']
    ordering = ['-date']
    
    def get_permissions(self):
        """
        Role-based permissions for performance evaluation management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admins and staff can manage evaluations
            permission_classes = [IsStaffOrAdmin]
        else:
            # Teachers have read-only access, students no access
            permission_classes = [IsTeacherOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Admin users can see all evaluations
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all evaluations
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can view evaluations (read-only)
            elif user_profile.user_type == 'teacher':
                return queryset
            
            # Students have no access
            elif user_profile.user_type == 'student':
                return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    @action(detail=False, methods=['get'])
    def by_rating(self, request):
        """Get evaluations by rating"""
        rating = request.query_params.get('rating', '')
        if not rating:
            return Response({'error': 'Rating parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        evaluations = self.get_queryset().filter(rating=rating)
        serializer = self.get_serializer(evaluations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get performance evaluation statistics"""
        total_evaluations = self.get_queryset().count()
        avg_rating = self.get_queryset().aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        rating_distribution = {}
        for rating in range(1, 6):
            count = self.get_queryset().filter(rating=rating).count()
            rating_distribution[f'rating_{rating}'] = count
        
        return Response({
            'total_evaluations': total_evaluations,
            'average_rating': round(avg_rating, 2),
            'rating_distribution': rating_distribution
        })
