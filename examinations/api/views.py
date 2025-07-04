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

from ..models import (
    Exam, ExamResult, Test, Question, Answer, 
    TestAttempt, StudentAnswer
)
from .serializers import (
    ExamSerializer, ExamResultSerializer, ExamCreateSerializer,
    TestSerializer, TestDetailSerializer, QuestionSerializer, AnswerSerializer,
    TestAttemptSerializer, TestAttemptDetailSerializer, StudentAnswerSerializer,
    BulkGradeExamSerializer, BulkGradeTestSerializer,
    ExamStatsSerializer, TestStatsSerializer
)

User = get_user_model()


class ExamViewSet(viewsets.ModelViewSet):
    """
    Enhanced ViewSet for managing exams with comprehensive functionality
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exam_type', 'course', 'status', 'date']
    search_fields = ['title', 'description', 'subject']
    ordering_fields = ['date', 'start_time', 'title', 'max_marks']
    ordering = ['-date', '-start_time']
    
    def get_permissions(self):
        """Role-based permissions for exam management"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_grade']:
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['statistics']:
            permission_classes = [IsStaffOrAdmin]
        else:
            permission_classes = [CanAccessExaminations]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return ExamCreateSerializer
        return ExamSerializer

    def get_queryset(self):
        """Filter queryset based on user role and permissions"""
        queryset = Exam.objects.select_related('course', 'created_by').prefetch_related('results')
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            if user_profile.user_type == 'staff':
                return queryset
            
            elif user_profile.user_type == 'teacher':
                try:
                    teacher = user.teacher
                    return queryset.filter(created_by=teacher)
                except:
                    return queryset.none()
            
            elif user_profile.user_type == 'student':
                try:
                    student = user.student
                    # Get exams for student's enrolled courses
                    enrolled_courses = student.enrollments.filter(
                        is_active=True
                    ).values_list('course', flat=True)
                    return queryset.filter(course__in=enrolled_courses)
                except:
                    return queryset.none()
                    
        except:
            return queryset.none()

    def perform_create(self, serializer):
        """Set created_by to current teacher"""
        try:
            teacher = self.request.user.teacher
            serializer.save(created_by=teacher)
        except:
            raise serializers.ValidationError("Only teachers can create exams")

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get all results for a specific exam with statistics"""
        exam = self.get_object()
        results = exam.results.select_related('student__user', 'graded_by__user')
        
        # Apply sorting
        sort_by = request.query_params.get('sort_by', 'score')
        if sort_by == 'student_name':
            results = results.order_by('student__user__first_name', 'student__user__last_name')
        elif sort_by == 'percentage':
            results = results.order_by('-percentage')
        else:
            results = results.order_by('-score')
        
        serializer = ExamResultSerializer(results, many=True)
        
        # Calculate statistics
        graded_results = results.filter(is_graded=True, score__isnull=False)
        total_students = results.count()
        graded_count = graded_results.count()
        
        if graded_count > 0:
            scores = [r.score for r in graded_results]
            avg_score = sum(scores) / len(scores)
            highest_score = max(scores)
            lowest_score = min(scores)
            passed_count = graded_results.filter(score__gte=exam.passing_marks).count()
            pass_rate = (passed_count / graded_count) * 100
        else:
            avg_score = highest_score = lowest_score = 0
            passed_count = 0
            pass_rate = 0
        
        return Response({
            'exam': ExamSerializer(exam).data,
            'results': serializer.data,
            'statistics': {
                'total_students': total_students,
                'graded_count': graded_count,
                'pending_count': total_students - graded_count,
                'average_score': round(avg_score, 2),
                'highest_score': highest_score,
                'lowest_score': lowest_score,
                'passed_count': passed_count,
                'failed_count': graded_count - passed_count,
                'pass_rate': round(pass_rate, 2)
            }
        })

    @action(detail=True, methods=['post'])
    def bulk_grade(self, request, pk=None):
        """Bulk grade exam results"""
        exam = self.get_object()
        serializer = BulkGradeExamSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                teacher = request.user.teacher
                exam_results = serializer.validated_data['exam_results']
                updated_count = 0
                
                for result_data in exam_results:
                    try:
                        result = ExamResult.objects.get(
                            id=result_data['result_id'],
                            exam=exam
                        )
                        result.score = result_data['score']
                        result.grade_comment = result_data.get('grade_comment', '')
                        result.teacher_feedback = result_data.get('teacher_feedback', '')
                        result.graded_by = teacher
                        result.graded_at = timezone.now()
                        result.is_graded = True
                        result.save()
                        updated_count += 1
                    except ExamResult.DoesNotExist:
                        continue
                
                return Response({
                    'message': f'Successfully graded {updated_count} exam results',
                    'updated_count': updated_count
                })
                
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get comprehensive exam statistics"""
        user = request.user
        
        # Base queryset
        if user.is_staff or user.is_superuser:
            queryset = Exam.objects.all()
        else:
            try:
                teacher = user.teacher
                queryset = Exam.objects.filter(created_by=teacher)
            except:
                return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Date filtering
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        stats = {
            'total_exams': queryset.count(),
            'exams_this_month': queryset.filter(created_at__gte=month_start).count(),
            'total_students_examined': ExamResult.objects.filter(
                exam__in=queryset
            ).values('student').distinct().count(),
            'recent_exams': ExamSerializer(
                queryset.order_by('-created_at')[:5], many=True
            ).data
        }
        
        # Calculate score statistics
        graded_results = ExamResult.objects.filter(
            exam__in=queryset, 
            is_graded=True, 
            score__isnull=False
        )
        
        if graded_results.exists():
            scores = graded_results.values_list('score', flat=True)
            stats.update({
                'average_score': round(sum(scores) / len(scores), 2),
                'highest_score': max(scores),
                'lowest_score': min(scores),
            })
            
            # Calculate pass rate (assuming passing score is exam-specific)
            passed = 0
            total = 0
            for result in graded_results.select_related('exam'):
                total += 1
                if result.score >= result.exam.passing_marks:
                    passed += 1
            
            stats['pass_rate'] = round((passed / total) * 100, 2) if total > 0 else 0
        else:
            stats.update({
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'pass_rate': 0
            })
        
        return Response(stats)


