from django.conf import settings
from django.db import models

from apps.courses.models import Course


class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
