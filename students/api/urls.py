from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, AcademicRecordViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'academic-records', AcademicRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]