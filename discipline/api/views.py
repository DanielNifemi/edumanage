from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, IsTeacherOrAdmin,
    IsStudentOrTeacherOrAdmin, CanAccessDiscipline
)

from ..models import InfractionType, DisciplinaryAction, DisciplinaryRecord, BehaviorNote
from .serializers import (
    InfractionTypeSerializer, DisciplinaryActionSerializer, DisciplinaryRecordSerializer,
    DisciplinaryRecordDetailSerializer, BehaviorNoteSerializer, BulkRecordSerializer
)


class InfractionTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing infraction types with role-based permissions
    - Admins/Staff: Full access to manage infraction types
    - Teachers: Can view infraction types
    - Students: Read-only access to infraction types
    """
    queryset = InfractionType.objects.all()
    serializer_class = InfractionTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['severity']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'severity']
    ordering = ['severity', 'name']
    
    def get_permissions(self):
        """
        Role-based permissions for infraction type management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only staff/admins can create/modify infraction types
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view infraction types
            permission_classes = [CanAccessDiscipline]
        
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def by_severity(self, request):
        """Get infraction types grouped by severity"""
        severity_groups = {
            'minor': self.queryset.filter(severity=1),
            'moderate': self.queryset.filter(severity=2),
            'severe': self.queryset.filter(severity=3)
        }
        
        result = {}
        for severity, infractions in severity_groups.items():
            result[severity] = InfractionTypeSerializer(infractions, many=True).data
        
        return Response(result)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific infraction type"""
        infraction_type = self.get_object()
        records = DisciplinaryRecord.objects.filter(infraction_type=infraction_type)
        
        total_records = records.count()
        resolved_count = records.filter(resolved=True).count()
        recent_records = records.filter(date__gte=timezone.now().date() - timedelta(days=30)).count()
        
        # Monthly trends
        monthly_trends = records.extra(
            select={'month': "strftime('%%Y-%%m', date)"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        return Response({
            'infraction_type': InfractionTypeSerializer(infraction_type).data,
            'statistics': {
                'total_records': total_records,
                'resolved_count': resolved_count,
                'unresolved_count': total_records - resolved_count,
                'recent_records': recent_records,
                'resolution_rate': (resolved_count / total_records * 100) if total_records > 0 else 0
            },
            'monthly_trends': list(monthly_trends)
        })


class DisciplinaryActionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing disciplinary actions with role-based permissions
    - Admins/Staff: Full access to manage disciplinary actions
    - Teachers: Can view and assign disciplinary actions
    - Students: Read-only access to disciplinary actions
    """
    queryset = DisciplinaryAction.objects.all()
    serializer_class = DisciplinaryActionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Role-based permissions for disciplinary action management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only staff/admins can create/modify disciplinary actions
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view disciplinary actions
            permission_classes = [CanAccessDiscipline]
        
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def effectiveness(self, request, pk=None):
        """Get effectiveness statistics for a disciplinary action"""
        action = self.get_object()
        records_with_action = DisciplinaryRecord.objects.filter(action_taken=action)
        
        total_cases = records_with_action.count()
        resolved_cases = records_with_action.filter(resolved=True).count()
        
        # Calculate average resolution time
        resolved_records = records_with_action.filter(resolved=True, action_date__isnull=False)
        avg_resolution_days = 0
        if resolved_records.exists():
            resolution_times = []
            for record in resolved_records:
                if record.action_date:
                    days = (record.action_date - record.date).days
                    resolution_times.append(days)
            avg_resolution_days = sum(resolution_times) / len(resolution_times) if resolution_times else 0
        
        return Response({
            'action': DisciplinaryActionSerializer(action).data,
            'effectiveness': {
                'total_cases': total_cases,
                'resolved_cases': resolved_cases,
                'resolution_rate': (resolved_cases / total_cases * 100) if total_cases > 0 else 0,
                'average_resolution_days': round(avg_resolution_days, 1)
            }
        })


class DisciplinaryRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing disciplinary records with role-based permissions
    - Admins/Staff: Full access to all disciplinary records
    - Teachers: Can create/view records for their students and report infractions
    - Students: Can view their own disciplinary records only
    """
    queryset = DisciplinaryRecord.objects.select_related(
        'student', 'infraction_type', 'action_taken', 'reported_by'
    ).all()
    serializer_class = DisciplinaryRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'infraction_type', 'action_taken', 'resolved', 'reported_by']
    search_fields = ['student__user__username', 'student__user__first_name', 'student__user__last_name', 'description']
    ordering_fields = ['date', 'student', 'infraction_type__severity']
    ordering = ['-date']
    
    def get_permissions(self):
        """
        Role-based permissions for disciplinary record management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_create', 'resolve', 'assign_action']:
            # Teachers and staff/admins can create/manage disciplinary records
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['statistics']:
            # Only staff/admins can access aggregated discipline statistics
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [CanAccessDiscipline]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DisciplinaryRecordDetailSerializer
        elif self.action == 'bulk_create':
            return BulkRecordSerializer
        return DisciplinaryRecordSerializer

    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = DisciplinaryRecord.objects.select_related(
            'student', 'infraction_type', 'action_taken', 'reported_by'
        ).all()
        user = self.request.user
        
        # Admin users and staff can see all records
        if user.is_staff or user.is_superuser:
            pass  # Return all records
        else:
            try:
                user_profile = user.userprofile
                
                # Staff can see all records
                if user_profile.user_type == 'staff':
                    pass  # Return all records
                
                # Teachers can see records for their students and records they reported
                elif user_profile.user_type == 'teacher':
                    try:
                        teacher = user.teacher
                        # Get students from teacher's courses
                        student_ids = []
                        for course in teacher.courses_taught.all():
                            course_student_ids = course.enrollments.filter(
                                is_active=True
                            ).values_list('student_id', flat=True)
                            student_ids.extend(course_student_ids)
                        
                        # Filter records for teacher's students or records they reported
                        queryset = queryset.filter(
                            Q(student__student__in=student_ids) |
                            Q(reported_by=teacher)
                        )
                    except:
                        queryset = queryset.none()
                
                # Students can only see their own records
                elif user_profile.user_type == 'student':
                    try:
                        student = user.student
                        queryset = queryset.filter(student=student)
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
        
        # Filter by severity
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(infraction_type__severity=severity)
        
        return queryset

    @action(detail=False, methods=['get'])
    def unresolved(self, request):
        """Get unresolved disciplinary records"""
        unresolved_records = self.queryset.filter(resolved=False)
        
        # Sort by date (oldest first for priority)
        unresolved_records = unresolved_records.order_by('date')
        
        serializer = DisciplinaryRecordDetailSerializer(unresolved_records, many=True)
        
        return Response({
            'unresolved_records': serializer.data,
            'total_unresolved': unresolved_records.count()
        })

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue disciplinary records (unresolved for more than 7 days)"""
        cutoff_date = timezone.now().date() - timedelta(days=7)
        overdue_records = self.queryset.filter(
            resolved=False,
            date__lt=cutoff_date
        ).order_by('date')
        
        serializer = DisciplinaryRecordDetailSerializer(overdue_records, many=True)
        
        return Response({
            'overdue_records': serializer.data,
            'total_overdue': overdue_records.count(),
            'cutoff_date': cutoff_date.isoformat()
        })

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple disciplinary records at once"""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            records = serializer.save()
            return Response({
                'status': 'Records created successfully',
                'created_count': len(records),
                'student_count': len(serializer.validated_data['student_ids'])
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark a disciplinary record as resolved"""
        record = self.get_object()
        resolution_notes = request.data.get('resolution_notes', '')
        
        record.resolved = True
        record.resolution_notes = resolution_notes
        record.save(update_fields=['resolved', 'resolution_notes'])
        
        serializer = DisciplinaryRecordDetailSerializer(record)
        return Response({
            'status': 'Record marked as resolved',
            'record': serializer.data
        })

    @action(detail=True, methods=['post'])
    def assign_action(self, request, pk=None):
        """Assign disciplinary action to a record"""
        record = self.get_object()
        action_id = request.data.get('action_id')
        action_date = request.data.get('action_date')
        
        if not action_id:
            return Response(
                {'error': 'action_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            action = DisciplinaryAction.objects.get(id=action_id)
        except DisciplinaryAction.DoesNotExist:
            return Response(
                {'error': 'Invalid action_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        record.action_taken = action
        if action_date:
            try:
                record.action_date = datetime.strptime(action_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            record.action_date = timezone.now().date()
        
        record.save(update_fields=['action_taken', 'action_date'])
        
        serializer = DisciplinaryRecordDetailSerializer(record)
        return Response({
            'status': 'Action assigned successfully',
            'record': serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get disciplinary records for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        records = self.queryset.filter(student_id=student_id)
        serializer = DisciplinaryRecordDetailSerializer(records, many=True)
        
        # Calculate student statistics
        total_records = records.count()
        resolved_records = records.filter(resolved=True).count()
        severe_infractions = records.filter(infraction_type__severity=3).count()
        recent_records = records.filter(date__gte=timezone.now().date() - timedelta(days=30)).count()
        
        return Response({
            'student_id': student_id,
            'records': serializer.data,
            'statistics': {
                'total_records': total_records,
                'resolved_records': resolved_records,
                'unresolved_records': total_records - resolved_records,
                'severe_infractions': severe_infractions,
                'recent_records': recent_records
            }
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get overall disciplinary statistics"""
        # Date range filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.queryset
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        total_records = queryset.count()
        resolved_records = queryset.filter(resolved=True).count()
        unresolved_records = total_records - resolved_records
        overdue_records = queryset.filter(
            resolved=False,
            date__lt=timezone.now().date() - timedelta(days=7)
        ).count()
        
        # Severity distribution
        severity_dist = queryset.values('infraction_type__severity').annotate(
            count=Count('id')
        ).order_by('infraction_type__severity')
        
        # Most common infractions
        common_infractions = queryset.values('infraction_type__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Monthly trends
        monthly_trends = queryset.extra(
            select={'month': "strftime('%%Y-%%m', date)"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        return Response({
            'statistics': {
                'total_records': total_records,
                'resolved_records': resolved_records,
                'unresolved_records': unresolved_records,
                'overdue_records': overdue_records,
                'resolution_rate': (resolved_records / total_records * 100) if total_records > 0 else 0
            },
            'severity_distribution': list(severity_dist),
            'most_common_infractions': list(common_infractions),
            'monthly_trends': list(monthly_trends),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        })


class BehaviorNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing behavior notes with role-based permissions
    - Admins/Staff: Full access to all behavior notes
    - Teachers: Can create/view notes for their students
    - Students: Can view their own behavior notes only
    """
    queryset = BehaviorNote.objects.select_related('student', 'noted_by').all()
    serializer_class = BehaviorNoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'noted_by']
    search_fields = ['student__user__username', 'student__user__first_name', 'student__user__last_name', 'note']
    ordering_fields = ['date', 'student']
    ordering = ['-date']
    
    def get_permissions(self):
        """
        Role-based permissions for behavior note management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Teachers and staff/admins can create/manage behavior notes
            permission_classes = [IsTeacherOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [CanAccessDiscipline]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = BehaviorNote.objects.select_related('student', 'noted_by').all()
        user = self.request.user
        
        # Admin users and staff can see all notes
        if user.is_staff or user.is_superuser:
            pass  # Return all notes
        else:
            try:
                user_profile = user.userprofile
                
                # Staff can see all notes
                if user_profile.user_type == 'staff':
                    pass  # Return all notes
                
                # Teachers can see notes for their students and notes they created
                elif user_profile.user_type == 'teacher':
                    try:
                        teacher = user.teacher
                        # Get students from teacher's courses
                        student_ids = []
                        for course in teacher.courses_taught.all():
                            course_student_ids = course.enrollments.filter(
                                is_active=True
                            ).values_list('student_id', flat=True)
                            student_ids.extend(course_student_ids)
                        
                        # Filter notes for teacher's students or notes they created
                        queryset = queryset.filter(
                            Q(student__student__in=student_ids) |
                            Q(noted_by=teacher)
                        )
                    except:
                        queryset = queryset.none()
                
                # Students can only see their own notes
                elif user_profile.user_type == 'student':
                    try:
                        student = user.student
                        queryset = queryset.filter(student=student)
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
        
        return queryset

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get behavior notes for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        notes = self.queryset.filter(student_id=student_id)
        serializer = BehaviorNoteSerializer(notes, many=True)
        
        return Response({
            'student_id': student_id,
            'notes': serializer.data,
            'total_notes': notes.count()
        })

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent behavior notes"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)
        
        recent_notes = self.queryset.filter(date__gte=start_date)
        serializer = BehaviorNoteSerializer(recent_notes, many=True)
        
        return Response({
            'recent_notes': serializer.data,
            'period_days': days,
            'total_recent': recent_notes.count()
        })
