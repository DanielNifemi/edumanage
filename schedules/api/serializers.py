from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Schedule, TimeSlot, DayOfWeek, Event
from teachers.models import Teacher, Class, Subject

User = get_user_model()


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for TimeSlot model"""
    duration = serializers.SerializerMethodField()
    display_time = serializers.SerializerMethodField()
    
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'duration', 'display_time']
        read_only_fields = ['id']
    
    def get_duration(self, obj):
        """Calculate duration in minutes"""
        if obj.start_time and obj.end_time:
            from datetime import datetime, timedelta
            start = datetime.combine(datetime.today(), obj.start_time)
            end = datetime.combine(datetime.today(), obj.end_time)
            duration = end - start
            return int(duration.total_seconds() / 60)
        return None
    
    def get_display_time(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"


class DayOfWeekSerializer(serializers.ModelSerializer):
    """Serializer for DayOfWeek model"""
    day_name = serializers.CharField(source='get_day_display', read_only=True)
    
    class Meta:
        model = DayOfWeek
        fields = ['id', 'day', 'day_name']
        read_only_fields = ['id']


class TeacherBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for teacher in schedule context"""
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_id', 'full_name']
        read_only_fields = ['id', 'teacher_id']


class ClassBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for class in schedule context"""
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher_name']
        read_only_fields = ['id']


class SubjectBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for subject in schedule context"""
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']


class ScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Schedule model"""
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    day_name = serializers.CharField(source='day.get_day_display', read_only=True)
    time_display = serializers.CharField(source='time_slot.__str__', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'class_group', 'day', 'time_slot', 'subject', 'teacher',
            'class_name', 'day_name', 'time_display', 'subject_name', 'teacher_name'
        ]
        read_only_fields = ['id']


class ScheduleDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for schedule with related objects"""
    class_group = ClassBasicSerializer(read_only=True)
    day = DayOfWeekSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    subject = SubjectBasicSerializer(read_only=True)
    teacher = TeacherBasicSerializer(read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'class_group', 'day', 'time_slot', 'subject', 'teacher'
        ]
        read_only_fields = ['id']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    duration = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()
    formatted_datetime = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_datetime', 'end_datetime',
            'location', 'duration', 'is_past', 'formatted_datetime'
        ]
        read_only_fields = ['id']
    
    def get_duration(self, obj):
        """Calculate event duration in hours"""
        if obj.start_datetime and obj.end_datetime:
            duration = obj.end_datetime - obj.start_datetime
            return round(duration.total_seconds() / 3600, 2)
        return None
    
    def get_is_past(self, obj):
        """Check if event is in the past"""
        from django.utils import timezone
        return obj.end_datetime < timezone.now()
    
    def get_formatted_datetime(self, obj):
        """Get formatted datetime string"""
        return {
            'start': obj.start_datetime.strftime('%Y-%m-%d %H:%M'),
            'end': obj.end_datetime.strftime('%Y-%m-%d %H:%M'),
            'date': obj.start_datetime.strftime('%Y-%m-%d'),
            'time': f"{obj.start_datetime.strftime('%H:%M')} - {obj.end_datetime.strftime('%H:%M')}"
        }


class WeeklyScheduleSerializer(serializers.Serializer):
    """Serializer for weekly schedule view"""
    class_group = serializers.CharField()
    schedule = serializers.DictField()
    
    
class TimetableSerializer(serializers.Serializer):
    """Serializer for timetable data"""
    day = serializers.CharField()
    time_slots = serializers.ListField()
    schedules = ScheduleSerializer(many=True)
