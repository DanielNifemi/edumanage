from django.urls import path
from . import views


urlpatterns = [
    path('exam/', views.exam_list, name='exam_list'),
    path('exam/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('create/', views.create_exam, name='create_exam'),
]