from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DisciplinaryRecord, BehaviorNote, Student
from .forms import DisciplinaryRecordForm, BehaviorNoteForm


@login_required
def student_discipline_record(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    records = DisciplinaryRecord.objects.filter(student=student).order_by('-date')
    notes = BehaviorNote.objects.filter(student=student).order_by('-date')
    return render(request, 'discipline/student_record.html', {
        'student': student,
        'records': records,
        'notes': notes
    })


@login_required
def add_disciplinary_record(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = DisciplinaryRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.student = student
            record.reported_by = request.user
            record.save()
            return redirect('student_discipline_record', student_id=student.id)
    else:
        form = DisciplinaryRecordForm()
    return render(request, 'discipline/add_record.html', {'form': form, 'student': student})


@login_required
def add_behavior_note(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = BehaviorNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.student = student
            note.noted_by = request.user
            note.save()
            return redirect('student_discipline_record', student_id=student.id)
    else:
        form = BehaviorNoteForm()
    return render(request, 'discipline/add_note.html', {'form': form, 'student': student})


@login_required
def discipline_dashboard(request):
    recent_records = DisciplinaryRecord.objects.order_by('-date')[:10]
    return render(request, 'discipline/dashboard.html', {'recent_records': recent_records})
