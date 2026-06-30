import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def validate_assignment_file(value):
    allowed = settings.ALLOWED_DOCUMENT_EXTENSIONS + ['.zip', '.rar']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed:
        raise ValidationError(
            f'Unsupported file format. Allowed: {", ".join(allowed)}'
        )
    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('File size exceeds maximum allowed (50MB).')


def assignment_file_path(instance, filename):
    return f'assignments/{instance.assignment.course.id}/{filename}'


def submission_file_path(instance, filename):
    return f'submissions/{instance.assignment.course.id}/{instance.student.id}/{filename}'


class Assignment(models.Model):
    """Course assignment with due date and grading criteria."""

    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    module = models.ForeignKey(
        'lessons.Module',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assignments',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to=assignment_file_path,
        blank=True,
        null=True,
        validators=[validate_assignment_file],
    )
    max_score = models.PositiveIntegerField(default=100)
    due_date = models.DateTimeField()
    allow_late_submission = models.BooleanField(default=False)
    late_penalty_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignments_assignment'
        ordering = ['due_date']
        indexes = [
            models.Index(fields=['course', 'is_published']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return self.title


class SubmissionStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Submitted'
    GRADED = 'graded', 'Graded'
    RETURNED = 'returned', 'Returned for Revision'
    LATE = 'late', 'Late Submission'


class AssignmentSubmission(models.Model):
    """Student submission for an assignment."""

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignment_submissions',
        limit_choices_to={'role': 'student'},
    )
    submission_file = models.FileField(
        upload_to=submission_file_path,
        validators=[validate_assignment_file],
    )
    text_submission = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.SUBMITTED,
        db_index=True,
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='graded_submissions',
        limit_choices_to={'role': 'instructor'},
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'assignments_submission'
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['assignment', 'status']),
        ]

    def __str__(self):
        return f'{self.student.email} - {self.assignment.title}'
