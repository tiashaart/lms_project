from django.contrib import admin

from .models import Module, Lesson


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "order",
        "created_at",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "module",
        "content_type",
        "duration_minutes",
        "is_published",
        "created_at",
    )

    list_filter = (
        "content_type",
        "is_published",
    )

    search_fields = (
        "title",
        "description",
    )