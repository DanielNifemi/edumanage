from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from ..models import Attendance, AttendanceReport, SchoolCalendar

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details in attendance context"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class SchoolCalendarSerializer(serializers.ModelSerializer):
    """Serializer for School Calendar model"""
    day_type = serializers.SerializerMethodField()
    
    class Meta:
        model = SchoolCalendar
        fields = ['id', 'date', 'is_holiday', 'event_name', 'day_type']
        read_only_fields = ['id']
    
    def get_day_type(self, obj):
        return 'Holiday' if obj.is_holiday else 'School Day'


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'date', 'is_present',
            'student_name', 'student_username', 'status'
        ]
        read_only_fields = ['id']
    
    def get_status(self, obj):
        return 'Present' if obj.is_present else 'Absent'


class AttendanceBulkSerializer(serializers.Serializer):
    """Serializer for bulk attendance marking"""
    date = serializers.DateField()
    student_data = serializers.DictField(
        child=serializers.BooleanField(),
        help_text="Dictionary with student_id as key and is_present as boolean value"
    )
    
    def create(self, validated_data):
        date = validated_data['date']
        student_data = validated_data['student_data']
        
        # Delete existing attendance for this date
        Attendance.objects.filter(date=date, student_id__in=student_data.keys()).delete()
        
        # Create new attendance records
        attendances = []
        for student_id, is_present in student_data.items():
            attendances.append(
                Attendance(student_id=int(student_id), date=date, is_present=is_present)
            )
        
        return Attendance.objects.bulk_create(attendances)


class AttendanceReportSerializer(serializers.ModelSerializer):
    """Serializer for Attendance Report model"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    attendance_percentage = serializers.SerializerMethodField()
    days_absent = serializers.SerializerMethodField()
    
    class Meta:
        model = AttendanceReport
        fields = [
            'id', 'student', 'start_date', 'end_date', 'total_days',
            'days_present', 'student_name', 'student_username',
            'attendance_percentage', 'days_absent'
        ]
        read_only_fields = ['id']
    
    def get_attendance_percentage(self, obj):
        if obj.total_days > 0:
            return round((obj.days_present / obj.total_days) * 100, 2)
        return 0
    
    def get_days_absent(self, obj):
        return obj.total_days - obj.days_present


class AttendanceStatsSerializer(serializers.Serializer):
    """Serializer for attendance statistics"""
    total_students = serializers.IntegerField()
    present_today = serializers.IntegerField()
    absent_today = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
    
    
class StudentAttendanceSummarySerializer(serializers.Serializer):
    """Serializer for student attendance summary"""
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    total_days = serializers.IntegerField()
    days_present = serializers.IntegerField()
    days_absent = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
    low_attendance_alert = serializers.BooleanField()


class AttendanceDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for attendance with all related information"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_grade = serializers.CharField(source='student.grade', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    is_late = serializers.SerializerMethodField()
    attendance_status_display = serializers.CharField(source='get_attendance_status_display', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'date', 'attendance_status', 'time_in', 
            'time_out', 'notes', 'student_name', 'student_grade',
            'student_id', 'is_late', 'attendance_status_display'
        ]
        read_only_fields = ['id']
    
    def get_is_late(self, obj):
        """Check if student was late (arrived after 8:00 AM)"""
        if obj.time_in:
            from datetime import time
            return obj.time_in > time(8, 0)  # Assuming school starts at 8:00 AM
        return False
