from django.urls import path
from . import views

urlpatterns = [
    path('student/<int:student_id>/', views.student_discipline_record, name='student_discipline_record'),
    path('student/<int:student_id>/add_record/', views.add_disciplinary_record, name='add_disciplinary_record'),
    path('student/<int:student_id>/add_note/', views.add_behavior_note, name='add_behavior_note'),
    path('dashboard/', views.discipline_dashboard, name='discipline_dashboard'),
]