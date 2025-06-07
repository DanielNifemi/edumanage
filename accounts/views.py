import json
import urllib.request

from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .decorators import role_required, superuser_or_self
from .forms import (
    CustomUserCreationForm, UserProfileForm, AdminCreationForm,
    StudentProfileForm, TeacherProfileForm, StaffProfileForm, CompleteProfileForm
)
from .models import CustomUser, UserProfile
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile
from allauth.account.views import SignupView, LoginView, LogoutView


def index(request):
    response = render(request, 'accounts/login.html')
    response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    return response


def phone_verification(request):
    if request.method == 'POST':
        user_json_url = request.POST.get('user_json_url')

        # Fetch and process user data from the provided URL
        with urllib.request.urlopen(user_json_url) as url:
            data = json.loads(url.read().decode())

        user_country_code = data["user_country_code"]
        user_phone_number = data["user_phone_number"]
        user_first_name = data["user_first_name"]
        user_last_name = data["user_last_name"]

        # Create or update user
        user, created = CustomUser.objects.get_or_create(phone_number=user_phone_number)
        user.first_name = user_first_name
        user.last_name = user_last_name
        user.is_phone_verified = True
        user.save()

        login(request, user)
        return JsonResponse({'success': True, 'redirect': '/dashboard/'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@user_passes_test(lambda u: u.is_admin)
def create_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.is_admin = True
            user.save()
            return redirect('admin:index')
    else:
        form = AdminCreationForm()
    return render(request, 'accounts/create_admin.html', {'form': form})


@login_required
def complete_profile(request):
    try:
        # Get or create the UserProfile
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'user_type': 'student'}
        )

        # Handle user type change
        if request.method == 'POST' and 'user_type' in request.POST:
            type_form = CompleteProfileForm(request.POST)
            if type_form.is_valid():
                new_type = type_form.cleaned_data['user_type']
                if new_type != profile.user_type:
                    profile.user_type = new_type
                    profile.save()
                    # Create the specific profile
                    profile.create_specific_profile()
                    messages.success(request, f'Profile type changed to {new_type}')
                    return redirect('complete_profile')
        
        # Create type selection form
        type_form = CompleteProfileForm(current_type=profile.user_type)

        # Handle specific profile form
        if profile.user_type == 'student':
            specific_profile, created = Student.objects.get_or_create(
                user=request.user,
                defaults={
                    'student_id': f"STU{request.user.id:06d}",
                    'date_of_birth': timezone.now().date(),
                    'grade': 'N/A',
                    'address': 'N/A',
                    'parent_name': 'N/A',
                    'parent_contact': 'N/A'
                }
            )
            form_class = StudentProfileForm
        elif profile.user_type == 'teacher':
            specific_profile, created = Teacher.objects.get_or_create(
                user=request.user,
                defaults={
                    'teacher_id': f"TCH{request.user.id:06d}",
                    'qualification': 'Not set',
                    'years_of_experience': 0
                }
            )
            form_class = TeacherProfileForm
        elif profile.user_type == 'staff':
            specific_profile, created = StaffProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'staff_id': f"STF{request.user.id:06d}",
                    'position': 'Staff Member',
                    'employee_id': f"EMP{request.user.id:06d}",
                    'date_joined': timezone.now().date()
                }
            )
            form_class = StaffProfileForm
        else:
            messages.error(request, "Invalid user type")
            return redirect('dashboard')

        # Handle specific profile form submission
        if request.method == 'POST' and 'user_type' not in request.POST:
            form = form_class(request.POST, instance=specific_profile)
            if form.is_valid():
                form.save()
                messages.success(request, f'{profile.user_type.title()} profile completed successfully.')
                return redirect('dashboard')
        else:
            form = form_class(instance=specific_profile)

        return render(request, 'accounts/complete_profile.html', {
            'form': form,
            'type_form': type_form,
            'profile_type': profile.user_type
        })

    except Exception as e:
        messages.error(request, f"Error accessing profile: {str(e)}")
        return redirect('dashboard')


@login_required
@superuser_or_self
def edit_profile(request, profile_type):
    if profile_type not in ['student', 'teacher', 'staff']:
        messages.error(request, "Invalid profile type")
        return redirect('dashboard')
    
    # Get the appropriate profile based on type
    if profile_type == 'student':
        profile = get_object_or_404(Student, user=request.user)
        form_class = StudentProfileForm
    elif profile_type == 'teacher':
        profile = get_object_or_404(Teacher, user=request.user)
        form_class = TeacherProfileForm
    else: # staff
        profile = get_object_or_404(StaffProfile, user=request.user)
        form_class = StaffProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your {profile_type} profile has been updated successfully.")
            return redirect('dashboard')
    else:
        form = form_class(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile_type': profile_type
    })


