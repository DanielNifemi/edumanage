from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_admin/', views.create_admin, name='create_admin'),
    path('signup/', views.CustomSignupView.as_view(), name='account_signup'),
    path('login/', views.CustomLoginView.as_view(), name='account_login'),
    path('logout/', views.CustomLogoutView.as_view(), name='account_logout'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
