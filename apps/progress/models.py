from django.conf import settings
from django.db import models

from apps.courses.models import Course


class StudentProgress(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_progress",
        db_column="student_id",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="student_progress",
        db_column="course_id",
    )

    completion_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    quiz_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    assignment_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    last_accessed_at = models.DateTimeField(
        auto_now=True,
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "progress_student_progress"
        ordering = ["-last_accessed_at"]

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"