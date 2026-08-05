from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.courses.models import Course


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignments_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignments'
        ordering = ['due_date']

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return timezone.now() > self.due_date


class AssignmentSubmission(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        GRADED = 'graded', 'Graded'
        LATE = 'late', 'Late'

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignment_submissions',
        limit_choices_to={'role': 'student'},
    )
    file = models.FileField(upload_to='assignment_submissions/', blank=True, null=True)
    text_submission = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='graded_submissions',
    )

    class Meta:
        db_table = 'assignment_submissions'
        unique_together = [('assignment', 'student')]
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.student.email} - {self.assignment.title}'
