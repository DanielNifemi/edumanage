from django import forms
from .models import Schedule, Event


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['class_group', 'day', 'time_slot', 'subject', 'teacher']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_datetime', 'end_datetime', 'location']
