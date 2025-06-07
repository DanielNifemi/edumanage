from django.contrib import admin
from .models import (
    Course, CourseEnrollment, CourseContent, Assignment,
    AssignmentSubmission, CourseAnnouncement
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'instructor', 'difficulty_level', 'status', 'start_date', 'enrollment_count']
    list_filter = ['subject', 'difficulty_level', 'status', 'start_date']
    search_fields = ['title', 'description', 'subject__name', 'instructor__user__first_name']
    readonly_fields = ['enrollment_count', 'completion_rate', 'created_at', 'updated_at']
    filter_horizontal = ['prerequisites']
    date_hierarchy = 'start_date'
    ordering = ['-created_at']


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date_enrolled', 'is_active', 'progress_percentage', 'completion_date']
    list_filter = ['is_active', 'date_enrolled', 'course__subject']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'course__title']
    readonly_fields = ['date_enrolled', 'is_completed']
    date_hierarchy = 'date_enrolled'
    ordering = ['-date_enrolled']


@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'is_required', 'created_at']
    list_filter = ['content_type', 'is_required', 'course__subject']
    search_fields = ['title', 'description', 'course__title']
    ordering = ['course', 'order']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['content', 'due_date', 'total_points', 'submission_type', 'is_overdue']
    list_filter = ['submission_type', 'allow_late_submission', 'due_date']
    search_fields = ['content__title', 'content__course__title', 'instructions']
    readonly_fields = ['is_overdue']
    date_hierarchy = 'due_date'
    ordering = ['due_date']


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'grade', 'is_late', 'is_graded']
    list_filter = ['submitted_at', 'graded_at', 'assignment__submission_type']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'assignment__content__title']
    readonly_fields = ['submitted_at', 'is_late', 'is_graded']
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']


@admin.register(CourseAnnouncement)
class CourseAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_by', 'created_at', 'is_pinned']
    list_filter = ['is_pinned', 'created_at', 'course__subject']
    search_fields = ['title', 'content', 'course__title']
    ordering = ['-is_pinned', '-created_at']
