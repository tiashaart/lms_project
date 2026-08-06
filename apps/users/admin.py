from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import EmailVerificationToken, PasswordResetToken, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'role', 'email_verified', 'is_active')
    list_filter = ('role', 'email_verified', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Hope Academy', {'fields': ('role', 'bio', 'phone', 'profile_picture', 'email_verified')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Hope Academy', {'fields': ('email', 'role')}),
    )


admin.site.register(EmailVerificationToken)
admin.site.register(PasswordResetToken)
