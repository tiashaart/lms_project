from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ENROLLMENT = 'enrollment', 'Enrollment'
        ASSIGNMENT = 'assignment', 'Assignment'
        COURSE_UPDATE = 'course_update', 'Course Update'
        ANNOUNCEMENT = 'announcement', 'Announcement'
        GRADE = 'grade', 'Grade'
        QUIZ = 'quiz', 'Quiz'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.title}'
