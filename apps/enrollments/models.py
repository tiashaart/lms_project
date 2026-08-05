from django.conf import settings
from django.db import models
from apps.courses.models import Course


class EnrollmentStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    COMPLETED = 'completed', 'Completed'
    DROPPED = 'dropped', 'Dropped'
    SUSPENDED = 'suspended', 'Suspended'


class Enrollment(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.ACTIVE
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = 'courses_enrollment'
        ordering = ['-enrolled_at']
        unique_together = ['student', 'course']


    def __str__(self):
        return f'{self.student.email} - {self.course.title}'