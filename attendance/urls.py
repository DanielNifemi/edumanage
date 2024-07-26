from django.urls import path
from . import views

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('bulk-mark/', views.bulk_mark_attendance, name='bulk_mark_attendance'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('list/', views.attendance_list, name='attendance_list'),
    path('calendar/', views.manage_school_calendar, name='manage_school_calendar'),
]