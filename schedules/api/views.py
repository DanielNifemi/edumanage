from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, IsTeacherOrAdmin,
    IsStudentOrTeacherOrAdmin, CanAccessSchedules
)

from ..models import Schedule, TimeSlot, DayOfWeek, Event
from .serializers import (
    ScheduleSerializer, ScheduleDetailSerializer, TimeSlotSerializer,
    DayOfWeekSerializer, EventSerializer, WeeklyScheduleSerializer,
    TimetableSerializer
)


class TimeSlotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing time slots with role-based permissions
    - Admins/Staff: Full access to manage time slots
    - Teachers: Can view time slots
    - Students: Can view time slots
    """
    queryset = TimeSlot.objects.all().order_by('start_time')
    serializer_class = TimeSlotSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['start_time', 'end_time']
    ordering = ['start_time']
    
    def get_permissions(self):
        """
        Role-based permissions for time slot management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only staff/admins can create/modify time slots
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view time slots
            permission_classes = [CanAccessSchedules]
        
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        """Get available time slots for a specific day and class"""
        day_id = request.query_params.get('day')
        class_id = request.query_params.get('class_id')
        
        if not day_id or not class_id:
            return Response(
                {'error': 'day and class_id parameters are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all time slots
        all_slots = TimeSlot.objects.all()
        
        # Get occupied slots for the day and class
        occupied_slots = Schedule.objects.filter(
            day_id=day_id,
            class_group_id=class_id
        ).values_list('time_slot_id', flat=True)
        
        # Filter available slots
        available_slots = all_slots.exclude(id__in=occupied_slots)
        serializer = self.get_serializer(available_slots, many=True)
        
        return Response({
            'available_slots': serializer.data,
            'total_slots': all_slots.count(),
            'occupied_slots': len(occupied_slots),
            'available_count': available_slots.count()
        })

    @action(detail=False, methods=['get'])
    def peak_hours(self, request):
        """Get statistics about peak usage hours"""
        slot_usage = TimeSlot.objects.annotate(
            usage_count=Count('schedule')
        ).order_by('-usage_count')
        
        serializer = self.get_serializer(slot_usage, many=True)
        
        # Add usage statistics
        for item in serializer.data:
            slot = TimeSlot.objects.get(id=item['id'])
            item['usage_count'] = slot.schedule_set.count()
        
        return Response({
            'peak_hours': serializer.data,
            'total_slots': slot_usage.count()
        })


class DayOfWeekViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing days of week with role-based permissions
    - Admins/Staff: Full access to manage days
    - Teachers: Can view days
    - Students: Can view days
    """
    queryset = DayOfWeek.objects.all().order_by('day')
    serializer_class = DayOfWeekSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['day']
    ordering = ['day']
    
    def get_permissions(self):
        """
        Role-based permissions for day management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only staff/admins can create/modify days
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view days
            permission_classes = [CanAccessSchedules]
        
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def working_days(self, request):
        """Get only working days (Monday to Friday)"""
        working_days = self.queryset.filter(day__lt=5)  # 0-4 are Monday to Friday
        serializer = self.get_serializer(working_days, many=True)
        return Response(serializer.data)


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing class schedules with role-based permissions
    - Admins/Staff: Full access to all schedules
    - Teachers: Can view their own schedules and schedules for their classes
    - Students: Can view schedules for their enrolled classes
    """
    queryset = Schedule.objects.select_related(
        'class_group', 'day', 'time_slot', 'subject', 'teacher__user'
    ).all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['class_group', 'day', 'subject', 'teacher']
    search_fields = ['class_group__name', 'subject__name', 'teacher__user__first_name', 'teacher__user__last_name']
    ordering_fields = ['day', 'time_slot', 'class_group', 'subject']
    ordering = ['day__day', 'time_slot__start_time']
    
    def get_permissions(self):
        """
        Role-based permissions for schedule management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_create']:
            # Teachers and staff/admins can create/modify schedules
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['conflicts', 'statistics']:
            # Only staff/admins can access schedule analysis
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view (with queryset filtering)
            permission_classes = [CanAccessSchedules]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScheduleDetailSerializer
        return ScheduleSerializer

    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        queryset = Schedule.objects.select_related(
            'class_group', 'day', 'time_slot', 'subject', 'teacher__user'
        ).all()
        user = self.request.user
        
        # Admin users and staff can see all schedules
        if user.is_staff or user.is_superuser:
            return queryset
        
        try:
            user_profile = user.userprofile
            
            # Staff can see all schedules
            if user_profile.user_type == 'staff':
                return queryset
            
            # Teachers can see their own schedules and schedules for their classes
            elif user_profile.user_type == 'teacher':
                try:
                    teacher = user.teacher
                    # Get teacher's courses and subjects
                    teacher_courses = teacher.courses_taught.all()
                    teacher_subjects = teacher.subjects.all()
                    
                    return queryset.filter(
                        Q(teacher=teacher) |
                        Q(subject__in=teacher_subjects) |
                        Q(class_group__in=[course.class_group for course in teacher_courses if hasattr(course, 'class_group')])
                    )
                except:
                    return queryset.none()
            
            # Students can see schedules for their enrolled classes
            elif user_profile.user_type == 'student':
                try:
                    student = user.student
                    # Get student's enrolled courses and their classes
                    enrolled_courses = student.enrollments.filter(is_active=True)
                    class_groups = [enrollment.course.class_group for enrollment in enrolled_courses if hasattr(enrollment.course, 'class_group')]
                    
                    return queryset.filter(class_group__in=class_groups)
                except:
                    return queryset.none()
            
        except:
            pass
        
        # Default: no access
        return queryset.none()

    @action(detail=False, methods=['get'])
    def by_class(self, request):
        """Get schedule for a specific class"""
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response(
                {'error': 'class_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedules = self.queryset.filter(class_group_id=class_id)
        serializer = ScheduleDetailSerializer(schedules, many=True)
        
        return Response({
            'class_id': class_id,
            'schedules': serializer.data,
            'total_periods': schedules.count()
        })

    @action(detail=False, methods=['get'])
    def by_teacher(self, request):
        """Get schedule for a specific teacher"""
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response(
                {'error': 'teacher_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedules = self.queryset.filter(teacher_id=teacher_id)
        serializer = ScheduleDetailSerializer(schedules, many=True)
        
        return Response({
            'teacher_id': teacher_id,
            'schedules': serializer.data,
            'total_periods': schedules.count()
        })

    @action(detail=False, methods=['get'])
    def weekly_timetable(self, request):
        """Get weekly timetable view"""
        class_id = request.query_params.get('class_id')
        teacher_id = request.query_params.get('teacher_id')
        
        queryset = self.queryset
        if class_id:
            queryset = queryset.filter(class_group_id=class_id)
        elif teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # Organize data by days
        timetable = defaultdict(list)
        days = DayOfWeek.objects.all().order_by('day')
        time_slots = TimeSlot.objects.all().order_by('start_time')
        
        for day in days:
            day_schedules = queryset.filter(day=day).order_by('time_slot__start_time')
            timetable[day.get_day_display()] = ScheduleDetailSerializer(day_schedules, many=True).data
        
        return Response({
            'timetable': dict(timetable),
            'time_slots': TimeSlotSerializer(time_slots, many=True).data,
            'days': DayOfWeekSerializer(days, many=True).data
        })

    @action(detail=False, methods=['get'])
    def conflicts(self, request):
        """Check for scheduling conflicts"""
        conflicts = []
        
        # Check for teacher conflicts (same teacher, same time, different classes)
        teacher_conflicts = Schedule.objects.values(
            'teacher', 'day', 'time_slot'
        ).annotate(
            class_count=Count('class_group', distinct=True)
        ).filter(class_count__gt=1)
        
        for conflict in teacher_conflicts:
            conflicting_schedules = Schedule.objects.filter(
                teacher_id=conflict['teacher'],
                day_id=conflict['day'],
                time_slot_id=conflict['time_slot']
            ).select_related('class_group', 'teacher__user', 'subject')
            
            conflicts.append({
                'type': 'teacher_conflict',
                'teacher': conflicting_schedules.first().teacher.user.get_full_name(),
                'day': conflicting_schedules.first().day.get_day_display(),
                'time_slot': str(conflicting_schedules.first().time_slot),
                'conflicting_classes': [s.class_group.name for s in conflicting_schedules]
            })
        
        return Response({
            'conflicts': conflicts,
            'total_conflicts': len(conflicts)
        })

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple schedules at once"""
        schedules_data = request.data.get('schedules', [])
        
        if not schedules_data:
            return Response(
                {'error': 'schedules data is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_schedules = []
        errors = []
        
        for schedule_data in schedules_data:
            serializer = ScheduleSerializer(data=schedule_data)
            if serializer.is_valid():
                try:
                    schedule = serializer.save()
                    created_schedules.append(ScheduleDetailSerializer(schedule).data)
                except Exception as e:
                    errors.append(f"Error creating schedule: {str(e)}")
            else:
                errors.append(serializer.errors)
        
        return Response({
            'created_schedules': created_schedules,
            'total_created': len(created_schedules),
            'errors': errors,
            'success_rate': len(created_schedules) / len(schedules_data) * 100 if schedules_data else 0
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get schedule statistics"""
        total_schedules = self.queryset.count()
        
        # Schedules by day
        schedules_by_day = {}
        for day in DayOfWeek.objects.all():
            count = self.queryset.filter(day=day).count()
            schedules_by_day[day.get_day_display()] = count
        
        # Schedules by time slot
        schedules_by_time = {}
        for slot in TimeSlot.objects.all():
            count = self.queryset.filter(time_slot=slot).count()
            schedules_by_time[str(slot)] = count
        
        # Teacher workload
        teacher_workload = self.queryset.values(
            'teacher__user__first_name', 'teacher__user__last_name'
        ).annotate(
            period_count=Count('id')
        ).order_by('-period_count')[:10]
        
        return Response({
            'total_schedules': total_schedules,
            'schedules_by_day': schedules_by_day,
            'schedules_by_time': schedules_by_time,
            'top_teachers_by_workload': list(teacher_workload),
            'average_periods_per_day': total_schedules / 5 if total_schedules > 0 else 0  # Assuming 5 working days
        })


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing events with role-based permissions
    - Admins/Staff: Full access to all events
    - Teachers: Can create/view events and school announcements
    - Students: Can view events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_datetime', 'end_datetime', 'title']
    ordering = ['start_datetime']
    
    def get_permissions(self):
        """
        Role-based permissions for event management
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_create']:
            # Teachers and staff/admins can create/modify events
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['statistics']:
            # Only staff/admins can access event statistics
            permission_classes = [IsStaffOrAdmin]
        else:
            # All authenticated users can view events
            permission_classes = [CanAccessSchedules]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filter events based on user permissions"""
        queryset = Event.objects.all()
        user = self.request.user
        
        # Admin users and staff can see all events
        if user.is_staff or user.is_superuser:
            pass  # Return all events
        else:
            try:
                user_profile = user.userprofile
                
                # Staff can see all events
                if user_profile.user_type == 'staff':
                    pass  # Return all events
                
                # Teachers and students can see all public events
                # (assuming all events are public for now - you can add visibility logic here)
                
            except:
                pass
        
        # Apply additional filters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(start_datetime__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_datetime__lte=end_date)
        
        # Filter upcoming/past events
        time_filter = self.request.query_params.get('time_filter')
        if time_filter == 'upcoming':
            queryset = queryset.filter(start_datetime__gt=timezone.now())
        elif time_filter == 'past':
            queryset = queryset.filter(end_datetime__lt=timezone.now())
        elif time_filter == 'current':
            now = timezone.now()
            queryset = queryset.filter(start_datetime__lte=now, end_datetime__gte=now)
        
        return queryset

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now()
        end_date = start_date + timedelta(days=days)
        
        events = self.queryset.filter(
            start_datetime__gte=start_date,
            start_datetime__lte=end_date
        ).order_by('start_datetime')
        
        serializer = self.get_serializer(events, many=True)
        
        return Response({
            'upcoming_events': serializer.data,
            'period_days': days,
            'total_events': events.count()
        })

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's events"""
        today = timezone.now().date()
        events = self.queryset.filter(
            start_datetime__date=today
        ).order_by('start_datetime')
        
        serializer = self.get_serializer(events, many=True)
        
        return Response({
            'todays_events': serializer.data,
            'date': today.isoformat(),
            'total_events': events.count()
        })

    @action(detail=False, methods=['get'])
    def calendar_view(self, request):
        """Get events in calendar format for a specific month"""
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        # Get events for the month
        events = self.queryset.filter(
            start_datetime__year=year,
            start_datetime__month=month
        ).order_by('start_datetime')
        
        # Group events by date
        calendar_data = defaultdict(list)
        for event in events:
            date_key = event.start_datetime.date().isoformat()
            calendar_data[date_key].append(EventSerializer(event).data)
        
        return Response({
            'calendar': dict(calendar_data),
            'year': year,
            'month': month,
            'total_events': events.count()
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get event statistics"""
        total_events = self.queryset.count()
        
        # Events by month
        events_by_month = self.queryset.extra(
            select={'month': "strftime('%%Y-%%m', start_datetime)"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        # Average event duration
        events_with_duration = self.queryset.exclude(
            end_datetime__isnull=True
        )
        
        total_duration = sum([
            (event.end_datetime - event.start_datetime).total_seconds() / 3600
            for event in events_with_duration
        ])
        
        avg_duration = total_duration / events_with_duration.count() if events_with_duration.count() > 0 else 0
        
        # Events by location
        events_by_location = self.queryset.exclude(
            location=''
        ).values('location').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'total_events': total_events,
            'events_by_month': list(events_by_month),
            'average_duration_hours': round(avg_duration, 2),
            'events_by_location': list(events_by_location),
            'upcoming_events_count': self.queryset.filter(
                start_datetime__gt=timezone.now()
            ).count()
        })

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple events at once"""
        events_data = request.data.get('events', [])
        
        if not events_data:
            return Response(
                {'error': 'events data is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_events = []
        errors = []
        
        for event_data in events_data:
            serializer = EventSerializer(data=event_data)
            if serializer.is_valid():
                try:
                    event = serializer.save()
                    created_events.append(EventSerializer(event).data)
                except Exception as e:
                    errors.append(f"Error creating event: {str(e)}")
            else:
                errors.append(serializer.errors)
        
        return Response({
            'created_events': created_events,
            'total_created': len(created_events),
            'errors': errors,
            'success_rate': len(created_events) / len(events_data) * 100 if events_data else 0
        })
