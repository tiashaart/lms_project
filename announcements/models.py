from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import UserRole


class AnnouncementVisibility(models.TextChoices):
    ALL = 'all', 'All Users'
    STUDENTS = 'students', 'Students Only'
    INSTRUCTORS = 'instructors', 'Instructors Only'
    ADMINS = 'admins', 'Administrators Only'
    COURSE = 'course', 'Course Enrolled Students'


class Announcement(models.Model):
    """System or course-specific announcement."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements',
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='announcements',
    )
    visibility = models.CharField(
        max_length=20,
        choices=AnnouncementVisibility.choices,
        default=AnnouncementVisibility.ALL,
        db_index=True,
    )
    is_published = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'announcements_announcement'
        ordering = ['-is_pinned', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['visibility', 'is_published']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['course', 'is_published']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @property
    def is_active(self):
        return self.is_published and not self.is_expired

    def is_visible_to(self, user):
        if not self.is_active:
            return False

        if self.visibility == AnnouncementVisibility.ALL:
            return True
        if self.visibility == AnnouncementVisibility.STUDENTS:
            return user.role == UserRole.STUDENT
        if self.visibility == AnnouncementVisibility.INSTRUCTORS:
            return user.role == UserRole.INSTRUCTOR
        if self.visibility == AnnouncementVisibility.ADMINS:
            return user.role == UserRole.ADMIN or user.is_superuser
        if self.visibility == AnnouncementVisibility.COURSE and self.course:
            from courses.models import Enrollment
            return Enrollment.objects.filter(
                student=user, course=self.course, is_active=True,
            ).exists()
        return False
