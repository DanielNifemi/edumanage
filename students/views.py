from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, AcademicRecord
from .forms import StudentForm, AcademicRecordForm
from accounts.decorators import role_required


@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    academic_records = student.academic_records.all()
    return render(request, 'students/student_detail.html', {'student': student, 'academic_records': academic_records})


@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, 'Student record created successfully.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record updated successfully.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})


@login_required
def academic_record_create(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        form = AcademicRecordForm(request.POST)
        if form.is_valid():
            academic_record = form.save(commit=False)
            academic_record.student = student
            academic_record.save()
            messages.success(request, 'Academic record added successfully.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = AcademicRecordForm()
    return render(request, 'students/academic_record_form.html', {'form': form, 'student': student})


@login_required
@role_required('student')
def view_grades(request):
    """View for students to see their grades"""
    # Get the current student's academic records
    try:
        student = request.user.student
        academic_records = student.academic_records.all()
    except:
        academic_records = []
    
    context = {
        'academic_records': academic_records
    }
    return render(request, 'students/view_grades.html', context)



