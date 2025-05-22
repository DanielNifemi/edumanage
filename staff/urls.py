from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.staff_profile, name='staff_profile'),
    path('leave/request/', views.leave_request, name='leave_request'),
    path('leave/list/', views.leave_list, name='leave_list'),
    path('evaluate/<int:staff_id>/', views.performance_evaluation, name='performance_evaluation'),
    path('list/', views.staff_list, name='staff_list'),
    path('records/manage/', views.manage_records, name='manage_records'),
]
