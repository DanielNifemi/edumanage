from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enroll/', views.course_enroll, name='course_enroll'),
    path('<int:pk>/drop/', views.course_drop, name='course_drop'),
    path('<int:course_pk>/content/create/', views.content_create, name='content_create'),
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('submission/<int:submission_pk>/grade/', views.grade_assignment, name='grade_assignment'),
]
