from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from accounts.permissions import (
    IsOwnerOrAdmin, IsAdminUser, IsStaffOrAdmin, 
    TeacherCanViewOwnStudents, ReadOnlyForStudents
)
from ..models import Student, AcademicRecord
from .serializers import (
    StudentSerializer, StudentCreateSerializer, StudentDetailSerializer,
    AcademicRecordSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing students with role-based permissions
    - Admins: Full access to all students
    - Staff: Full access to all students  
    - Teachers: Read access to students in their classes
    - Students: Read access to their own profile only
    """
    queryset = Student.objects.select_related('user').prefetch_related('academic_records')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grade', 'student_id']
    search_fields = ['user__first_name', 'user__last_name', 'student_id', 'parent_name']
    ordering_fields = ['user__first_name', 'user__last_name', 'student_id', 'grade']
    ordering = ['user__first_name']
    
    def get_permissions(self):
        """
        Role-based permissions for student management
        """
        if self.action in ['create', 'destroy']:
            # Only admins and staff can create/delete students
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Students can update their own profile, staff/admins can update any
            permission_classes = [IsOwnerOrAdmin]
        else:
            # For list/retrieve, apply teacher restrictions
            permission_classes = [TeacherCanViewOwnStudents]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Admin users can see all students
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Students can only see their own profile
            if user_profile.user_type == 'student':
                return queryset.filter(user=user)
            
            # Staff can see all students
            elif user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see students in their classes/courses
            elif user_profile.user_type == 'teacher':
                try:
                    teacher = user.teacher
                    # Get students enrolled in teacher's courses
                    return queryset.filter(
                        courseenrollment__course__instructor=teacher
                    ).distinct()
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer
    
    @action(detail=True, methods=['get'])
    def academic_records(self, request, pk=None):
        """Get all academic records for a specific student"""
        student = self.get_object()
        records = student.academic_records.all()
        serializer = AcademicRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for students"""
        query = request.query_params.get('q', '')
        grade = request.query_params.get('grade', '')
        
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(student_id__icontains=query) |
                Q(parent_name__icontains=query)
            )
        
        if grade:
            queryset = queryset.filter(grade=grade)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_grade(self, request):
        """Get students grouped by grade"""
        grade = request.query_params.get('grade', '')
        if not grade:
            return Response({'error': 'Grade parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        students = self.get_queryset().filter(grade=grade)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)


class AcademicRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing academic records
    """
    queryset = AcademicRecord.objects.select_related('student__user')
    serializer_class = AcademicRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'subject', 'grade', 'semester', 'year']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'subject']
    ordering_fields = ['year', 'semester', 'subject', 'grade']
    ordering = ['-year', 'semester']
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get academic records for a specific student"""
        student_id = request.query_params.get('student_id', '')
        if not student_id:
            return Response({'error': 'Student ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        records = self.get_queryset().filter(student_id=student_id)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """Get academic records for a specific subject"""
        subject = request.query_params.get('subject', '')
        if not subject:
            return Response({'error': 'Subject parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        records = self.get_queryset().filter(subject__icontains=subject)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get academic statistics"""
        total_records = self.get_queryset().count()
        subjects = self.get_queryset().values_list('subject', flat=True).distinct().count()
        
        return Response({
            'total_records': total_records,
            'total_subjects': subjects,
            'latest_records': AcademicRecordSerializer(
                self.get_queryset().order_by('-year', '-semester')[:5], many=True
            ).data
        })