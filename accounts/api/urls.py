from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.UserProfileViewSet, basename='userprofile')

urlpatterns = [
    # ViewSet URLs
    path('', include(router.urls)),
    
    # Test endpoint for debugging
    path('test/', views.test_endpoint, name='api_test'),
    
    # Authentication URLs (function-based views)
    path('csrf/', views.csrf_token_view, name='api_csrf_token'),
    path('user/', views.current_user_view, name='api_current_user'),
    path('login/', views.login_view, name='api_login'),
    path('register/', views.register_view, name='api_register'),
    path('logout/', views.logout_view, name='api_logout'),
    path('profile/', views.user_profile, name='api_user_profile'),
    path('dashboard/', views.dashboard_data, name='api_dashboard_data'),
]