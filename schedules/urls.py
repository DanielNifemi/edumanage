from django.urls import path
from . import views

urlpatterns = [
    path('class/<int:class_id>/', views.class_schedule, name='class_schedule'),
    path('add/', views.add_schedule, name='add_schedule'),
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.add_event, name='add_event'),
]