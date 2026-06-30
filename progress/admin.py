from django.contrib import admin

from progress.models import StudentProgress


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'course', 'completion_percentage',
        'quiz_average', 'assignment_average', 'last_accessed_at',
    ]
    search_fields = ['student__email', 'course__title']
    list_filter = ['completion_percentage', 'last_accessed_at']
    ordering = ['-last_accessed_at']
    readonly_fields = ['started_at', 'completed_at', 'last_accessed_at']
    raw_id_fields = ['student', 'course']
    filter_horizontal = ['completed_lessons']
