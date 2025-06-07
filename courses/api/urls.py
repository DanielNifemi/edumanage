from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'enrollments', views.CourseEnrollmentViewSet, basename='enrollment')
router.register(r'content', views.CourseContentViewSet, basename='content')
router.register(r'assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'submissions', views.AssignmentSubmissionViewSet, basename='submission')
router.register(r'announcements', views.CourseAnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]

# Available endpoints:
# GET /api/courses/ - List all courses with filtering and search
# POST /api/courses/ - Create a new course
# GET /api/courses/{id}/ - Get course details
# PUT /api/courses/{id}/ - Update course
# PATCH /api/courses/{id}/ - Partial update course
# DELETE /api/courses/{id}/ - Delete course
# POST /api/courses/{id}/enroll/ - Enroll in course
# POST /api/courses/{id}/unenroll/ - Unenroll from course
# GET /api/courses/{id}/content/ - Get course content
# GET /api/courses/{id}/assignments/ - Get course assignments
# GET /api/courses/{id}/enrollments/ - Get course enrollments
# GET /api/courses/{id}/analytics/ - Get course analytics
# GET /api/courses/statistics/ - Get overall course statistics

# GET /api/enrollments/ - List enrollments
# POST /api/enrollments/ - Create enrollment
# GET /api/enrollments/{id}/ - Get enrollment details
# POST /api/enrollments/{id}/update_progress/ - Update progress

# GET /api/content/ - List course content
# POST /api/content/ - Create content
# POST /api/content/bulk_create/ - Create multiple contents

# GET /api/assignments/ - List assignments
# POST /api/assignments/ - Create assignment
# GET /api/assignments/{id}/submissions/ - Get assignment submissions
# POST /api/assignments/{id}/bulk_grade/ - Grade multiple submissions

# GET /api/submissions/ - List submissions
# POST /api/submissions/ - Create submission
# POST /api/submissions/{id}/grade/ - Grade submission

# GET /api/announcements/ - List announcements
# POST /api/announcements/ - Create announcement
# POST /api/announcements/{id}/toggle_pin/ - Toggle pin status