@login_required
def dashboard(request):
    context = {}
    try:
        user_profile = request.user.userprofile
        context['user_type'] = user_profile.user_type
    except UserProfile.DoesNotExist:
        # Create a default UserProfile if it doesn't exist
        user_profile = UserProfile.objects.create(
            user=request.user,
            user_type='student'  # Default to student
        )
        context['user_type'] = user_profile.user_type
    
    context['is_superuser'] = request.user.is_superuser

    # Get relevant profiles
    student_profile = None
    teacher_profile = None
    staff_profile = None

    if context['is_superuser']:
        student_profile = Student.objects.filter(user=request.user).first()
        teacher_profile = Teacher.objects.filter(user=request.user).first()
        staff_profile = StaffProfile.objects.filter(user=request.user).first()

        context.update({
            'student_profile': student_profile,
            'teacher_profile': teacher_profile,
            'staff_profile': staff_profile,
            'available_roles': [role for role, _ in UserProfile.USER_TYPES]
        })
      # Load course information based on user type
    try:
        if user_profile.user_type == 'teacher':
            teacher = getattr(request.user, 'teacher', None)
            if teacher:
                context['courses'] = teacher.courses_taught.all().prefetch_related('students')
        elif user_profile.user_type == 'student':
            student = getattr(request.user, 'student', None)
            if student:
                context['enrollments'] = student.courseenrollment_set.select_related('course').all()
    except Exception as e:
        # Log the error but don't crash the dashboard
        print(f"Error loading course information: {e}")
    
    return render(request, 'accounts/dashboard.html', context)


class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.user
        
        # Create UserProfile with selected type
        profile = UserProfile.objects.create(
            user=user,
            user_type=form.cleaned_data['user_type']
        )
        
        # Create the specific profile
        profile.create_specific_profile()
        
        # Redirect to profile completion
        return redirect('complete_profile')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class StudentLoginView(LoginView):
    template_name = 'accounts/login_student.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = 'student'
        context['role_title'] = 'Student Portal'
        context['role_description'] = 'Access your courses, grades, and assignments'
        context['role_color'] = '#4285f4'  # Blue
        return context


class TeacherLoginView(LoginView):
    template_name = 'accounts/login_teacher.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = 'teacher'
        context['role_title'] = 'Teacher Portal'
        context['role_description'] = 'Manage your classes, grade assignments, and track student progress'
        context['role_color'] = '#34a853'  # Green
        return context


class StaffLoginView(LoginView):
    template_name = 'accounts/login_staff.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = 'staff'
        context['role_title'] = 'Staff Portal'
        context['role_description'] = 'Administrative access to manage school operations'
        context['role_color'] = '#fbbc04'  # Yellow
        return context


class AdminLoginView(LoginView):
    template_name = 'accounts/login_admin.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = 'admin'
        context['role_title'] = 'Administrator Portal'
        context['role_description'] = 'Complete system access and management'
        context['role_color'] = '#ea4335'  # Red
        return context


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    template_name = 'accounts/logout.html'
    
    def get_success_url(self):
        return '/'  # Redirect to home page after logout


@login_required
@user_passes_test(lambda u: u.is_superuser)
def switch_role(request, role):
    if role not in dict(UserProfile.USER_TYPES):
        messages.error(request, "Invalid role selected.")
        return redirect('dashboard')
    
    try:
        # Get or create the UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        
        # Update the user type
        profile.user_type = role
        profile.save()
        
        # Create role-specific profile if it doesn't exist
        if role == 'student':
            Student.objects.get_or_create(
                user=request.user,
                defaults={
                    'student_id': f"STU{request.user.id:06d}",
                    'date_of_birth': timezone.now().date(),
                    'grade': 'N/A',
                    'address': 'N/A',
                    'parent_name': 'N/A',
                    'parent_contact': 'N/A'
                }
            )
        elif role == 'teacher':
            Teacher.objects.get_or_create(
                user=request.user,
                defaults={
                    'teacher_id': f"TCH{request.user.id:06d}",
                    'subjects': 'Not set',
                    'qualification': 'Not set',
                    'department': 'Not set',
                    'date_joined': timezone.now().date()
                }
            )
        elif role == 'staff':
            StaffProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'staff_id': f"STF{request.user.id:06d}",
                    'department': 'Not set',
                    'position': 'Not set',
                    'date_joined': timezone.now().date()
                }
            )
        
        messages.success(request, f"Successfully switched to {role} role.")
        
    except Exception as e:
        messages.error(request, f"An error occurred while switching roles: {str(e)}")
        return redirect('dashboard')
    
    return redirect('dashboard')


@role_required('teacher')
def grade_assignments(request):
    return render(request, 'teachers/grade_assignments.html')


@role_required('staff')
def manage_records(request):
    return render(request, 'staff/manage_records.html')


@role_required('student')
def view_grades(request):
    return render(request, 'students/view_grades.html')
