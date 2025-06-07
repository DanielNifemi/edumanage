from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import InfractionType, DisciplinaryAction, DisciplinaryRecord, BehaviorNote
from students.models import Student

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for staff references"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id', 'username']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class StudentBasicSerializer(serializers.ModelSerializer):
    """Basic student serializer"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'user', 'full_name']
        read_only_fields = ['id', 'student_id']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class InfractionTypeSerializer(serializers.ModelSerializer):
    """Serializer for infraction types"""
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    record_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InfractionType
        fields = ['id', 'name', 'description', 'severity', 'severity_display', 'record_count']
        read_only_fields = ['id', 'record_count']
    
    def get_record_count(self, obj):
        return obj.disciplinaryrecord_set.count()


class DisciplinaryActionSerializer(serializers.ModelSerializer):
    """Serializer for disciplinary actions"""
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DisciplinaryAction
        fields = ['id', 'name', 'description', 'usage_count']
        read_only_fields = ['id', 'usage_count']
    
    def get_usage_count(self, obj):
        return obj.disciplinaryrecord_set.count()


class DisciplinaryRecordSerializer(serializers.ModelSerializer):
    """Serializer for disciplinary records"""
    student = StudentBasicSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    infraction_type = InfractionTypeSerializer(read_only=True)
    infraction_type_id = serializers.IntegerField(write_only=True)
    action_taken = DisciplinaryActionSerializer(read_only=True)
    action_taken_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reported_by = UserBasicSerializer(read_only=True)
    days_since_incident = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = DisciplinaryRecord
        fields = [
            'id', 'student', 'student_id', 'infraction_type', 'infraction_type_id',
            'date', 'reported_by', 'description', 'action_taken', 'action_taken_id',
            'action_date', 'resolved', 'resolution_notes', 'days_since_incident', 'is_overdue'
        ]
        read_only_fields = ['id', 'reported_by', 'days_since_incident', 'is_overdue']
    
    def get_days_since_incident(self, obj):
        from django.utils import timezone
        return (timezone.now().date() - obj.date).days
    
    def get_is_overdue(self, obj):
        from django.utils import timezone
        # Consider unresolved records older than 7 days as overdue
        if not obj.resolved:
            return (timezone.now().date() - obj.date).days > 7
        return False
    
    def validate_student_id(self, value):
        try:
            Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid student ID")
        return value
    
    def validate_infraction_type_id(self, value):
        try:
            InfractionType.objects.get(id=value)
        except InfractionType.DoesNotExist:
            raise serializers.ValidationError("Invalid infraction type ID")
        return value
    
    def validate_action_taken_id(self, value):
        if value is not None:
            try:
                DisciplinaryAction.objects.get(id=value)
            except DisciplinaryAction.DoesNotExist:
                raise serializers.ValidationError("Invalid disciplinary action ID")
        return value
    
    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        infraction_type_id = validated_data.pop('infraction_type_id')
        action_taken_id = validated_data.pop('action_taken_id', None)
        
        validated_data['student'] = Student.objects.get(id=student_id)
        validated_data['infraction_type'] = InfractionType.objects.get(id=infraction_type_id)
        if action_taken_id:
            validated_data['action_taken'] = DisciplinaryAction.objects.get(id=action_taken_id)
        validated_data['reported_by'] = self.context['request'].user
        
        return super().create(validated_data)


class DisciplinaryRecordDetailSerializer(DisciplinaryRecordSerializer):
    """Detailed serializer for disciplinary records"""
    student_history_count = serializers.SerializerMethodField()
    related_notes = serializers.SerializerMethodField()
    
    class Meta(DisciplinaryRecordSerializer.Meta):
        fields = DisciplinaryRecordSerializer.Meta.fields + ['student_history_count', 'related_notes']
    
    def get_student_history_count(self, obj):
        return DisciplinaryRecord.objects.filter(student=obj.student).count()
    
    def get_related_notes(self, obj):
        # Get behavior notes from the same day
        notes = BehaviorNote.objects.filter(student=obj.student, date=obj.date)
        return BehaviorNoteSerializer(notes, many=True).data


class BehaviorNoteSerializer(serializers.ModelSerializer):
    """Serializer for behavior notes"""
    student = StudentBasicSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    noted_by = UserBasicSerializer(read_only=True)
    days_since_note = serializers.SerializerMethodField()
    
    class Meta:
        model = BehaviorNote
        fields = ['id', 'student', 'student_id', 'date', 'noted_by', 'note', 'days_since_note']
        read_only_fields = ['id', 'noted_by', 'days_since_note']
    
    def get_days_since_note(self, obj):
        from django.utils import timezone
        return (timezone.now().date() - obj.date).days
    
    def validate_student_id(self, value):
        try:
            Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid student ID")
        return value
    
    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        validated_data['student'] = Student.objects.get(id=student_id)
        validated_data['noted_by'] = self.context['request'].user
        return super().create(validated_data)


class BulkRecordSerializer(serializers.Serializer):
    """Serializer for bulk creating disciplinary records"""
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=50
    )
    infraction_type_id = serializers.IntegerField()
    date = serializers.DateField()
    description = serializers.CharField()
    action_taken_id = serializers.IntegerField(required=False, allow_null=True)
    action_date = serializers.DateField(required=False, allow_null=True)
    
    def validate_student_ids(self, value):
        # Check if all student IDs are valid
        valid_ids = Student.objects.filter(id__in=value).values_list('id', flat=True)
        invalid_ids = set(value) - set(valid_ids)
        
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid student IDs: {list(invalid_ids)}")
        
        return value
    
    def validate_infraction_type_id(self, value):
        try:
            InfractionType.objects.get(id=value)
        except InfractionType.DoesNotExist:
            raise serializers.ValidationError("Invalid infraction type ID")
        return value
    
    def create(self, validated_data):
        student_ids = validated_data.pop('student_ids')
        infraction_type_id = validated_data.pop('infraction_type_id')
        action_taken_id = validated_data.pop('action_taken_id', None)
        
        infraction_type = InfractionType.objects.get(id=infraction_type_id)
        action_taken = DisciplinaryAction.objects.get(id=action_taken_id) if action_taken_id else None
        reported_by = self.context['request'].user
        
        records = []
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            record = DisciplinaryRecord(
                student=student,
                infraction_type=infraction_type,
                action_taken=action_taken,
                reported_by=reported_by,
                **validated_data
            )
            records.append(record)
        
        # Bulk create records
        created_records = DisciplinaryRecord.objects.bulk_create(records)
        return created_records
