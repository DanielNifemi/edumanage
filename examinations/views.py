from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Exam, ExamResult
from students.models import Student
from teachers.models import Teacher


@login_required
def exam_list(request):
    if request.user.is_teacher:
        exams = Exam.objects.filter(created_by=request.user)
    else:
        exams = Exam.objects.all()
    return render(request, 'examinations/exam_list.html', {'exams': exams})


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam_results = ExamResult.objects.filter(exam=exam)

    if request.user.is_teacher:
        if request.method == 'POST':
            student_id = request.POST.get('student_id')
            score = request.POST.get('score')
            grade_comment = request.POST.get('grade_comment')
            exam_result = get_object_or_404(ExamResult, exam=exam, student_id=student_id)
            exam_result.score = score
            exam_result.is_graded = True
            exam_result.graded_by = request.user
            exam_result.grade_comment = grade_comment
            exam_result.save()
        return render(request, 'examinations/exam_detail.html', {'exam': exam, 'exam_results': exam_results})
    else:
        student_exam_result = ExamResult.objects.get(exam=exam, student=request.user.student)
        return render(request, 'examinations/student_exam_detail.html',
                      {'exam': exam, 'exam_result': student_exam_result})


@login_required
# @user_passes_test(lambda u: u.is_teacher)
def create_exam(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        subject = request.POST.get('subject')
        students = request.POST.getlist('students')
        exam = Exam.objects.create(name=name, date=date, subject=subject, created_by=request.user)
        for student_id in students:
            student = Student.objects.get(id=student_id)
            ExamResult.objects.create(exam=exam, student=student)
        return redirect('examinations:exam_list')
    else:
        students = Student.objects.all()
        return render(request, 'examinations/create_exam.html', {'students': students})
