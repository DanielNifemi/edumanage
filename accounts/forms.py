from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from .models import CustomUser, UserProfile
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create UserProfile with selected type
            UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type']
            )
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')


class AdminCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_admin')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type']


class PhoneVerificationForm(forms.Form):
    phone_number = forms.CharField(max_length=15)


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)


class ProfileBaseForm(forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    class Meta:
        abstract = True

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob > timezone.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future!")
        return dob


class StudentProfileForm(ProfileBaseForm):
    parent_contact = forms.CharField(validators=[ProfileBaseForm.phone_validator])

    class Meta:
        model = Student
        fields = ['student_id', 'date_of_birth', 'grade', 'address', 'parent_name', 'parent_contact']

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not student_id.startswith('STU'):
            raise forms.ValidationError("Student ID must start with 'STU'")
        return student_id


class TeacherProfileForm(ProfileBaseForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'subjects', 'qualification', 'department', 'years_of_experience']
        widgets = {
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data.get('teacher_id')
        if not teacher_id.startswith('TCH'):
            raise forms.ValidationError("Teacher ID must start with 'TCH'")
        return teacher_id


class StaffProfileForm(ProfileBaseForm):
    class Meta:
        model = StaffProfile
        fields = ['staff_id', 'department', 'role', 'position', 'employee_id', 
                 'date_of_birth', 'phone_number', 'address']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_staff_id(self):
        staff_id = self.cleaned_data.get('staff_id')
        if not staff_id.startswith('STF'):
            raise forms.ValidationError("Staff ID must start with 'STF'")
        return staff_id


class CompleteProfileForm(forms.Form):
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()',
            'style': 'padding: 0.5rem; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; width: 100%;'
        })
    )

    def __init__(self, *args, **kwargs):
        current_type = kwargs.pop('current_type', None)
        super().__init__(*args, **kwargs)
        if current_type:
            self.fields['user_type'].initial = current_type
