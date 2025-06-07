from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    attachment = models.FileField(upload_to='message_attachments/', null=True, blank=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.subject}"

    class Meta:
        ordering = ['-timestamp']


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('new_message', 'New Message'),
        ('assignment_due', 'Assignment Due'),
        ('new_announcement', 'New Announcement'),
        ('grade_released', 'Grade Released'),
        # Add other types as needed
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)  # Can be null if not message-related
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='new_message')  # Added default
    text_content = models.TextField(null=True, blank=True)  # For notifications not directly tied to a message
    related_object_id = models.PositiveIntegerField(null=True, blank=True)  # Generic FK to related object (e.g., Assignment ID, Announcement ID)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}: {self.get_notification_type_display()}"

    class Meta:
        ordering = ['-timestamp']


class Announcement(models.Model):
    """Model for general announcements"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='authored_announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # Target audience (optional - could be implemented with ManyToManyField to User groups or roles)
    # target_roles = models.ManyToManyField(Role) # Example if you have a Role model

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
