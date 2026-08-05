import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_video_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
        raise ValidationError(
            f'Unsupported video format. Allowed: {", ".join(settings.ALLOWED_VIDEO_EXTENSIONS)}'
        )
    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('Video file size exceeds maximum allowed (50MB).')


def validate_pdf_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in settings.ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError(
            f'Unsupported document format. Allowed: {", ".join(settings.ALLOWED_DOCUMENT_EXTENSIONS)}'
        )
    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('Document file size exceeds maximum allowed (50MB).')


def lesson_video_path(instance, filename):
    return f'courses/{instance.module.course.id}/lessons/videos/{filename}'


def lesson_pdf_path(instance, filename):
    return f'courses/{instance.module.course.id}/lessons/pdfs/{filename}'


class ContentType(models.TextChoices):
    VIDEO = 'video', 'Video'
    PDF = 'pdf', 'PDF'
    TEXT = 'text', 'Text'
    MIXED = 'mixed', 'Mixed'


class Module(models.Model):
    """Course module grouping related lessons."""

    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='modules',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons_module'
        ordering = ['order', 'created_at']
        unique_together = ['course', 'order']
        indexes = [
            models.Index(fields=['course', 'order']),
            models.Index(fields=['course', 'is_published']),
        ]

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Lesson(models.Model):
    """Individual lesson with video, PDF, or text content."""

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content_type = models.CharField(
        max_length=10,
        choices=ContentType.choices,
        default=ContentType.TEXT,
    )
    text_content = models.TextField(blank=True)
    video = models.FileField(
        upload_to=lesson_video_path,
        blank=True,
        null=True,
        validators=[validate_video_file],
    )
    pdf = models.FileField(
        upload_to=lesson_pdf_path,
        blank=True,
        null=True,
        validators=[validate_pdf_file],
    )
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    is_free_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons_lesson'
        ordering = ['order', 'created_at']
        unique_together = ['module', 'order']
        indexes = [
            models.Index(fields=['module', 'order']),
            models.Index(fields=['module', 'is_published']),
        ]

    def __str__(self):
        return self.title

    @property
    def course(self):
        return self.module.course
