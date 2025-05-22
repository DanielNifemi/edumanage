from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('phone-verification/', views.phone_verification, name='phone_verification'),
    path('create_admin/', views.create_admin, name='create_admin'),
    path('signup/', views.CustomSignupView.as_view(), name='account_signup'),
    path('login/', views.CustomLoginView.as_view(), name='account_login'),
    path('logout/', views.CustomLogoutView.as_view(), name='account_logout'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),  # match the URL style
    path('dashboard/', views.dashboard, name='dashboard'),
    path('switch-role/<str:role>/', views.switch_role, name='switch_role'),
    path('edit-profile/<str:profile_type>/', views.edit_profile, name='edit_profile'),
    
    # Teacher routes
    path('grade-assignments/', views.grade_assignments, name='grade_assignments'),
    
    # Staff routes
    path('manage-records/', views.manage_records, name='manage_records'),
    
    # Student routes
    path('view-grades/', views.view_grades, name='view_grades'),
]
