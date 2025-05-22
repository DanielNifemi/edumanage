from django import forms
from django.contrib.auth import get_user_model
from .models import Attendance, SchoolCalendar

User = get_user_model()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'is_present']


class BulkAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for student in User.objects.all():
            self.fields[f'student_{student.id}'] = forms.BooleanField(label=student.username, required=False)


class AttendanceReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    student = forms.ModelChoiceField(queryset=User.objects.all())


class SchoolCalendarForm(forms.ModelForm):
    class Meta:
        model = SchoolCalendar
        fields = ['date', 'is_holiday', 'event_name']