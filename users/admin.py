from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Student


from users.models import (
    User,
    StudentProfile,
    InstructorProfile,
    AdministratorProfile,
)

admin.site.register(Student)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'role',
        'is_active', 'is_verified', 'created_at',
    ]
    list_filter = ['role', 'is_active', 'is_verified', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio', 'date_of_birth'),
        }),
        ('Role & Status', {
            'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser'),
        }),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name',
                'last_name', 'role', 'is_active',
            ),
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'department', 'academic_level', 'enrollment_date']
    search_fields = ['user__email', 'student_id', 'department']
    list_filter = ['department', 'academic_level', 'enrollment_date']
    ordering = ['-enrollment_date']
    readonly_fields = ['student_id', 'enrollment_date']


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'employee_id', 'department',
        'specialization', 'years_of_experience',
    ]
    search_fields = ['user__email', 'employee_id', 'specialization']
    list_filter = ['department', 'years_of_experience']
    ordering = ['user__email']
    readonly_fields = ['employee_id']


@admin.register(AdministratorProfile)
class AdministratorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'access_level']
    search_fields = ['user__email', 'employee_id']
    list_filter = ['department', 'access_level']
    ordering = ['user__email']
    readonly_fields = ['employee_id']
