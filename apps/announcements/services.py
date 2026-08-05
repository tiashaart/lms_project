from django.utils import timezone

from apps.enrollments.models import Enrollment
from apps.notifications.services import NotificationService

from .models import Announcement


class AnnouncementService:
    @staticmethod
    def publish(announcement):
        announcement.is_published = True
        announcement.published_at = timezone.now()
        announcement.save(update_fields=['is_published', 'published_at', 'updated_at'])

        if announcement.course:
            students = Enrollment.objects.filter(
                course=announcement.course, status=Enrollment.Status.ACTIVE,
            ).select_related('student')
            NotificationService.notify_announcement(
                [e.student for e in students], announcement,
            )
        return announcement
