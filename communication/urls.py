from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('compose/', views.compose_message, name='compose_message'),
    path('view/<int:message_id>/', views.view_message, name='view_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('forward/<int:message_id>/', views.forward_message, name='forward_message'),
    path('reply/<int:message_id>/', views.reply_message, name='reply_message'),
    path('notifications/', views.notifications, name='notifications'),
]