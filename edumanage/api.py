from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework import permissions

# Create schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="EduManage API",
        default_version='v1',
        description="API for EduManage System",
        contact=openapi.Contact(email="contact@edumanage.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# API URLs patterns
urlpatterns = [    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('auth/', include('accounts.api.urls')),
    path('students/', include('students.api.urls')),
    path('teachers/', include('teachers.api.urls')),
    path('staff/', include('staff.api.urls')),
    path('examinations/', include('examinations.api.urls')),
    path('attendance/', include('attendance.api.urls')),
    path('courses/', include('courses.api.urls')),
    path('discipline/', include('discipline.api.urls')),
    path('schedules/', include('schedules.api.urls')),
    path('communication/', include('communication.api.urls')),
]
