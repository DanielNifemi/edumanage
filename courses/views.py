from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.utils import timezone
from .models import Course, CourseContent, Assignment, AssignmentSubmission, CourseEnrollment
from .forms import (CourseForm, CourseContentForm, AssignmentForm, 
                   AssignmentSubmissionForm, GradeAssignmentForm)
from accounts.decorators import role_required

@login_required
def course_list(request):
    """List all courses for students/teachers"""
    if hasattr(request.user, 'teacher'):
        # For teachers, show courses they teach
        courses = Course.objects.filter(instructor=request.user.teacher)
    else:
        # For students, show enrolled courses
        enrollments = CourseEnrollment.objects.filter(
            student=request.user.student,
            is_active=True
        ).select_related('course')
        courses = [enrollment.course for enrollment in enrollments]
    
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
@role_required('teacher')
def course_create(request):
    """Create a new course (teachers only)"""
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.teacher
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def course_detail(request, pk):
    """View course details"""
    course = get_object_or_404(Course, pk=pk)
    now = timezone.now()
    contents = CourseContent.objects.filter(course=course).order_by('-created_at')
    
    context = {
        'course': course,
        'contents': contents,
        'now': now
    }
    
    if hasattr(request.user, 'teacher'):
        # Additional context for teachers
        context['is_instructor'] = request.user.teacher == course.instructor
        if context['is_instructor']:
            context['enrolled_students'] = course.students.all()
            
            # Get all assignments and their submission stats
            assignments = Assignment.objects.filter(content__course=course)
            assignment_stats = []
            for assignment in assignments:
                submissions = AssignmentSubmission.objects.filter(assignment=assignment)
                graded = submissions.exclude(grade=None).count()
                total = submissions.count()
                assignment_stats.append({
                    'assignment': assignment,
                    'submissions': total,
                    'graded': graded,
                })
            context['assignment_stats'] = assignment_stats
            
    elif hasattr(request.user, 'student'):
        # Check if student is enrolled
        context['is_enrolled'] = CourseEnrollment.objects.filter(
            student=request.user.student,
            course=course,
            is_active=True
        ).exists()
        
        if context['is_enrolled']:
            # Get assignment submission status for the student
            assignments = Assignment.objects.filter(content__course=course)
            student_submissions = []
            for assignment in assignments:
                submission = AssignmentSubmission.objects.filter(
                    assignment=assignment,
                    student=request.user.student
                ).first()
                student_submissions.append({
                    'assignment': assignment,
                    'submission': submission,
                })
            context['student_submissions'] = student_submissions
        
    return render(request, 'courses/course_detail.html', context)

@login_required
@role_required('student')
def course_enroll(request, pk):
    """Enroll in a course (students only)"""
    course = get_object_or_404(Course, pk=pk)
    if not course.is_active:
        messages.error(request, 'This course is not currently open for enrollment.')
        return redirect('course_detail', pk=course.pk)
    
    enrollment, created = CourseEnrollment.objects.get_or_create(
        student=request.user.student,
        course=course,
        defaults={'is_active': True}
    )
    
    if not created and not enrollment.is_active:
        enrollment.is_active = True
        enrollment.save()
        messages.success(request, f'Welcome back to {course.name}!')
    else:
        messages.success(request, f'Successfully enrolled in {course.name}!')
    
    return redirect('course_detail', pk=course.pk)

@login_required
@role_required('student')
def course_drop(request, pk):
    """Drop a course (students only)"""
    enrollment = get_object_or_404(
        CourseEnrollment,
        student=request.user.student,
        course_id=pk,
        is_active=True
    )
    enrollment.is_active = False
    enrollment.save()
    messages.success(request, f'Successfully dropped {enrollment.course.name}')
    return redirect('course_list')

@login_required
@role_required('teacher')
def content_create(request, course_pk):
    """Add course content or assignment (teachers only)"""
    course = get_object_or_404(Course, pk=course_pk)
    if request.user.teacher != course.instructor:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        content_form = CourseContentForm(request.POST, request.FILES)
        assignment_form = AssignmentForm(request.POST)
        
        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.course = course
            content.save()
            
            # If it's an assignment, save assignment details
            if content.content_type == 'ASSIGNMENT' and assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.content = content
                assignment.save()
            
            messages.success(request, 'Content added successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        content_form = CourseContentForm()
        assignment_form = AssignmentForm()
        
    return render(request, 'courses/content_form.html', {
        'content_form': content_form,
        'assignment_form': assignment_form,
        'course': course
    })

@login_required
def assignment_detail(request, pk):
    """View assignment details and handle submission"""
    content = get_object_or_404(CourseContent, pk=pk, content_type='ASSIGNMENT')
    assignment = content.assignment
    course = content.course
    
    if not hasattr(request.user, 'student'):
        context = {
            'assignment': assignment,
            'submissions': AssignmentSubmission.objects.filter(assignment=assignment)
        }
        template = 'courses/assignment_teacher_view.html'
    else:
        submission = AssignmentSubmission.objects.filter(
            assignment=assignment,
            student=request.user.student
        ).first()
        
        if request.method == 'POST' and not submission:
            form = AssignmentSubmissionForm(
                request.POST, 
                request.FILES,
                submission_type=assignment.submission_type
            )
            if form.is_valid():
                submission = form.save(commit=False)
                submission.assignment = assignment
                submission.student = request.user.student
                submission.save()
                messages.success(request, 'Assignment submitted successfully!')
                return redirect('assignment_detail', pk=pk)
        else:
            form = AssignmentSubmissionForm(
                submission_type=assignment.submission_type,
                instance=submission
            )
        
        context = {
            'assignment': assignment,
            'form': form,
            'submission': submission
        }
        template = 'courses/assignment_student_view.html'
    
    return render(request, template, context)

@login_required
@role_required('teacher')
def grade_assignment(request, submission_pk):
    """Grade a student's assignment submission (teachers only)"""
    submission = get_object_or_404(AssignmentSubmission, pk=submission_pk)
    if request.user.teacher != submission.assignment.content.course.instructor:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = GradeAssignmentForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade submitted successfully!')
            return redirect('assignment_detail', pk=submission.assignment.content.pk)
    else:
        form = GradeAssignmentForm(instance=submission)
    
    return render(request, 'courses/grade_form.html', {
        'form': form,
        'submission': submission
    })
