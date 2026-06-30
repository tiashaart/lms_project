from django.contrib import admin

from announcements.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'visibility', 'course',
        'is_published', 'is_pinned', 'expires_at', 'published_at',
    ]
    search_fields = ['title', 'content', 'author__email']
    list_filter = ['visibility', 'is_published', 'is_pinned', 'published_at']
    ordering = ['-is_pinned', '-published_at']
    readonly_fields = ['published_at', 'created_at', 'updated_at']
    raw_id_fields = ['author', 'course']
