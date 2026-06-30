from django.contrib import admin

from assignments.models import Assignment, AssignmentSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'course', 'max_score', 'due_date',
        'is_published', 'allow_late_submission',
    ]
    search_fields = ['title', 'course__title']
    list_filter = ['is_published', 'allow_late_submission', 'due_date']
    ordering = ['due_date']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['course', 'module']


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'assignment', 'status', 'score',
        'submitted_at', 'graded_at',
    ]
    search_fields = ['student__email', 'assignment__title']
    list_filter = ['status', 'submitted_at', 'graded_at']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at', 'graded_at']
    raw_id_fields = ['student', 'assignment', 'graded_by']
