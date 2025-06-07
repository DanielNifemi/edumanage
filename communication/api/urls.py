from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, NotificationViewSet, AnnouncementViewSet  # Added AnnouncementViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')  # Added AnnouncementViewSet

urlpatterns = [
    path('', include(router.urls)),
]
