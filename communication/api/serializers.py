from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Message, Notification, Announcement  # Added Announcement

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for message recipients/senders"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'email']
        read_only_fields = ['id', 'username', 'email']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for creating and listing messages"""
    sender = UserBasicSerializer(read_only=True)
    recipient_id = serializers.IntegerField(write_only=True)
    recipient = UserBasicSerializer(read_only=True)
    has_replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'recipient', 'recipient_id', 'subject', 'body', 
            'timestamp', 'is_read', 'parent', 'attachment', 'has_replies', 'reply_count'
        ]
        read_only_fields = ['id', 'sender', 'timestamp', 'has_replies', 'reply_count']
    
    def get_has_replies(self, obj):
        return obj.replies.exists()
    
    def get_reply_count(self, obj):
        return obj.replies.count()
    
    def create(self, validated_data):
        recipient_id = validated_data.pop('recipient_id')
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({'recipient_id': 'Invalid recipient ID'})
        
        validated_data['recipient'] = recipient
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class MessageDetailSerializer(MessageSerializer):
    """Detailed serializer for message retrieval with replies"""
    replies = serializers.SerializerMethodField()
    parent_message = serializers.SerializerMethodField()
    
    class Meta(MessageSerializer.Meta):
        fields = MessageSerializer.Meta.fields + ['replies', 'parent_message']
    
    def get_replies(self, obj):
        replies = obj.replies.all().order_by('timestamp')
        return MessageSerializer(replies, many=True, context=self.context).data
    
    def get_parent_message(self, obj):
        if obj.parent:
            return {
                'id': obj.parent.id,
                'subject': obj.parent.subject,
                'sender': UserBasicSerializer(obj.parent.sender).data,
                'timestamp': obj.parent.timestamp
            }
        return None


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new messages"""
    recipient_id = serializers.IntegerField()
    
    class Meta:
        model = Message
        fields = ['recipient_id', 'subject', 'body', 'parent', 'attachment']
    
    def validate_recipient_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid recipient ID")
        return value
    
    def validate_parent(self, value):
        if value and value.sender != self.context['request'].user and value.recipient != self.context['request'].user:
            raise serializers.ValidationError("You can only reply to messages you sent or received")
        return value
    
    def create(self, validated_data):
        recipient_id = validated_data.pop('recipient_id')
        recipient = User.objects.get(id=recipient_id)
        
        validated_data['recipient'] = recipient
        validated_data['sender'] = self.context['request'].user
        message = Message.objects.create(**validated_data)
        # Create notification for the recipient
        Notification.objects.create(user=recipient, message=message, notification_type='new_message')
        return message


class MessageReplySerializer(serializers.ModelSerializer):
    """Serializer for replying to messages"""
    class Meta:
        model = Message
        fields = ['body', 'attachment'] # Replies typically only need a body and optional attachment

    def create(self, validated_data):
        request = self.context['request']
        parent_message_id = self.context['view'].kwargs.get('parent_pk') # Assuming parent_pk is used in URL for reply
        
        try:
            parent_message = Message.objects.get(id=parent_message_id)
        except Message.DoesNotExist:
            raise serializers.ValidationError("Parent message not found.")

        # Determine recipient of the reply (the other party in the original message)
        if parent_message.sender == request.user:
            recipient = parent_message.recipient
        elif parent_message.recipient == request.user:
            recipient = parent_message.sender
        else:
            raise serializers.ValidationError("You cannot reply to this message.")

        reply = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=f"Re: {parent_message.subject}",
            body=validated_data['body'],
            parent=parent_message,
            attachment=validated_data.get('attachment')
        )
        # Create notification for the recipient of the reply
        Notification.objects.create(user=recipient, message=reply, notification_type='new_reply')
        return reply


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    message_subject = serializers.CharField(source='message.subject', read_only=True)
    message_sender = UserBasicSerializer(source='message.sender', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'message', 'message_subject', 'message_sender',
            'is_read', 'timestamp', 'notification_type', 'notification_type_display',
            'related_object_id'
        ]
        read_only_fields = ['id', 'user', 'message', 'timestamp']


class AnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for announcements"""
    author = UserBasicSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='author', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'author', 'author_id', 'created_at', 
            'updated_at', 'is_published'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def create(self, validated_data):
        # If author_id is not provided, it will be set in perform_create of the ViewSet
        if 'author' not in validated_data and 'request' in self.context:
            validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class MessageStatsSerializer(serializers.Serializer):
    """Serializer for message statistics"""
    total_sent = serializers.IntegerField()
    total_received = serializers.IntegerField()
    unread_count = serializers.IntegerField()
    reply_count = serializers.IntegerField()
    recent_messages = MessageSerializer(many=True)


class BulkMessageSerializer(serializers.Serializer):
    """Serializer for sending bulk messages"""
    recipient_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100
    )
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()
    attachment = serializers.FileField(required=False)
    
    def validate_recipient_ids(self, value):
        # Check if all recipient IDs are valid
        valid_ids = User.objects.filter(id__in=value).values_list('id', flat=True)
        invalid_ids = set(value) - set(valid_ids)
        
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid recipient IDs: {list(invalid_ids)}")
        
        return value
    
    def create(self, validated_data):
        recipient_ids = validated_data.pop('recipient_ids')
        sender = self.context['request'].user
        
        messages = []
        for recipient_id in recipient_ids:
            recipient = User.objects.get(id=recipient_id)
            message = Message(
                sender=sender,
                recipient=recipient,
                **validated_data
            )
            messages.append(message)
        
        # Bulk create messages
        created_messages = Message.objects.bulk_create(messages)
        return created_messages
