from django import forms
from .models import Student, AcademicRecord


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'date_of_birth', 'grade', 'address', 'parent_name', 'parent_contact']


class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ['subject', 'grade', 'semester', 'year']
