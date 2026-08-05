from rest_framework import serializers

from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model = Announcement
        fields = (
            'id', 'course', 'author', 'author_name', 'title', 'content',
            'is_published', 'created_at', 'updated_at', 'published_at',
        )
        read_only_fields = ('id', 'author', 'is_published', 'created_at', 'updated_at', 'published_at')


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('course', 'title', 'content')