class ExamResultViewSet(viewsets.ModelViewSet):
    """ViewSet for managing exam results and grading"""
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exam', 'student', 'is_graded', 'grade_letter']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__student_id']
    ordering_fields = ['score', 'percentage', 'submitted_at', 'created_at']
    ordering = ['-score']
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [CanAccessExaminations]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = ExamResult.objects.select_related('exam', 'student__user', 'graded_by__user')
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            if user_profile.user_type == 'teacher':
                teacher = user.teacher
                return queryset.filter(exam__created_by=teacher)
            
            elif user_profile.user_type == 'student':
                student = user.student
                return queryset.filter(student=student)
                
        except:
            return queryset.none()


class TestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing tests/quizzes"""
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['test_type', 'course', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'available_from', 'title']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [CanAccessExaminations]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestDetailSerializer
        return TestSerializer

    def get_queryset(self):
        queryset = Test.objects.select_related('course', 'created_by').prefetch_related('questions')
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            if user_profile.user_type == 'teacher':
                teacher = user.teacher
                return queryset.filter(created_by=teacher)
            
            elif user_profile.user_type == 'student':
                student = user.student
                enrolled_courses = student.enrollments.filter(
                    is_active=True
                ).values_list('course', flat=True)
                return queryset.filter(course__in=enrolled_courses, is_published=True)
                
        except:
            return queryset.none()

    def perform_create(self, serializer):
        try:
            teacher = self.request.user.teacher
            serializer.save(created_by=teacher)
        except:
            from rest_framework import serializers as drf_serializers
            raise drf_serializers.ValidationError("Only teachers can create tests")

    @action(detail=True, methods=['get'])
    def attempts(self, request, pk=None):
        """Get all attempts for a specific test"""
        test = self.get_object()
        attempts = test.attempts.select_related('student__user')
        
        serializer = TestAttemptSerializer(attempts, many=True)
        
        # Calculate statistics
        total_attempts = attempts.count()
        completed_attempts = attempts.filter(is_completed=True)
        graded_attempts = attempts.filter(is_graded=True)
        
        stats = {
            'total_attempts': total_attempts,
            'completed_attempts': completed_attempts.count(),
            'pending_attempts': total_attempts - completed_attempts.count(),
            'graded_attempts': graded_attempts.count(),
        }
        
        if graded_attempts.exists():
            scores = graded_attempts.values_list('score', flat=True)
            stats.update({
                'average_score': round(sum(scores) / len(scores), 2),
                'highest_score': max(scores),
                'lowest_score': min(scores),
            })
        
        return Response({
            'test': TestSerializer(test).data,
            'attempts': serializer.data,
            'statistics': stats
        })

    @action(detail=True, methods=['post'])
    def bulk_grade_answers(self, request, pk=None):
        """Bulk grade student answers for essay/short answer questions"""
        test = self.get_object()
        serializer = BulkGradeTestSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                teacher = request.user.teacher
                student_answers = serializer.validated_data['student_answers']
                updated_count = 0
                
                for answer_data in student_answers:
                    try:
                        answer = StudentAnswer.objects.get(
                            id=answer_data['answer_id'],
                            attempt__test=test
                        )
                        answer.points_earned = answer_data['points_earned']
                        answer.teacher_feedback = answer_data.get('teacher_feedback', '')
                        answer.is_graded = True
                        answer.save()
                        updated_count += 1
                        
                        # Update attempt score if all questions are graded
                        attempt = answer.attempt
                        if not attempt.student_answers.filter(is_graded=False).exists():
                            total_score = attempt.student_answers.aggregate(
                                total=Sum('points_earned')
                            )['total'] or 0
                            attempt.score = total_score
                            attempt.percentage = (total_score / test.total_points) * 100 if test.total_points > 0 else 0
                            attempt.is_graded = True
                            attempt.graded_by = teacher
                            attempt.graded_at = timezone.now()
                            attempt.save()
                        
                    except StudentAnswer.DoesNotExist:
                        continue
                
                return Response({
                    'message': f'Successfully graded {updated_count} answers',
                    'updated_count': updated_count
                })
                
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing test questions"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['test', 'question_type']
    ordering_fields = ['order', 'points']
    ordering = ['test', 'order']
    
    def get_permissions(self):
        return [IsTeacherOrAdmin()]

    def get_queryset(self):
        queryset = Question.objects.select_related('test').prefetch_related('answers')
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            teacher = user.teacher
            return queryset.filter(test__created_by=teacher)
        except:
            return queryset.none()


class AnswerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing answer choices"""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['question', 'is_correct']
    ordering_fields = ['order']
    ordering = ['question', 'order']
    
    def get_permissions(self):
        return [IsTeacherOrAdmin()]

    def get_queryset(self):
        queryset = Answer.objects.select_related('question__test')
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            teacher = user.teacher
            return queryset.filter(question__test__created_by=teacher)
        except:
            return queryset.none()


class TestAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing test attempts"""
    queryset = TestAttempt.objects.all()
    serializer_class = TestAttemptSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['test', 'student', 'is_completed', 'is_graded']
    ordering_fields = ['started_at', 'score']
    ordering = ['-started_at']
    
    def get_permissions(self):
        return [CanAccessExaminations()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestAttemptDetailSerializer
        return TestAttemptSerializer

    def get_queryset(self):
        queryset = TestAttempt.objects.select_related('test', 'student__user')
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            if user_profile.user_type == 'teacher':
                teacher = user.teacher
                return queryset.filter(test__created_by=teacher)
            
            elif user_profile.user_type == 'student':
                student = user.student
                return queryset.filter(student=student)
                
        except:
            return queryset.none()
