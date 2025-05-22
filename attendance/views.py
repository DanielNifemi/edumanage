import base64
import io

import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AttendanceForm, AttendanceReportForm, BulkAttendanceForm, SchoolCalendarForm
from .models import Attendance, AttendanceReport, SchoolCalendar

User = get_user_model()


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            Attendance.check_low_attendance(attendance.student)
            messages.success(request, 'Attendance marked successfully.')
            return redirect('mark_attendance')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/mark_attendance.html', {'form': form})


@login_required
def bulk_mark_attendance(request):
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            student_data = {
                int(key.split('_')[1]): value
                for key, value in form.cleaned_data.items()
                if key.startswith('student_')
            }
            Attendance.mark_bulk_attendance(date, student_data)
            messages.success(request, 'Bulk attendance marked successfully.')
            return redirect('bulk_mark_attendance')
    else:
        form = BulkAttendanceForm()
    return render(request, 'attendance/bulk_mark_attendance.html', {'form': form})


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

            # Create graph
            plt.figure(figsize=(10, 5))
            plt.bar(['Present', 'Absent'], [days_present, total_days - days_present])
            plt.title('Attendance Report')
            plt.ylabel('Number of Days')

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            graph = base64.b64encode(image_png)
            graph = graph.decode('utf-8')

            return render(request, 'attendance/report_result.html', {'report': report, 'graph': graph})
    else:
        form = AttendanceReportForm()
    return render(request, 'attendance/report_form.html', {'form': form})


@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})


@login_required
def manage_school_calendar(request):
    if request.method == 'POST':
        form = SchoolCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added to school calendar.')
            return redirect('manage_school_calendar')
    else:
        form = SchoolCalendarForm()

    events = SchoolCalendar.objects.all().order_by('date')
    return render(request, 'attendance/manage_school_calendar.html', {'form': form, 'events': events})