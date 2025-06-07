from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, SubjectViewSet, ClassViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
