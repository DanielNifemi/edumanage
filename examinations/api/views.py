from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Sum, Max, Min
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
from django.contrib.auth import get_user_model
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, IsTeacherOrAdmin,
    IsStudentOrTeacherOrAdmin, CanAccessExaminations
)

from ..models import Exam, ExamResult
from .serializers import (
    ExamSerializer, ExamResultSerializer, ExamDetailSerializer, 
    ExamResultDetailSerializer, ExamStatsSerializer, BulkGradingSerializer
)

User = get_user_model()


class ExamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing exams with role-based permissions
    - Admins/Staff: Full access to all exams and exam management
    - Teachers: Can create/manage exams for their courses and subjects
    - Students: Can view exams they are registered for
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'exam_type', 'date']
    search_fields = ['title', 'subject__name', 'description']
    ordering_fields = ['date', 'title', 'max_marks']
    ordering = ['-date']
    
    def get_permissions(self):
        """
        Role-based permissions for exam management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_grade']:
            # Teachers and staff/admins can create/modify exams
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['statistics']:
            # Only staff/admins can access aggregated exam statistics
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [CanAccessExaminations]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamDetailSerializer
        return ExamSerializer

    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = Exam.objects.all()
        user = self.request.user
        
        # Admin users and staff can see all exams
        if user.is_staff or user.is_superuser:
            pass  # Return all exams
        else:
            try:
                user_profile = user.userprofile
                
                # Staff can see all exams
                if user_profile.user_type == 'staff':
                    pass  # Return all exams
                
                # Teachers can see exams for their subjects/courses
                elif user_profile.user_type == 'teacher':
                    try:
                        teacher = user.teacher
                        # Filter exams for teacher's subjects and courses
                        teacher_subjects = teacher.subjects.all()
                        teacher_courses = teacher.courses_taught.all()
                        
                        queryset = queryset.filter(
                            Q(subject__in=teacher_subjects) |
                            Q(course__in=teacher_courses)
                        )
                    except:
                        queryset = queryset.none()
                
                # Students can see exams for their enrolled courses
                elif user_profile.user_type == 'student':
                    try:
                        student = user.student
                        # Get exams for student's enrolled courses
                        enrolled_courses = student.enrollments.filter(
                            is_active=True
                        ).values_list('course', flat=True)
                        
                        queryset = queryset.filter(course__in=enrolled_courses)
                    except:
                        queryset = queryset.none()
                
            except:
                # Default: no access for unknown user types
                queryset = queryset.none()
        
        # Apply additional filters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter by class
        class_id = self.request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(class_group_id=class_id)
        
        # Filter by teacher
        teacher_id = self.request.query_params.get('teacher_id')
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        return queryset

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get all results for a specific exam"""
        exam = self.get_object()
        results = ExamResult.objects.filter(exam=exam).select_related('student')
        
        # Apply sorting
        sort_by = request.query_params.get('sort_by', 'marks_obtained')
        if sort_by == 'rank':
            results = results.order_by('-marks_obtained')
        elif sort_by == 'student_name':
            results = results.order_by('student__first_name', 'student__last_name')
        else:
            results = results.order_by('-marks_obtained')
        
        serializer = ExamResultDetailSerializer(results, many=True)
        
        # Calculate exam statistics
        total_students = results.count()
        if total_students > 0:
            avg_marks = results.aggregate(Avg('marks_obtained'))['marks_obtained__avg']
            highest_marks = results.aggregate(Max('marks_obtained'))['marks_obtained__max']
            lowest_marks = results.aggregate(Min('marks_obtained'))['marks_obtained__min']
            pass_count = results.filter(marks_obtained__gte=exam.passing_marks).count()
            pass_rate = (pass_count / total_students) * 100
        else:
            avg_marks = highest_marks = lowest_marks = 0
            pass_count = 0
            pass_rate = 0
        
        return Response({
            'exam': ExamDetailSerializer(exam).data,
            'results': serializer.data,
            'statistics': {
                'total_students': total_students,
                'average_marks': round(avg_marks, 2) if avg_marks else 0,
                'highest_marks': highest_marks,
                'lowest_marks': lowest_marks,
                'pass_count': pass_count,
                'fail_count': total_students - pass_count,
                'pass_rate': round(pass_rate, 2)
            }
        })

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Get detailed analytics for an exam"""
        exam = self.get_object()
        results = ExamResult.objects.filter(exam=exam)
        
        if not results.exists():
            return Response({
                'exam': ExamDetailSerializer(exam).data,
                'analytics': {
                    'message': 'No results available for analysis'
                }
            })
        
        # Grade distribution
        grade_distribution = defaultdict(int)
        marks_ranges = defaultdict(int)
        
        for result in results:
            grade_distribution[result.grade] += 1
            
            # Marks range distribution
            percentage = (result.marks_obtained / exam.max_marks) * 100
            if percentage >= 90:
                marks_ranges['90-100%'] += 1
            elif percentage >= 80:
                marks_ranges['80-89%'] += 1
            elif percentage >= 70:
                marks_ranges['70-79%'] += 1
            elif percentage >= 60:
                marks_ranges['60-69%'] += 1
            elif percentage >= 50:
                marks_ranges['50-59%'] += 1
            else:
                marks_ranges['Below 50%'] += 1
        
        # Performance quartiles
        marks_list = list(results.values_list('marks_obtained', flat=True))
        marks_list.sort()
        
        n = len(marks_list)
        q1 = marks_list[n//4] if n > 0 else 0
        q2 = marks_list[n//2] if n > 0 else 0  # Median
        q3 = marks_list[3*n//4] if n > 0 else 0
        
        return Response({
            'exam': ExamDetailSerializer(exam).data,
            'analytics': {
                'grade_distribution': dict(grade_distribution),
                'marks_ranges': dict(marks_ranges),
                'quartiles': {
                    'q1': q1,
                    'median': q2,
                    'q3': q3
                },
                'total_results': results.count()
            }
        })

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming exams"""
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=days)
        
        upcoming_exams = self.queryset.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        serializer = ExamDetailSerializer(upcoming_exams, many=True)
        
        return Response({
            'upcoming_exams': serializer.data,
            'period_days': days,
            'total_upcoming': upcoming_exams.count()
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get overall exam statistics"""
        # Date range filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.queryset
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        total_exams = queryset.count()
        
        # Exam type distribution
        exam_types = queryset.values('exam_type').annotate(
            count=Count('id')
        ).order_by('exam_type')
        
        # Monthly exam count
        monthly_exams = queryset.extra(
            select={'month': "strftime('%%Y-%%m', date)"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        # Subject-wise exam count
        subject_exams = queryset.values('subject__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'total_exams': total_exams,
            'exam_type_distribution': list(exam_types),
            'monthly_distribution': list(monthly_exams),
            'subject_distribution': list(subject_exams),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        })


class ExamResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing exam results with role-based permissions
    - Admins/Staff: Full access to all exam results
    - Teachers: Can create/view results for their exams and students
    - Students: Can view their own exam results only
    """
    queryset = ExamResult.objects.select_related('exam', 'student').all()
    serializer_class = ExamResultSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exam', 'student', 'grade']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'exam__title']
    ordering_fields = ['marks_obtained', 'exam__date', 'grade']
    ordering = ['-exam__date', '-marks_obtained']
    
    def get_permissions(self):
        """
        Role-based permissions for exam result management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_grade']:
            # Teachers and staff/admins can create/update results
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['top_performers', 'grade_distribution']:
            # Only staff/admins can access aggregated result statistics
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [CanAccessExaminations]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = ExamResult.objects.select_related('exam', 'student').all()
        user = self.request.user
        
        # Admin users and staff can see all results
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all results
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see results for their exams and students
            elif user_profile.user_type == 'teacher':
                try:
                    teacher = user.teacher
                    # Get results for teacher's exams and students in their courses
                    teacher_subjects = teacher.subjects.all()
                    teacher_courses = teacher.courses_taught.all()
                    
                    # Filter results for teacher's exams or students in their courses
                    student_ids = []
                    for course in teacher_courses:
                        course_student_ids = course.enrollments.filter(
                            is_active=True
                        ).values_list('student_id', flat=True)
                        student_ids.extend(course_student_ids)
                    
                    return queryset.filter(
                        Q(exam__subject__in=teacher_subjects) |
                        Q(exam__course__in=teacher_courses) |
                        Q(student__student__in=student_ids)
                    )
                except:
                    return queryset.none()
            
            # Students can only see their own results
            elif user_profile.user_type == 'student':
                try:
                    return queryset.filter(student=user)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamResultDetailSerializer
        elif self.action == 'bulk_grade':
            return BulkGradingSerializer
        return ExamResultSerializer

    @action(detail=False, methods=['post'])
    def bulk_grade(self, request):
        """Grade multiple students for an exam"""
        serializer = BulkGradingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        exam_id = serializer.validated_data['exam_id']
        results_data = serializer.validated_data['results']
        
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response(
                {'error': 'Exam not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        created_results = []
        updated_results = []
        errors = []
        
        for result_data in results_data:
            student_id = result_data['student_id']
            marks_obtained = result_data['marks_obtained']
            
            try:
                student = User.objects.get(id=student_id)
                
                # Validate marks
                if marks_obtained > exam.max_marks:
                    errors.append(f"Marks for student {student_id} exceed maximum marks")
                    continue
                
                result, created = ExamResult.objects.update_or_create(
                    exam=exam,
                    student=student,
                    defaults={'marks_obtained': marks_obtained}
                )
                
                if created:
                    created_results.append(ExamResultDetailSerializer(result).data)
                else:
                    updated_results.append(ExamResultDetailSerializer(result).data)
                    
            except User.DoesNotExist:
                errors.append(f"Student with ID {student_id} not found")
            except Exception as e:
                errors.append(f"Error for student {student_id}: {str(e)}")
        
        return Response({
            'exam_id': exam_id,
            'created_results': created_results,
            'updated_results': updated_results,
            'total_created': len(created_results),
            'total_updated': len(updated_results),
            'errors': errors
        })

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get all exam results for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = self.queryset.filter(student_id=student_id)
        
        # Apply date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            results = results.filter(exam__date__gte=start_date)
        if end_date:
            results = results.filter(exam__date__lte=end_date)
        
        serializer = ExamResultDetailSerializer(results, many=True)
        
        # Calculate student statistics
        total_exams = results.count()
        if total_exams > 0:
            avg_marks = results.aggregate(Avg('marks_obtained'))['marks_obtained__avg']
            best_performance = results.order_by('-marks_obtained').first()
            worst_performance = results.order_by('marks_obtained').first()
            
            # Calculate percentage averages
            percentages = []
            for result in results:
                percentage = (result.marks_obtained / result.exam.max_marks) * 100
                percentages.append(percentage)
            avg_percentage = sum(percentages) / len(percentages) if percentages else 0
        else:
            avg_marks = avg_percentage = 0
            best_performance = worst_performance = None
        
        return Response({
            'student_id': student_id,
            'results': serializer.data,
            'statistics': {
                'total_exams': total_exams,
                'average_marks': round(avg_marks, 2) if avg_marks else 0,
                'average_percentage': round(avg_percentage, 2),
                'best_performance': ExamResultDetailSerializer(best_performance).data if best_performance else None,
                'worst_performance': ExamResultDetailSerializer(worst_performance).data if worst_performance else None
            }
        })

    @action(detail=False, methods=['get'])
    def by_exam(self, request):
        """Get all results for a specific exam"""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response(
                {'error': 'exam_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = self.queryset.filter(exam_id=exam_id)
        serializer = ExamResultDetailSerializer(results, many=True)
        
        return Response({
            'exam_id': exam_id,
            'results': serializer.data,
            'total_results': results.count()
        })

    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top performing students"""
        limit = int(request.query_params.get('limit', 10))
        exam_id = request.query_params.get('exam_id')
        
        queryset = self.queryset
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        
        # Get top performers based on marks obtained
        top_results = queryset.order_by('-marks_obtained')[:limit]
        serializer = ExamResultDetailSerializer(top_results, many=True)
        
        return Response({
            'top_performers': serializer.data,
            'limit': limit,
            'exam_id': exam_id if exam_id else 'all_exams'
        })

    @action(detail=False, methods=['get'])
    def grade_distribution(self, request):
        """Get grade distribution across results"""
        exam_id = request.query_params.get('exam_id')
        
        queryset = self.queryset
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        
        # Get grade distribution
        grade_counts = queryset.values('grade').annotate(
            count=Count('id'),
            percentage=Count('id') * 100.0 / queryset.count()
        ).order_by('grade')
        
        return Response({
            'grade_distribution': list(grade_counts),
            'total_results': queryset.count(),
            'exam_id': exam_id if exam_id else 'all_exams'
        })

    @action(detail=False, methods=['get'])
    def performance_trends(self, request):
        """Get performance trends over time"""
        student_id = request.query_params.get('student_id')
        subject_id = request.query_params.get('subject_id')
        
        queryset = self.queryset
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if subject_id:
            queryset = queryset.filter(exam__subject_id=subject_id)
        
        # Get results ordered by exam date
        results = queryset.select_related('exam').order_by('exam__date')
        
        trend_data = []
        for result in results:
            percentage = (result.marks_obtained / result.exam.max_marks) * 100
            trend_data.append({
                'exam_date': result.exam.date.isoformat(),
                'exam_title': result.exam.title,
                'marks_obtained': result.marks_obtained,
                'max_marks': result.exam.max_marks,
                'percentage': round(percentage, 2),
                'grade': result.grade
            })
        
        # Calculate trend direction
        if len(trend_data) >= 2:
            recent_avg = sum([d['percentage'] for d in trend_data[-3:]]) / min(3, len(trend_data))
            older_avg = sum([d['percentage'] for d in trend_data[:-3]]) / max(1, len(trend_data) - 3)
            trend_direction = 'improving' if recent_avg > older_avg else 'declining' if recent_avg < older_avg else 'stable'
        else:
            trend_direction = 'insufficient_data'
        
        return Response({
            'performance_trends': trend_data,
            'trend_analysis': {
                'direction': trend_direction,
                'total_exams': len(trend_data)
            },
            'filters': {
                'student_id': student_id,
                'subject_id': subject_id
            }
        })
