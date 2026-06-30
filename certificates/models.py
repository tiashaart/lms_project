import uuid

from django.conf import settings
from django.db import models


def certificate_pdf_path(instance, filename):
    return f'certificates/{instance.course.id}/{instance.certificate_number}.pdf'


class Certificate(models.Model):
    """Course completion certificate."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates',
        limit_choices_to={'role': 'student'},
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='certificates',
    )
    certificate_number = models.CharField(max_length=50, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to=certificate_pdf_path, blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    revoke_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'certificates_certificate'
        unique_together = ['student', 'course']
        ordering = ['-issued_at']
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['certificate_number']),
        ]

    def __str__(self):
        return f'{self.certificate_number} - {self.student.email}'

    @staticmethod
    def generate_certificate_number():
        return f'HALMS-CERT-{uuid.uuid4().hex[:12].upper()}'
