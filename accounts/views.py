import json
import urllib.request

from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile, CustomUser
from .forms import UserProfileForm, AdminCreationForm
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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/complete_profile.html', {'form': form})


@login_required
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_type = profile.user_type
    return render(request, 'accounts/dashboard.html', {'user_type': user_type})


class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
