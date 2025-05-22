from django import forms
from .models import StaffProfile, LeaveRequest, PerformanceEvaluation


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        exclude = ['user']


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        exclude = ['staff', 'status']


class PerformanceEvaluationForm(forms.ModelForm):
    class Meta:
        model = PerformanceEvaluation
        exclude = ['staff', 'evaluator', 'date']
