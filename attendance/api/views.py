from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta, date
from collections import defaultdict
from django.contrib.auth import get_user_model
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, IsTeacherOrAdmin,
    IsStudentOrTeacherOrAdmin, CanAccessAttendance
)

from ..models import Attendance, AttendanceReport, SchoolCalendar
from .serializers import (
    AttendanceSerializer, AttendanceReportSerializer, SchoolCalendarSerializer,
    AttendanceDetailSerializer, AttendanceStatsSerializer
)

User = get_user_model()


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing attendance records with role-based permissions
    - Admins/Staff: Full access to all attendance records
    - Teachers: Can view/mark attendance for their students
    - Students: Can view their own attendance records only
    """
    queryset = Attendance.objects.select_related('student').all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'date', 'is_present']
    search_fields = ['student__username', 'student__first_name', 'student__last_name']
    ordering_fields = ['date', 'student', 'is_present']
    ordering = ['-date']
    
    def get_permissions(self):
        """
        Role-based permissions for attendance management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_mark']:
            # Teachers and staff/admins can create/update attendance records
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['low_attendance_alerts', 'statistics', 'trends']:
            # Only staff/admins can access aggregated attendance data
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [CanAccessAttendance]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AttendanceDetailSerializer
        return AttendanceSerializer

    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = Attendance.objects.select_related('student').all()
        user = self.request.user
        
        # Admin users and staff can see all attendance records
        if user.is_staff or user.is_superuser:
            pass  # Return all records
        else:
            try:
                user_profile = user.userprofile
                
                # Staff can see all attendance records
                if user_profile.user_type == 'staff':
                    pass  # Return all records
                
                # Teachers can see attendance for their students
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
                        
                        # Filter attendance records for these students
                        queryset = queryset.filter(student__student__in=student_ids)
                    except:
                        queryset = queryset.none()
                
                # Students can only see their own attendance records
                elif user_profile.user_type == 'student':
                    try:
                        queryset = queryset.filter(student=user)
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
        
        # Filter by class (if student is part of a class)
        class_id = self.request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(student__student__class_group_id=class_id)
            queryset = queryset.filter(student__student__class_group_id=class_id)
        
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Mark attendance for multiple students at once"""
        date_str = request.data.get('date')
        students_data = request.data.get('students', [])
        
        if not date_str or not students_data:
            return Response(
                {'error': 'date and students data are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_attendances = []
        updated_attendances = []
        errors = []
        
        for student_data in students_data:
            student_id = student_data.get('student_id')
            is_present = student_data.get('is_present', False)
            
            if not student_id:
                errors.append('Missing student_id in student data')
                continue
            
            try:
                attendance, created = Attendance.objects.update_or_create(
                    student_id=student_id,
                    date=attendance_date,
                    defaults={'is_present': is_present}
                )
                
                if created:
                    created_attendances.append(AttendanceDetailSerializer(attendance).data)
                else:
                    updated_attendances.append(AttendanceDetailSerializer(attendance).data)
                    
                # Check for low attendance
                Attendance.check_low_attendance(attendance.student)
                
            except Exception as e:
                errors.append(f"Error for student {student_id}: {str(e)}")
        
        return Response({
            'created_attendances': created_attendances,
            'updated_attendances': updated_attendances,
            'total_created': len(created_attendances),
            'total_updated': len(updated_attendances),
            'errors': errors,
            'date': date_str
        })

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get attendance records for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendances = self.queryset.filter(student_id=student_id)
        
        # Apply date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            attendances = attendances.filter(date__gte=start_date)
        if end_date:
            attendances = attendances.filter(date__lte=end_date)
        
        serializer = AttendanceDetailSerializer(attendances, many=True)
        
        # Calculate statistics
        total_days = attendances.count()
        present_days = attendances.filter(is_present=True).count()
        absent_days = total_days - present_days
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        return Response({
            'student_id': student_id,
            'attendances': serializer.data,
            'statistics': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'attendance_percentage': round(attendance_percentage, 2)
            }
        })

    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """Get attendance records for a specific date"""
        date_str = request.query_params.get('date')
        if not date_str:
            return Response(
                {'error': 'date parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendances = self.queryset.filter(date=attendance_date)
        serializer = AttendanceDetailSerializer(attendances, many=True)
        
        # Calculate daily statistics
        total_students = attendances.count()
        present_students = attendances.filter(is_present=True).count()
        absent_students = total_students - present_students
        daily_attendance_rate = (present_students / total_students * 100) if total_students > 0 else 0
        
        return Response({
            'date': date_str,
            'attendances': serializer.data,
            'daily_statistics': {
                'total_students': total_students,
                'present_students': present_students,
                'absent_students': absent_students,
                'attendance_rate': round(daily_attendance_rate, 2)
            }
        })

    @action(detail=False, methods=['get'])
    def low_attendance_alerts(self, request):
        """Get students with low attendance"""
        threshold = float(request.query_params.get('threshold', 0.75))
        days_back = int(request.query_params.get('days', 30))
        
        start_date = timezone.now().date() - timedelta(days=days_back)
        
        # Get all students with attendance records in the period
        students_with_low_attendance = []
        
        for user in User.objects.all():
            attendances = self.queryset.filter(
                student=user, 
                date__gte=start_date
            )
            
            total_days = attendances.count()
            present_days = attendances.filter(is_present=True).count()
            
            if total_days > 0:
                attendance_rate = present_days / total_days
                if attendance_rate < threshold:
                    students_with_low_attendance.append({
                        'student_id': user.id,
                        'student_name': user.get_full_name() or user.username,
                        'total_days': total_days,
                        'present_days': present_days,
                        'attendance_rate': round(attendance_rate * 100, 2),
                        'threshold': threshold * 100
                    })
        
        return Response({
            'low_attendance_students': students_with_low_attendance,
            'threshold_percentage': threshold * 100,
            'period_days': days_back,
            'start_date': start_date.isoformat(),
            'total_flagged': len(students_with_low_attendance)
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get overall attendance statistics"""
        # Date range filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.queryset
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        total_records = queryset.count()
        present_records = queryset.filter(is_present=True).count()
        absent_records = total_records - present_records
        
        overall_attendance_rate = (present_records / total_records * 100) if total_records > 0 else 0
        
        # Daily attendance rates for the period
        daily_stats = queryset.values('date').annotate(
            total=Count('id'),
            present=Count('id', filter=Q(is_present=True))
        ).order_by('date')
        
        for day in daily_stats:
            day['attendance_rate'] = (day['present'] / day['total'] * 100) if day['total'] > 0 else 0
            day['date'] = day['date'].isoformat()
        
        # Monthly statistics
        monthly_stats = queryset.extra(
            select={'month': "strftime('%%Y-%%m', date)"}
        ).values('month').annotate(
            total=Count('id'),
            present=Count('id', filter=Q(is_present=True))
        ).order_by('month')
        
        for month in monthly_stats:
            month['attendance_rate'] = (month['present'] / month['total'] * 100) if month['total'] > 0 else 0
        
        return Response({
            'overall_statistics': {
                'total_records': total_records,
                'present_records': present_records,
                'absent_records': absent_records,
                'overall_attendance_rate': round(overall_attendance_rate, 2)
            },
            'daily_statistics': list(daily_stats),
            'monthly_statistics': list(monthly_stats),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        })

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get attendance trends over time"""
        days_back = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days_back)
        
        # Get daily attendance rates for the period
        daily_trends = []
        current_date = start_date
        end_date = timezone.now().date()
        
        while current_date <= end_date:
            day_attendances = self.queryset.filter(date=current_date)
            total = day_attendances.count()
            present = day_attendances.filter(is_present=True).count()
            rate = (present / total * 100) if total > 0 else 0
            
            daily_trends.append({
                'date': current_date.isoformat(),
                'total_students': total,
                'present_students': present,
                'attendance_rate': round(rate, 2)
            })
            
            current_date += timedelta(days=1)
        
        # Calculate trend direction
        if len(daily_trends) >= 2:
            recent_avg = sum([d['attendance_rate'] for d in daily_trends[-7:]]) / min(7, len(daily_trends))
            older_avg = sum([d['attendance_rate'] for d in daily_trends[:-7]]) / max(1, len(daily_trends) - 7)
            trend_direction = 'improving' if recent_avg > older_avg else 'declining' if recent_avg < older_avg else 'stable'
        else:
            trend_direction = 'insufficient_data'
        
        return Response({
            'daily_trends': daily_trends,
            'trend_analysis': {
                'direction': trend_direction,
                'recent_average': round(recent_avg, 2) if len(daily_trends) >= 2 else 0,
                'period_days': days_back
            }
        })


class AttendanceReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing attendance reports with role-based permissions
    - Admins/Staff: Full access to all attendance reports
    - Teachers: Can view/generate reports for their students
    - Students: Can view their own attendance reports only
    """
    queryset = AttendanceReport.objects.select_related('student').all()
    serializer_class = AttendanceReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'start_date', 'end_date']
    search_fields = ['student__username', 'student__first_name', 'student__last_name']
    ordering_fields = ['start_date', 'end_date', 'total_days', 'days_present']
    ordering = ['-start_date']
    
    def get_permissions(self):
        """
        Role-based permissions for attendance report management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'generate_report']:
            # Teachers and staff/admins can create/update reports
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['class_summary']:
            # Only staff/admins can access class summaries
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [CanAccessAttendance]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = AttendanceReport.objects.select_related('student').all()
        user = self.request.user
        
        # Admin users and staff can see all reports
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all reports
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see reports for their students
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
                    
                    # Filter reports for these students
                    return queryset.filter(student__student__in=student_ids)
                except:
                    return queryset.none()
            
            # Students can only see their own reports
            elif user_profile.user_type == 'student':
                try:
                    return queryset.filter(student=user)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()

    @action(detail=False, methods=['post'])
    def generate_report(self, request):
        """Generate a new attendance report"""
        student_id = request.data.get('student_id')
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')
        
        if not all([student_id, start_date_str, end_date_str]):
            return Response(
                {'error': 'student_id, start_date, and end_date are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            student = User.objects.get(id=student_id)
        except (ValueError, User.DoesNotExist) as e:
            return Response(
                {'error': f'Invalid data: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get attendance records for the period
        attendances = Attendance.objects.filter(
            student=student,
            date__range=[start_date, end_date]
        )
        
        total_days = (end_date - start_date).days + 1
        days_present = attendances.filter(is_present=True).count()
        
        # Create or update report
        report, created = AttendanceReport.objects.update_or_create(
            student=student,
            start_date=start_date,
            end_date=end_date,
            defaults={
                'total_days': total_days,
                'days_present': days_present
            }
        )
        
        serializer = AttendanceReportSerializer(report)
        
        return Response({
            'report': serializer.data,
            'created': created,
            'attendance_percentage': (days_present / total_days * 100) if total_days > 0 else 0
        })

    @action(detail=False, methods=['get'])
    def class_summary(self, request):
        """Get attendance summary for all students in a class"""
        class_id = request.query_params.get('class_id')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        if not all([class_id, start_date_str, end_date_str]):
            return Response(
                {'error': 'class_id, start_date, and end_date are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all students in the class (assuming relationship exists)
        student_summaries = []
        
        # This would need to be adjusted based on your actual class-student relationship
        # For now, getting all students with attendance in the period
        students_with_attendance = Attendance.objects.filter(
            date__range=[start_date, end_date]
        ).values_list('student', flat=True).distinct()
        
        for student_id in students_with_attendance:
            student = User.objects.get(id=student_id)
            attendances = Attendance.objects.filter(
                student=student,
                date__range=[start_date, end_date]
            )
            
            total_days = (end_date - start_date).days + 1
            days_present = attendances.filter(is_present=True).count()
            attendance_rate = (days_present / total_days * 100) if total_days > 0 else 0
            
            student_summaries.append({
                'student_id': student.id,
                'student_name': student.get_full_name() or student.username,
                'total_days': total_days,
                'days_present': days_present,
                'attendance_rate': round(attendance_rate, 2)
            })
        
        # Sort by attendance rate (lowest first for attention)
        student_summaries.sort(key=lambda x: x['attendance_rate'])
        
        return Response({
            'class_id': class_id,
            'period': {
                'start_date': start_date_str,
                'end_date': end_date_str
            },
            'student_summaries': student_summaries,
            'class_statistics': {
                'total_students': len(student_summaries),
                'average_attendance_rate': sum([s['attendance_rate'] for s in student_summaries]) / len(student_summaries) if student_summaries else 0
            }
        })


class SchoolCalendarViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school calendar with role-based permissions
    - Admins/Staff: Full access to manage calendar events and holidays
    - Teachers: Can view all calendar events, create announcements
    - Students: Can view calendar events and holidays only
    """
    queryset = SchoolCalendar.objects.all()
    serializer_class = SchoolCalendarSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_holiday']
    ordering_fields = ['date']
    ordering = ['date']
    
    def get_permissions(self):
        """
        Role-based permissions for school calendar management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only staff/admins can create/modify calendar events
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view calendar
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset

    @action(detail=False, methods=['get'])
    def holidays(self, request):
        """Get only holiday dates"""
        holidays = self.queryset.filter(is_holiday=True)
        serializer = self.get_serializer(holidays, many=True)
        return Response({
            'holidays': serializer.data,
            'total_holidays': holidays.count()
        })

    @action(detail=False, methods=['get'])
    def working_days(self, request):
        """Get working days for a date range"""
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        if not start_date_str or not end_date_str:
            return Response(
                {'error': 'start_date and end_date parameters are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get holidays in the range
        holidays = self.queryset.filter(
            date__range=[start_date, end_date],
            is_holiday=True
        ).values_list('date', flat=True)
        
        # Calculate working days
        total_days = (end_date - start_date).days + 1
        holiday_count = len(holidays)
        working_days = total_days - holiday_count
        
        return Response({
            'period': {
                'start_date': start_date_str,
                'end_date': end_date_str
            },
            'total_days': total_days,
            'holidays': holiday_count,
            'working_days': working_days,
            'holiday_dates': [h.isoformat() for h in holidays]
        })

    @action(detail=False, methods=['get'])
    def upcoming_events(self, request):
        """Get upcoming events"""
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=days)
        
        events = self.queryset.filter(
            date__range=[start_date, end_date]
        ).exclude(event_name__isnull=True).exclude(event_name='')
        
        serializer = self.get_serializer(events, many=True)
        
        return Response({
            'upcoming_events': serializer.data,
            'period_days': days,
            'total_events': events.count()
        })
