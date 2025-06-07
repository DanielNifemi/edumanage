from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StaffProfileViewSet, DepartmentViewSet, RoleViewSet,
    LeaveRequestViewSet, PerformanceEvaluationViewSet
)

router = DefaultRouter()
router.register(r'staff', StaffProfileViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'evaluations', PerformanceEvaluationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
