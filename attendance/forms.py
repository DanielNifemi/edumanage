from django import forms
from django.contrib.auth import get_user_model
from .models import Attendance

User = get_user_model()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'is_present']


class AttendanceReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    student = forms.ModelChoiceField(queryset=User.objects.all())
