from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Teacher, Subject, Class, Lesson
from .forms import TeacherProfileForm, LessonForm


@login_required
def teacher_profile(request):
    teacher = get_object_or_404(Teacher, staff_profile__user=request.user)
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_profile')
    else:
        form = TeacherProfileForm(instance=teacher)
    return render(request, 'teachers/profile.html', {'form': form, 'teacher': teacher})


@login_required
def teacher_subjects(request):
    teacher = get_object_or_404(Teacher, staff_profile__user=request.user)
    subjects = teacher.subjects.all()
    return render(request, 'teachers/subjects.html', {'subjects': subjects})


@login_required
def teacher_classes(request):
    teacher = get_object_or_404(Teacher, staff_profile__user=request.user)
    classes = teacher.classes.all()
    return render(request, 'teachers/classes.html', {'classes': classes})


@login_required
def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher = request.user.staffprofile.teacher
            lesson.save()
            return redirect('teacher_lessons')
    else:
        form = LessonForm()
    return render(request, 'teachers/add_lesson.html', {'form': form})


@login_required
def teacher_lessons(request):
    teacher = get_object_or_404(Teacher, staff_profile__user=request.user)
    lessons = Lesson.objects.filter(teacher=teacher)
    return render(request, 'teachers/lessons.html', {'lessons': lessons})


@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, teacher=request.user.staffprofile.teacher)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('teacher_lessons')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'teachers/edit_lesson.html', {'form': form, 'lesson': lesson})
