from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StaffProfile, LeaveRequest, PerformanceEvaluation
from .forms import StaffProfileForm, LeaveRequestForm, PerformanceEvaluationForm
from accounts.decorators import role_required


@login_required
def staff_profile(request):
    profile, created = StaffProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('staff_profile')
    else:
        form = StaffProfileForm(instance=profile)
    return render(request, 'staff/profile.html', {'form': form})


@login_required
def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.staff = request.user.staffprofile
            leave_request.save()
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'staff/leave_request.html', {'form': form})


@login_required
def leave_list(request):
    leaves = LeaveRequest.objects.filter(staff=request.user.staffprofile)
    return render(request, 'staff/leave_list.html', {'leaves': leaves})


@login_required
def performance_evaluation(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    if request.method == 'POST':
        form = PerformanceEvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.staff = staff
            evaluation.evaluator = request.user
            evaluation.save()
            return redirect('staff_list')
    else:
        form = PerformanceEvaluationForm()
    return render(request, 'staff/performance_evaluation.html', {'form': form, 'staff': staff})


@login_required
def staff_list(request):
    staff_list = StaffProfile.objects.all()
    return render(request, 'staff/staff_list.html', {'staff_list': staff_list})


@login_required
@role_required('staff')
def manage_records(request):
    """View for staff to manage records"""
    return render(request, 'staff/manage_records.html')
