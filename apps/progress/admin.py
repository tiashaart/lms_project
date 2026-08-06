from django.contrib import admin
from .models import StudentProgress


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "course",
        "completion_percentage",
        "quiz_average",
        "assignment_average",
        "last_accessed_at",
        "started_at",
        "completed_at",
    )

    list_filter = (
        "course",
        "completed_at",
    )

    search_fields = (
        "student__email",
        "course__title",
    )

    ordering = (
        "-last_accessed_at",
    )
