from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class StudentProgress(models.Model):
    """Tracks student progress within a course."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_progress',
        limit_choices_to={'role': 'student'},
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='student_progress',
    )
    completion_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    completed_lessons = models.ManyToManyField(
        'lessons.Lesson',
        blank=True,
        related_name='completed_by',
    )
    quiz_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    assignment_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    last_accessed_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'progress_student_progress'
        unique_together = ['student', 'course']
        ordering = ['-last_accessed_at']
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['completion_percentage']),
        ]
        verbose_name_plural = 'Student progress records'

    def __str__(self):
        return f'{self.student.email} - {self.course.title} ({self.completion_percentage}%)'
