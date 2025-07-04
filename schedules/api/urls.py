from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, TimeSlotViewSet, DayOfWeekViewSet, EventViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'time-slots', TimeSlotViewSet, basename='timeslot')
router.register(r'days', DayOfWeekViewSet, basename='dayofweek')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    
    # Custom endpoints
    path('schedules/by-class/', ScheduleViewSet.as_view({'get': 'by_class'}), name='schedule-by-class'),
    path('schedules/by-teacher/', ScheduleViewSet.as_view({'get': 'by_teacher'}), name='schedule-by-teacher'),
    path('schedules/weekly-timetable/', ScheduleViewSet.as_view({'get': 'weekly_timetable'}), name='schedule-weekly-timetable'),
    path('schedules/conflicts/', ScheduleViewSet.as_view({'get': 'conflicts'}), name='schedule-conflicts'),
    path('schedules/bulk-create/', ScheduleViewSet.as_view({'post': 'bulk_create'}), name='schedule-bulk-create'),
    path('schedules/statistics/', ScheduleViewSet.as_view({'get': 'statistics'}), name='schedule-statistics'),
    
    path('time-slots/available-slots/', TimeSlotViewSet.as_view({'get': 'available_slots'}), name='timeslot-available'),
    path('time-slots/peak-hours/', TimeSlotViewSet.as_view({'get': 'peak_hours'}), name='timeslot-peak-hours'),
    
    path('days/working-days/', DayOfWeekViewSet.as_view({'get': 'working_days'}), name='dayofweek-working-days'),
    
    path('events/upcoming/', EventViewSet.as_view({'get': 'upcoming'}), name='event-upcoming'),
    path('events/today/', EventViewSet.as_view({'get': 'today'}), name='event-today'),
    path('events/calendar-view/', EventViewSet.as_view({'get': 'calendar_view'}), name='event-calendar-view'),
    path('api/events/bulk-create/', EventViewSet.as_view({'post': 'bulk_create'}), name='event-bulk-create'),
    path('api/events/statistics/', EventViewSet.as_view({'get': 'statistics'}), name='event-statistics'),
]
