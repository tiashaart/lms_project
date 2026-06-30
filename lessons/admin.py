from django.contrib import admin

from lessons.models import Module, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ['order']
    fields = ['title', 'content_type', 'order', 'is_published', 'duration_minutes']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_published', 'created_at']
    search_fields = ['title', 'course__title']
    list_filter = ['is_published', 'created_at']
    ordering = ['course', 'order']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['course']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'module', 'content_type', 'order',
        'is_published', 'is_free_preview', 'duration_minutes',
    ]
    search_fields = ['title', 'module__title', 'module__course__title']
    list_filter = ['content_type', 'is_published', 'is_free_preview']
    ordering = ['module', 'order']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['module']
