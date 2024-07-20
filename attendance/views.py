from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Attendance, AttendanceReport
from .forms import AttendanceForm, AttendanceReportForm


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance marked successfully.')
            return redirect('mark_attendance')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/mark_attendance.html', {'form': form})


@login_required
def attendance_report(request):
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            student = form.cleaned_data['student']

            attendances = Attendance.objects.filter(
                student=student,
                date__range=[start_date, end_date]
            )

            total_days = (end_date - start_date).days + 1
            days_present = attendances.filter(is_present=True).count()

            report = AttendanceReport.create_report(
                student=student,
                start_date=start_date,
                end_date=end_date,
                total_days=total_days,
                days_present=days_present
            )

            return render(request, 'attendance/report_result.html', {'report': report})
    else:
        form = AttendanceReportForm()
    return render(request, 'attendance/report_form.html', {'form': form})


@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})