# filepath: c:\Users\USER\PycharmProjects\edumanage\courses\api\views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, IsTeacherOrAdmin,
    ReadOnlyForStudents, IsStudentOrTeacherOrAdmin
)
from rest_framework.permissions import BasePermission

from ..models import (
    Course, CourseEnrollment, CourseContent, Assignment,
    AssignmentSubmission, CourseAnnouncement
)
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, CourseCreateUpdateSerializer,
    CourseEnrollmentSerializer, CourseEnrollmentCreateSerializer,
    CourseContentSerializer, AssignmentSerializer, AssignmentCreateUpdateSerializer,
    AssignmentSubmissionSerializer, AssignmentSubmissionCreateSerializer,
    AssignmentGradingSerializer, CourseAnnouncementSerializer, CourseStatsSerializer
)


class CanManageCourse(BasePermission):
    """
    Permission that allows course instructors to manage their own courses,
    and staff/admins to manage any course.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can manage any course
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Staff can manage any course
        try:
            user_profile = request.user.userprofile
            if user_profile.user_type == 'staff':
                return True
        except:
            pass
        
        # Teachers can only manage their own courses
        try:
            if hasattr(obj, 'instructor'):
                return obj.instructor.user == request.user
            elif hasattr(obj, 'course') and hasattr(obj.course, 'instructor'):
                return obj.course.instructor.user == request.user
            elif hasattr(obj, 'content') and hasattr(obj.content.course, 'instructor'):
                return obj.content.course.instructor.user == request.user
        except:
            pass
        
        return False


class CanManageOwnSubmission(BasePermission):
    """
    Permission that allows students to manage their own submissions,
    and teachers/staff to manage submissions for their courses.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can manage any submission
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        try:
            user_profile = request.user.userprofile
            
            # Staff can manage any submission
            if user_profile.user_type == 'staff':
                return True
            
            # Teachers can manage submissions for their courses
            elif user_profile.user_type == 'teacher':
                try:
                    teacher = request.user.teacher
                    return obj.assignment.content.course.instructor == teacher
                except:
                    return False
            
            # Students can only manage their own submissions
            elif user_profile.user_type == 'student':
                try:
                    student = request.user.student
                    return obj.student == student
                except:
                    return False
        except:
            pass
        
        return False


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses with role-based permissions
    - Admins/Staff: Full access to all courses
    - Teachers: Can create/manage their own courses, view all courses
    - Students: Can view published courses and enroll/unenroll
    """
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'instructor', 'difficulty_level', 'status']
    search_fields = ['title', 'description', 'subject__name', 'instructor__user__first_name', 'instructor__user__last_name']
    ordering_fields = ['title', 'start_date', 'end_date', 'created_at', 'enrollment_count']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Role-based permissions for course management
        """
        if self.action in ['create']:
            # Teachers and staff/admins can create courses
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Course instructors can update their courses, staff/admins can update any
            permission_classes = [CanManageCourse]
        elif self.action in ['enroll', 'unenroll']:
            # Only students can enroll/unenroll
            permission_classes = [IsStudentOrTeacherOrAdmin]
        else:
            # All authenticated users can view courses
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = Course.objects.select_related('subject', 'instructor__user').prefetch_related('prerequisites')
        user = self.request.user
        
        # Admin users and staff can see all courses
        if user.is_staff or user.is_superuser:
            pass  # Return all courses
        else:
            try:
                user_profile = user.userprofile
                
                # Staff can see all courses
                if user_profile.user_type == 'staff':
                    pass  # Return all courses
                
                # Teachers can see all courses
                elif user_profile.user_type == 'teacher':
                    pass  # Return all courses
                
                # Students can only see published courses
                elif user_profile.user_type == 'student':
                    queryset = queryset.filter(status='published')
                
            except:
                # Default to published courses only for unauthenticated or unknown users
                queryset = queryset.filter(status='published')
        
        # Filter by enrollment status
        enrollment_status = self.request.query_params.get('enrollment_status')
        if enrollment_status == 'available':
            queryset = queryset.filter(status='published').exclude(
                id__in=CourseEnrollment.objects.filter(
                    student__user=self.request.user,
                    is_active=True
                ).values_list('course_id', flat=True)
            )
        elif enrollment_status == 'enrolled':
            queryset = queryset.filter(
                id__in=CourseEnrollment.objects.filter(
                    student__user=self.request.user,
                    is_active=True
                ).values_list('course_id', flat=True)
            )
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseDetailSerializer
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll a student in the course"""
        course = self.get_object()
        
        try:
            student = request.user.student
        except:
            return Response(
                {'error': 'Only students can enroll in courses'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already enrolled
        if CourseEnrollment.objects.filter(student=student, course=course, is_active=True).exists():
            return Response(
                {'error': 'Already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if course is full
        if course.is_full:
            return Response(
                {'error': 'Course is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create enrollment
        enrollment = CourseEnrollment.objects.create(student=student, course=course)
        serializer = CourseEnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def unenroll(self, request, pk=None):
        """Unenroll a student from the course"""
        course = self.get_object()
        
        try:
            student = request.user.student
        except:
            return Response(
                {'error': 'Only students can unenroll from courses'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            enrollment = CourseEnrollment.objects.get(student=student, course=course, is_active=True)
            enrollment.is_active = False
            enrollment.save()
            return Response({'message': 'Successfully unenrolled'}, status=status.HTTP_200_OK)
        except CourseEnrollment.DoesNotExist:
            return Response(
                {'error': 'Not enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def content(self, request, pk=None):
        """Get all content for a specific course"""
        course = self.get_object()
        contents = course.contents.all().order_by('order')
        serializer = CourseContentSerializer(contents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get all assignments for a specific course"""
        course = self.get_object()
        assignments = Assignment.objects.filter(content__course=course).select_related('content')
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get all enrollments for a specific course"""
        course = self.get_object()
        enrollments = course.enrollments.filter(is_active=True).select_related('student__user')
        serializer = CourseEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Get detailed analytics for a specific course"""
        course = self.get_object()
        
        analytics_data = {
            'enrollment_stats': {
                'total_enrolled': course.enrollment_count,
                'completed': course.enrollments.filter(completion_date__isnull=False).count(),
                'active': course.enrollments.filter(is_active=True, completion_date__isnull=True).count(),
                'completion_rate': course.completion_rate
            },
            'content_stats': {
                'total_content': course.contents.count(),
                'by_type': course.contents.values('content_type').annotate(count=Count('id'))
            },
            'assignment_stats': {
                'total_assignments': Assignment.objects.filter(content__course=course).count(),
                'total_submissions': AssignmentSubmission.objects.filter(assignment__content__course=course).count(),
                'graded_submissions': AssignmentSubmission.objects.filter(
                    assignment__content__course=course,
                    grade__isnull=False
                ).count()
            },
            'grade_distribution': self._get_grade_distribution(course),
            'recent_activity': self._get_recent_activity(course)
        }
        
        return Response(analytics_data)
    
    def _get_grade_distribution(self, course):
        """Helper method to get grade distribution"""
        submissions = AssignmentSubmission.objects.filter(
            assignment__content__course=course,
            grade__isnull=False
        )
        
        if not submissions:
            return {}
        
        grades = [float(sub.grade) for sub in submissions]
        return {
            'average': sum(grades) / len(grades),
            'highest': max(grades),
            'lowest': min(grades),
            'total_graded': len(grades)
        }
    
    def _get_recent_activity(self, course):
        """Helper method to get recent course activity"""
        recent_enrollments = course.enrollments.filter(
            date_enrolled__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        recent_submissions = AssignmentSubmission.objects.filter(
            assignment__content__course=course,
            submitted_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        return {
            'recent_enrollments': recent_enrollments,
            'recent_submissions': recent_submissions
        }
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get overall course statistics"""
        stats = {
            'total_courses': Course.objects.count(),
            'active_courses': Course.objects.filter(status='published').count(),
            'draft_courses': Course.objects.filter(status='draft').count(),
            'archived_courses': Course.objects.filter(status='archived').count(),
            'total_enrollments': CourseEnrollment.objects.filter(is_active=True).count(),
            'total_students': CourseEnrollment.objects.filter(is_active=True).values('student').distinct().count(),
            'average_completion_rate': Course.objects.aggregate(
                avg_rate=Avg('enrollments__progress_percentage')
            )['avg_rate'] or 0,
            'most_popular_courses': Course.objects.annotate(
                enrollment_count=Count('enrollments', filter=Q(enrollments__is_active=True))
            ).order_by('-enrollment_count')[:5],
            'recent_enrollments': CourseEnrollment.objects.filter(
                date_enrolled__gte=timezone.now() - timedelta(days=7)
            ).select_related('student__user', 'course')[:10]
        }
        
        serializer = CourseStatsSerializer(stats)
        return Response(serializer.data)


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing course enrollments with role-based permissions
    - Admins/Staff: Full access to all enrollments
    - Teachers: Can view enrollments for their courses
    - Students: Can view their own enrollments only
    """
    queryset = CourseEnrollment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'student', 'is_active']
    ordering_fields = ['date_enrolled', 'progress_percentage']
    ordering = ['-date_enrolled']
    
    def get_permissions(self):
        """
        Role-based permissions for enrollment management
        """
        if self.action in ['create', 'destroy']:
            # Students can create/delete their own enrollments, staff/admins can manage any
            permission_classes = [IsOwnerOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # Teachers can update enrollments for their courses, staff/admins can update any
            permission_classes = [IsOwnerOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = CourseEnrollment.objects.select_related(
            'student__user', 'course__subject', 'course__instructor__user'
        )
        user = self.request.user
        
        # Admin users and staff can see all enrollments
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all enrollments
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see enrollments for their courses
            elif user_profile.user_type == 'teacher':
                try:
                    teacher = user.teacher
                    return queryset.filter(course__instructor=teacher)
                except:
                    return queryset.none()
            
            # Students can only see their own enrollments
            elif user_profile.user_type == 'student':
                try:
                    student = user.student
                    return queryset.filter(student=student)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CourseEnrollmentCreateSerializer
        return CourseEnrollmentSerializer
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update enrollment progress percentage"""
        enrollment = self.get_object()
        progress = request.data.get('progress_percentage')
        
        if progress is None:
            return Response(
                {'error': 'progress_percentage is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            progress = float(progress)
            if 0 <= progress <= 100:
                enrollment.progress_percentage = progress
                if progress == 100 and not enrollment.completion_date:
                    enrollment.completion_date = timezone.now()
                enrollment.save()
                
                serializer = CourseEnrollmentSerializer(enrollment)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Progress must be between 0 and 100'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Invalid progress value'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CourseContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing course content with role-based permissions
    - Admins/Staff: Full access to all course content
    - Teachers: Can manage content for their own courses, view all content
    - Students: Can view content for courses they're enrolled in
    """
    queryset = CourseContent.objects.all()
    serializer_class = CourseContentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'content_type', 'is_required']
    ordering_fields = ['order', 'created_at']
    ordering = ['course', 'order']
    
    def get_permissions(self):
        """
        Role-based permissions for course content management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Course instructors can manage their content, staff/admins can manage any
            permission_classes = [CanManageCourse]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = CourseContent.objects.select_related('course')
        user = self.request.user
        
        # Admin users and staff can see all content
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all content
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see all content
            elif user_profile.user_type == 'teacher':
                return queryset
            
            # Students can only see content for courses they're enrolled in
            elif user_profile.user_type == 'student':
                try:
                    student = user.student
                    enrolled_course_ids = student.courseenrollment_set.filter(
                        is_active=True
                    ).values_list('course_id', flat=True)
                    return queryset.filter(course_id__in=enrolled_course_ids)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple course contents at once"""
        contents_data = request.data.get('contents', [])
        
        if not contents_data:
            return Response(
                {'error': 'No content data provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_contents = []
        for content_data in contents_data:
            serializer = CourseContentSerializer(data=content_data)
            if serializer.is_valid():
                content = serializer.save()
                created_contents.append(content)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        response_serializer = CourseContentSerializer(created_contents, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assignments with role-based permissions
    - Admins/Staff: Full access to all assignments
    - Teachers: Can manage assignments for their own courses, view all assignments
    - Students: Can view assignments for courses they're enrolled in
    """
    queryset = Assignment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content__course', 'submission_type', 'allow_late_submission']
    ordering_fields = ['due_date', 'total_points']
    ordering = ['due_date']
    
    def get_permissions(self):
        """
        Role-based permissions for assignment management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_grade']:
            # Course instructors can manage their assignments, staff/admins can manage any
            permission_classes = [CanManageCourse]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = Assignment.objects.select_related('content__course')
        user = self.request.user
        
        # Admin users and staff can see all assignments
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all assignments
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see all assignments (but can only modify their own)
            elif user_profile.user_type == 'teacher':
                return queryset
            
            # Students can only see assignments for courses they're enrolled in
            elif user_profile.user_type == 'student':
                try:
                    student = user.student
                    enrolled_course_ids = student.courseenrollment_set.filter(
                        is_active=True
                    ).values_list('course_id', flat=True)
                    return queryset.filter(content__course_id__in=enrolled_course_ids)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AssignmentCreateUpdateSerializer
        return AssignmentSerializer
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get all submissions for a specific assignment"""
        assignment = self.get_object()
        submissions = assignment.submissions.select_related('student__user', 'graded_by__user')
        
        # Filter by grading status
        grading_status = request.query_params.get('grading_status')
        if grading_status == 'graded':
            submissions = submissions.filter(grade__isnull=False)
        elif grading_status == 'ungraded':
            submissions = submissions.filter(grade__isnull=True)
        
        serializer = AssignmentSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def bulk_grade(self, request, pk=None):
        """Grade multiple submissions at once"""
        assignment = self.get_object()
        grading_data = request.data.get('grades', [])
        
        if not grading_data:
            return Response(
                {'error': 'No grading data provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        graded_submissions = []
        for grade_info in grading_data:
            submission_id = grade_info.get('submission_id')
            grade = grade_info.get('grade')
            feedback = grade_info.get('feedback', '')
            
            try:
                submission = assignment.submissions.get(id=submission_id)
                submission.grade = grade
                submission.feedback = feedback
                submission.graded_by = request.user.teacher
                submission.graded_at = timezone.now()
                submission.save()
                graded_submissions.append(submission)
            except AssignmentSubmission.DoesNotExist:
                continue
        
        serializer = AssignmentSubmissionSerializer(graded_submissions, many=True)
        return Response(serializer.data)


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assignment submissions with role-based permissions
    - Admins/Staff: Full access to all submissions
    - Teachers: Can view/grade submissions for their courses
    - Students: Can only view/create their own submissions
    """
    queryset = AssignmentSubmission.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['assignment', 'student', 'grade']
    ordering_fields = ['submitted_at', 'grade']
    ordering = ['-submitted_at']
    
    def get_permissions(self):
        """
        Role-based permissions for assignment submission management
        """
        if self.action in ['create']:
            # Students can create their own submissions, teachers/staff can create any
            permission_classes = [IsStudentOrTeacherOrAdmin]
        elif self.action in ['grade']:
            # Only teachers and staff/admins can grade submissions
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Students can update their own submissions, teachers/staff can update any
            permission_classes = [CanManageOwnSubmission]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = AssignmentSubmission.objects.select_related(
            'assignment__content__course', 'student__user', 'graded_by__user'
        )
        user = self.request.user
        
        # Admin users and staff can see all submissions
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all submissions
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see submissions for their courses
            elif user_profile.user_type == 'teacher':
                try:
                    teacher = user.teacher
                    return queryset.filter(assignment__content__course__instructor=teacher)
                except:
                    return queryset.none()
            
            # Students can only see their own submissions
            elif user_profile.user_type == 'student':
                try:
                    student = user.student
                    return queryset.filter(student=student)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentSubmissionCreateSerializer
        elif self.action in ['grade']:
            return AssignmentGradingSerializer
        return AssignmentSubmissionSerializer
    
    def perform_create(self, serializer):
        # Set the student from the current user
        if hasattr(self.request.user, 'student'):
            serializer.save(student=self.request.user.student)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """Grade a specific submission"""
        submission = self.get_object()
        serializer = AssignmentGradingSerializer(submission, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(
                graded_by=request.user.teacher,
                graded_at=timezone.now()
            )
            response_serializer = AssignmentSubmissionSerializer(submission)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseAnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing course announcements with role-based permissions
    - Admins/Staff: Full access to all announcements
    - Teachers: Can manage announcements for their own courses, view all announcements
    - Students: Can view announcements for courses they're enrolled in
    """
    queryset = CourseAnnouncement.objects.all()
    serializer_class = CourseAnnouncementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'is_pinned']
    ordering_fields = ['created_at', 'is_pinned']
    ordering = ['-is_pinned', '-created_at']
    
    def get_permissions(self):
        """
        Role-based permissions for course announcement management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'toggle_pin']:
            # Course instructors can manage their announcements, staff/admins can manage any
            permission_classes = [CanManageCourse]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = CourseAnnouncement.objects.select_related('course', 'created_by__user')
        user = self.request.user
        
        # Admin users and staff can see all announcements
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all announcements
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see all announcements (but can only modify their own)
            elif user_profile.user_type == 'teacher':
                return queryset
            
            # Students can only see announcements for courses they're enrolled in
            elif user_profile.user_type == 'student':
                try:
                    student = user.student
                    enrolled_course_ids = student.courseenrollment_set.filter(
                        is_active=True
                    ).values_list('course_id', flat=True)
                    return queryset.filter(course_id__in=enrolled_course_ids)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()
    
    def perform_create(self, serializer):
        # Set the created_by from the current user's teacher profile
        if hasattr(self.request.user, 'teacher'):
            serializer.save(created_by=self.request.user.teacher)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def toggle_pin(self, request, pk=None):
        """Toggle the pinned status of an announcement"""
        announcement = self.get_object()
        announcement.is_pinned = not announcement.is_pinned
        announcement.save()
        
        serializer = CourseAnnouncementSerializer(announcement)
        return Response(serializer.data)
