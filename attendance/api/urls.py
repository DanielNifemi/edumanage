from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, AttendanceReportViewSet, SchoolCalendarViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet)
router.register(r'reports', AttendanceReportViewSet)
router.register(r'calendar', SchoolCalendarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
