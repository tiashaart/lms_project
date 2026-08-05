from django.db import models
from apps.courses.models import Course
from django.conf import settings


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons_module'
        ordering = ['order']

    def __str__(self):
        return self.title


class Lesson(models.Model):

    class ContentType(models.TextChoices):
        VIDEO = 'video', 'Video'
        TEXT = 'text', 'Text'
        PDF = 'pdf', 'PDF'

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices,
        default=ContentType.TEXT
    )

    text_content = models.TextField(blank=True)

    video = models.FileField(
        upload_to='lessons/videos/',
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to='lessons/pdfs/',
        blank=True,
        null=True
    )

    duration_minutes = models.PositiveIntegerField(default=0)

    order = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(default=False)

    is_free_preview = models.BooleanField(default=False)

    instructor_auth = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'lessons_lesson'
        ordering = ['order']


    def __str__(self):
        return self.title