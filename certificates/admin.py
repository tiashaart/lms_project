from django.contrib import admin

from certificates.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = [
        'certificate_number', 'student', 'course',
        'issued_at', 'is_valid',
    ]
    search_fields = ['certificate_number', 'student__email', 'course__title']
    list_filter = ['is_valid', 'issued_at']
    ordering = ['-issued_at']
    readonly_fields = ['certificate_number', 'issued_at', 'revoked_at']
    raw_id_fields = ['student', 'course']
