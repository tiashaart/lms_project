from django.utils import timezone
from rest_framework import serializers

from announcements.models import Announcement
from users.serializers import UserSerializer


class AnnouncementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    course_title = serializers.CharField(
        source='course.title', read_only=True, default=None,
    )

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'author', 'course', 'course_title',
            'visibility', 'is_published', 'is_pinned',
            'published_at', 'expires_at', 'is_expired', 'is_active',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['author', 'published_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        if validated_data.get('is_published'):
            validated_data['published_at'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('is_published') and not instance.published_at:
            validated_data['published_at'] = timezone.now()
        return super().update(instance, validated_data)
