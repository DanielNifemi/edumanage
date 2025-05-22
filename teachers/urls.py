from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('subjects/', views.teacher_subjects, name='teacher_subjects'),
    path('classes/', views.teacher_classes, name='teacher_classes'),
    path('lessons/', views.teacher_lessons, name='teacher_lessons'),
    path('lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/edit/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
]
