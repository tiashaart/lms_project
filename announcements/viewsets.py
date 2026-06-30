from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from announcements.models import Announcement
from announcements.serializers import AnnouncementSerializer
from users.permissions import IsInstructorOrAdmin


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['visibility', 'is_published', 'is_pinned', 'course']
    search_fields = ['title', 'content']
    ordering_fields = ['published_at', 'created_at', 'expires_at']
    ordering = ['-is_pinned', '-published_at']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()

        if user.role in ('admin',) or user.is_superuser:
            return Announcement.objects.select_related('author', 'course').all()

        if user.role == 'instructor':
            if self.action in ('update', 'partial_update', 'destroy', 'create'):
                return Announcement.objects.filter(author=user)
            visible_ids = []
            for ann in Announcement.objects.filter(is_published=True).exclude(
                expires_at__lt=now,
            ):
                if ann.is_visible_to(user):
                    visible_ids.append(ann.pk)
            return Announcement.objects.filter(pk__in=visible_ids)

        visible_ids = []
        for ann in Announcement.objects.filter(is_published=True).exclude(
            expires_at__lt=now,
        ).select_related('author', 'course'):
            if ann.is_visible_to(user):
                visible_ids.append(ann.pk)
        return Announcement.objects.filter(pk__in=visible_ids).select_related(
            'author', 'course',
        )
