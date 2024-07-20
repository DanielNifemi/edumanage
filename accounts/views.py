from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile, CustomUser
from .forms import UserProfileForm, AdminCreationForm
from allauth.account.views import SignupView, LoginView, LogoutView


@login_required
def home(request):
    return render(request, 'accounts/home.html')


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
