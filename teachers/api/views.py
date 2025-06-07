from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, IsTeacherOrAdmin, 
    IsTeacherUser, ReadOnlyForStudents
)
from ..models import Teacher, Subject, Class, Lesson
from .serializers import (
    TeacherSerializer, TeacherCreateSerializer, TeacherDetailSerializer,
    SubjectSerializer, ClassSerializer, LessonSerializer
)


class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teachers with role-based permissions
    - Admins/Staff: Full access to all teachers
    - Teachers: Can view all teachers, update own profile only
    - Students: Read-only access to teachers
    """
    queryset = Teacher.objects.select_related('user').prefetch_related('subjects', 'classes')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'teacher_id']
    search_fields = ['user__first_name', 'user__last_name', 'teacher_id', 'department']
    ordering_fields = ['user__first_name', 'user__last_name', 'teacher_id', 'department', 'years_of_experience']
    ordering = ['user__first_name']
    
    def get_permissions(self):
        """
        Role-based permissions for teacher management
        """
        if self.action in ['create', 'destroy']:
            # Only admins and staff can create/delete teachers
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Teachers can update their own profile, staff/admins can update any
            permission_classes = [IsOwnerOrAdmin]
        else:
            # For list/retrieve, students have read-only access
            permission_classes = [ReadOnlyForStudents]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Admin users and staff can see all teachers
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all teachers
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers and students can see all teachers (read-only for students)
            elif user_profile.user_type in ['teacher', 'student']:
                return queryset
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        elif self.action == 'retrieve':
            return TeacherDetailSerializer
        return TeacherSerializer
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Get all lessons for a specific teacher"""
        teacher = self.get_object()
        lessons = teacher.lesson_set.all().order_by('-date', '-start_time')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        """Get all subjects taught by a specific teacher"""
        teacher = self.get_object()
        subjects = teacher.subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """Get teachers by department"""
        department = request.query_params.get('department', '')
        if not department:
            return Response({'error': 'Department parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        teachers = self.get_queryset().filter(department__icontains=department)
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get teacher statistics"""
        total_teachers = self.get_queryset().count()
        departments = self.get_queryset().values_list('department', flat=True).distinct().count()
        avg_experience = self.get_queryset().aggregate(avg_exp=Avg('years_of_experience'))['avg_exp'] or 0
        
        return Response({
            'total_teachers': total_teachers,
            'total_departments': departments,
            'average_experience': round(avg_experience, 1),
            'recent_teachers': TeacherSerializer(
                self.get_queryset().order_by('-created_at')[:5], many=True
            ).data
        })


class SubjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing subjects with role-based permissions
    - Admins/Staff: Full access to all subjects
    - Teachers: Full access to subjects
    - Students: Read-only access to subjects
    """
    queryset = Subject.objects.prefetch_related('teachers')
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Role-based permissions for subject management
        """
        if self.action in ['create', 'destroy']:
            # Only admins and staff can create/delete subjects
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Teachers and staff can update subjects
            permission_classes = [IsTeacherOrAdmin]
        else:
            # Students have read-only access
            permission_classes = [ReadOnlyForStudents]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def teachers(self, request, pk=None):
        """Get all teachers for a specific subject"""
        subject = self.get_object()
        teachers = subject.teachers.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get subject statistics"""
        total_subjects = self.get_queryset().count()
        subjects_with_teachers = self.get_queryset().annotate(
            teacher_count=Count('teachers')
        ).filter(teacher_count__gt=0).count()
        
        return Response({
            'total_subjects': total_subjects,
            'subjects_with_teachers': subjects_with_teachers,
            'subjects_without_teachers': total_subjects - subjects_with_teachers
        })


class ClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing classes with role-based permissions
    - Admins/Staff: Full access to all classes
    - Teachers: Full access to their own classes, read access to others
    - Students: Read-only access to classes
    """
    queryset = Class.objects.select_related('teacher__user')
    serializer_class = ClassSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['teacher']
    search_fields = ['name', 'teacher__user__first_name', 'teacher__user__last_name']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Role-based permissions for class management
        """
        if self.action in ['create', 'destroy']:
            # Only admins and staff can create/delete classes
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Teachers can update their own classes, staff/admins can update any
            permission_classes = [IsOwnerOrAdmin]
        else:
            # Students have read-only access
            permission_classes = [ReadOnlyForStudents]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Admin users and staff can see all classes
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all classes
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers and students can see all classes
            elif user_profile.user_type in ['teacher', 'student']:
                return queryset
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Get all lessons for a specific class"""
        class_obj = self.get_object()
        lessons = class_obj.lesson_set.all().order_by('-date', '-start_time')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing lessons with role-based permissions
    - Admins/Staff: Full access to all lessons
    - Teachers: Full access to their own lessons, read access to others
    - Students: Read-only access to lessons
    """
    queryset = Lesson.objects.select_related('teacher__user', 'subject', 'class_group')
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['teacher', 'subject', 'class_group', 'date']
    search_fields = ['topic', 'teacher__user__first_name', 'teacher__user__last_name', 'subject__name']
    ordering_fields = ['date', 'start_time', 'topic']
    ordering = ['-date', 'start_time']
    
    def get_permissions(self):
        """
        Role-based permissions for lesson management
        """
        if self.action in ['create', 'destroy']:
            # Teachers and staff/admins can create/delete lessons
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Teachers can update their own lessons, staff/admins can update any
            permission_classes = [IsOwnerOrAdmin]
        else:
            # Students have read-only access
            permission_classes = [ReadOnlyForStudents]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Admin users and staff can see all lessons
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all lessons
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see all lessons (but can only modify their own)
            elif user_profile.user_type == 'teacher':
                return queryset
            
            # Students can see all lessons (read-only)
            elif user_profile.user_type == 'student':
                return queryset
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's lessons"""
        today = timezone.now().date()
        lessons = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def this_week(self, request):
        """Get this week's lessons"""
        today = timezone.now().date()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        lessons = self.get_queryset().filter(date__range=[start_week, end_week])
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_teacher(self, request):
        """Get lessons by teacher"""
        teacher_id = request.query_params.get('teacher_id', '')
        if not teacher_id:
            return Response({'error': 'Teacher ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        lessons = self.get_queryset().filter(teacher_id=teacher_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """Get lessons by subject"""
        subject_id = request.query_params.get('subject_id', '')
        if not subject_id:
            return Response({'error': 'Subject ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        lessons = self.get_queryset().filter(subject_id=subject_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
