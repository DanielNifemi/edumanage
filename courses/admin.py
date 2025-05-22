from django.contrib import admin
from .models import Course, CourseContent, Assignment, AssignmentSubmission, CourseEnrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name', 'instructor', 'semester', 'year', 'is_active')
    list_filter = ('semester', 'year', 'is_active')
    search_fields = ('course_code', 'name', 'instructor__user__username')

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'content_type', 'created_at')
    list_filter = ('content_type', 'course')
    search_fields = ('title', 'description', 'course__name')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_course', 'total_points', 'submission_type')
    search_fields = ('content__title', 'content__course__name')
    
    def get_title(self, obj):
        return obj.content.title
    get_title.short_description = 'Title'
    
    def get_course(self, obj):
        return obj.content.course
    get_course.short_description = 'Course'

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_assignment', 'submitted_at', 'grade')
    list_filter = ('submitted_at', 'assignment__content__course')
    search_fields = ('student__user__username', 'assignment__content__title')
    
    def get_assignment(self, obj):
        return obj.assignment.content.title
    get_assignment.short_description = 'Assignment'

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled', 'is_active')
    list_filter = ('is_active', 'course', 'date_enrolled')
    search_fields = ('student__user__username', 'course__name')
