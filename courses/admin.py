from django.contrib import admin

from courses.models import Category, Course, Enrollment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'created_at']
    ordering = ['name']
    readonly_fields = ['slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'instructor', 'level', 'status',
        'price', 'is_free', 'duration_hours', 'created_at',
    ]
    search_fields = ['title', 'description', 'instructor__email']
    list_filter = ['status', 'level', 'is_free', 'category', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['slug', 'published_at', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['instructor', 'category']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'course', 'status', 'progress_percentage',
        'is_active', 'enrolled_at',
    ]
    search_fields = ['student__email', 'course__title']
    list_filter = ['status', 'is_active', 'enrolled_at']
    ordering = ['-enrolled_at']
    readonly_fields = ['enrolled_at', 'completed_at']
    raw_id_fields = ['student', 'course']
