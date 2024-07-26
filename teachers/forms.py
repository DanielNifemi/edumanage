# forms.py

from django import forms
from .models import Teacher, Lesson


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['subjects', 'qualification', 'years_of_experience']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'class_group', 'date', 'start_time', 'end_time', 'topic', 'youtube_link']
