from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from edumanage.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('edumanage.api')),  # API endpoints for React frontend
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('staff/', include('staff.urls')),
    path('discipline/', include('discipline.urls')),
    path('attendance/', include('attendance.urls')),
    path('communication/', include('communication.urls')),
    path('schedules/', include('schedules.urls')),
    path('examinations/', include('examinations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
