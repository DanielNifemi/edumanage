from django import forms
from .models import Course, CourseContent, Assignment, AssignmentSubmission

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'name', 'description', 'syllabus', 
                 'virtual_classroom_link', 'schedule', 'semester', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'schedule': forms.TextInput(attrs={'placeholder': 'e.g., Mon/Wed 10 AM'}),
            'year': forms.NumberInput(attrs={'min': 2024}),
        }

class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = ['title', 'description', 'content_type', 'file', 'url', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['total_points', 'submission_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['submission_type'].widget = forms.Select(choices=[
            ('file', 'File Upload'),
            ('text', 'Text Submission'),
            ('link', 'URL Link'),
        ])

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['submitted_file', 'submitted_text', 'submitted_url']

    def __init__(self, *args, submission_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        if submission_type:
            # Only show relevant submission field based on assignment type
            if submission_type == 'file':
                del self.fields['submitted_text']
                del self.fields['submitted_url']
            elif submission_type == 'text':
                del self.fields['submitted_file']
                del self.fields['submitted_url']
            elif submission_type == 'link':
                del self.fields['submitted_file']
                del self.fields['submitted_text']

class GradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['grade', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }
