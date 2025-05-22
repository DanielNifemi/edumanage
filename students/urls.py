from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('create/', views.student_create, name='student_create'),
    path('<int:pk>/update/', views.student_update, name='student_update'),
    path('<int:student_pk>/add_academic_record/', views.academic_record_create, name='academic_record_create'),
    path('grades/', views.view_grades, name='view_grades'),
]