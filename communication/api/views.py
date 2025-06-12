from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from accounts.permissions import (
    IsOwnerOrAdmin, IsStaffOrAdmin, IsTeacherOrAdmin,
    IsStudentOrTeacherOrAdmin, CanAccessCommunication
)

from ..models import Message, Notification, Announcement
from .serializers import (
    MessageSerializer, MessageDetailSerializer, MessageCreateSerializer, 
    MessageReplySerializer, NotificationSerializer, MessageStatsSerializer,
    BulkMessageSerializer, UserBasicSerializer, AnnouncementSerializer
)

User = get_user_model()


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages with role-based permissions
    - All authenticated users can send/receive messages
    - Staff/Admins can view all messages (for moderation)
    - Users can only see messages they sent or received
    """
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_read', 'sender', 'recipient']
    search_fields = ['subject', 'body', 'sender__username', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['timestamp', 'subject', 'is_read']
    ordering = ['-timestamp']
    
    def get_permissions(self):
        """
        Role-based permissions for message management
        """
        if self.action in ['statistics'] and self.request.query_params.get('admin') == 'true':
            # Only staff/admins can access system-wide message statistics
            permission_classes = [IsStaffOrAdmin]
        elif self.action in ['bulk_send']:
            # Teachers and staff/admins can send bulk messages
            permission_classes = [IsTeacherOrAdmin]
        else:
            # All authenticated users can manage their own messages
            permission_classes = [CanAccessCommunication]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Get messages for the current user (sent or received) or all if admin"""
        user = self.request.user
        
        # Admin users and staff can see all messages if requested
        if (user.is_staff or user.is_superuser) and self.request.query_params.get('admin') == 'true':
            return Message.objects.select_related('sender', 'recipient').prefetch_related(
                Prefetch('replies', queryset=Message.objects.select_related('sender', 'recipient'))
            ).all()
        
        # Regular users can only see their own messages
        return Message.objects.select_related('sender', 'recipient').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'recipient'))
        ).filter(
            Q(sender=user) | Q(recipient=user)
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MessageDetailSerializer
        elif self.action == 'create':
            return MessageCreateSerializer
        elif self.action == 'reply':
            return MessageReplySerializer
        elif self.action == 'bulk_send':
            return BulkMessageSerializer
        return MessageSerializer

    def retrieve(self, request, *args, **kwargs):
        """Mark message as read when retrieved"""
        instance = self.get_object()
        
        # Mark as read if current user is the recipient
        if instance.recipient == request.user and not instance.is_read:
            instance.is_read = True
            instance.save(update_fields=['is_read'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get user's inbox messages"""
        messages = self.get_queryset().filter(
            recipient=request.user,
            parent__isnull=True  # Only show parent messages, not replies
        )
        
        # Apply filtering
        is_read = request.query_params.get('is_read')
        if is_read is not None:
            messages = messages.filter(is_read=is_read.lower() == 'true')
        
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get user's sent messages"""
        messages = self.get_queryset().filter(
            sender=request.user,
            parent__isnull=True  # Only show parent messages, not replies
        )
        
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get user's unread messages"""
        unread_messages = self.get_queryset().filter(
            recipient=request.user,
            is_read=False
        )
        
        serializer = self.get_serializer(unread_messages, many=True)
        return Response({
            'unread_messages': serializer.data,
            'unread_count': unread_messages.count()
        })

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Reply to a message"""
        parent_message = self.get_object()
        
        # Check if user can reply to this message
        if parent_message.sender != request.user and parent_message.recipient != request.user:
            return Response(
                {'error': 'You can only reply to messages you sent or received'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'parent_message': parent_message}
        )
        
        if serializer.is_valid():
            reply = serializer.save()
            return Response(
                MessageDetailSerializer(reply, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        
        if message.recipient != request.user:
            return Response(
                {'error': 'You can only mark your own messages as read'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = True
        message.save(update_fields=['is_read'])
        
        return Response({'status': 'Message marked as read'})

    @action(detail=True, methods=['post'])
    def mark_unread(self, request, pk=None):
        """Mark a message as unread"""
        message = self.get_object()
        
        if message.recipient != request.user:
            return Response(
                {'error': 'You can only mark your own messages as unread'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = False
        message.save(update_fields=['is_read'])
        
        return Response({'status': 'Message marked as unread'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all user's messages as read"""
        updated_count = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        
        return Response({
            'status': 'All messages marked as read',
            'updated_count': updated_count
        })

    @action(detail=False, methods=['post'], url_path='bulk-send')
    def bulk_send(self, request):
        """
        Send a message to multiple users or groups.
        Requires 'recipient_ids' (list of user IDs) or 'recipient_roles' (list of roles like 'student', 'teacher').
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                messages_sent = serializer.save()
                if not messages_sent:
                    return Response(
                        {'status': 'No messages sent. This might occur if the sender is the only recipient.'},
                        status=status.HTTP_200_OK # Or 204 No Content, depending on preference
                    )
                return Response(
                    {'status': f'{len(messages_sent)} messages sent successfully'},
                    status=status.HTTP_201_CREATED
                )
            except serializers.ValidationError as e: # Catch validation errors from serializer.save() if any
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get message statistics for the current user or system-wide if admin.
        """
        user = request.user
        
        if (user.is_staff or user.is_superuser) and request.query_params.get('admin') == 'true':
            # System-wide statistics
            total_messages = Message.objects.count()
            total_read = Message.objects.filter(is_read=True).count()
            total_unread = total_messages - total_read
            
            # Messages in the last 24 hours
            one_day_ago = timezone.now() - timedelta(days=1)
            recent_messages = Message.objects.filter(timestamp__gte=one_day_ago).count()
            
            # Top 5 senders
            top_senders_data = Message.objects.values('sender').annotate(
                num_sent=Count('id')
            ).order_by('-num_sent')[:5]
            
            top_senders = []
            for item in top_senders_data:
                sender_user = User.objects.filter(id=item['sender']).first()
                if sender_user:
                    top_senders.append({
                        'user': UserBasicSerializer(sender_user).data,
                        'num_sent': item['num_sent']
                    })

            stats = {
                'total_messages': total_messages,
                'total_read': total_read,
                'total_unread': total_unread,
                'recent_messages_24h': recent_messages,
                'top_senders': top_senders
            }
        else:
            # User-specific statistics
            total_sent = self.get_queryset().filter(sender=user).count()
            total_received = self.get_queryset().filter(recipient=user).count()
            unread_received = self.get_queryset().filter(recipient=user, is_read=False).count()
            
            stats = {
                'total_sent': total_sent,
                'total_received': total_received,
                'unread_received': unread_received
            }
            
        serializer = MessageStatsSerializer(stats)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notifications.
    Users can only see their own notifications.
    Admins can see all notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated] # Base permission
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['timestamp', 'is_read']
    ordering = ['-timestamp']

    def get_queryset(self):
        """Return notifications for the current user or all if admin."""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Notification.objects.select_related('user', 'message').all()
        return Notification.objects.select_related('user', 'message').filter(user=user)

    @action(detail=True, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        """Mark a specific notification as read."""
        notification = self.get_object()
        if notification.user != request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response({'error': 'You can only mark your own notifications as read.'},
                            status=status.HTTP_403_FORBIDDEN)
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({'status': 'Notification marked as read'})

    @action(detail=False, methods=['post'], url_path='mark-all-as-read')
    def mark_all_as_read(self, request):
        """Mark all notifications for the current user as read."""
        updated_count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': f'{updated_count} notifications marked as read'})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        """Get the count of unread notifications for the current user."""
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing announcements.
    - All authenticated users can view published announcements.
    - Staff/Admins can create, update, delete, publish, and unpublish announcements.
    """
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_published', 'author']
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'is_published']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return published announcements for all users.
        Admins/Staff see all announcements (published and unpublished).
        """
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Announcement.objects.select_related('author').all()
        return Announcement.objects.select_related('author').filter(is_published=True)

    def get_permissions(self):
        """
        - Allow read-only for authenticated users for list/retrieve.
        - Require Staff/Admin for other actions.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['publish', 'unpublish']:
            permission_classes = [IsStaffOrAdmin] # Or a more specific permission like CanManageAnnouncements
        else: # create, update, partial_update, destroy
            permission_classes = [IsStaffOrAdmin] # Or a more specific permission
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Set the author of the announcement to the current user."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish an announcement."""
        announcement = self.get_object()
        # Permission check is handled by get_permissions
        announcement.is_published = True
        announcement.save(update_fields=['is_published'])
        return Response(AnnouncementSerializer(announcement).data)

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """Unpublish an announcement."""
        announcement = self.get_object()
        # Permission check is handled by get_permissions
        announcement.is_published = False
        announcement.save(update_fields=['is_published'])
        return Response(AnnouncementSerializer(announcement).data)

    # Example of a custom action for announcements, e.g., targeting specific roles
    # @action(detail=True, methods=['post'], url_path='target-roles')
    # def target_roles(self, request, pk=None):
    #     announcement = self.get_object()
    #     # Logic to update target roles for the announcement
    #     # Requires a 'roles' field in request.data (e.g., list of role IDs or names)
    #     # And a ManyToManyField 'target_roles' on the Announcement model
    #     return Response({'status': 'Target roles updated'})

# TODO: Consider adding a Dashboard/Feed API view that aggregates:
# - Recent unread messages
# - Recent unread notifications
# - Recent published announcements
# This could be useful for a central dashboard page in the frontend.
