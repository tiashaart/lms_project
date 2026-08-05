from rest_framework import serializers

from lessons.models import Module, Lesson, ContentType


class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='module.course_id', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'course_id', 'title', 'description',
            'content_type', 'text_content', 'video', 'pdf',
            'duration_minutes', 'order', 'is_published',
            'is_free_preview', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'module', 'title', 'description', 'content_type',
            'text_content', 'video', 'pdf', 'duration_minutes',
            'order', 'is_published', 'is_free_preview',
        ]

    def validate(self, attrs):
        content_type = attrs.get('content_type', ContentType.TEXT)
        if content_type == ContentType.VIDEO and not attrs.get('video'):
            if not (self.instance and self.instance.video):
                raise serializers.ValidationError({'video': 'Video file is required.'})
        if content_type == ContentType.PDF and not attrs.get('pdf'):
            if not (self.instance and self.instance.pdf):
                raise serializers.ValidationError({'pdf': 'PDF file is required.'})
        return attrs


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Module
        fields = [
            'id', 'course', 'course_title', 'title', 'description',
            'order', 'is_published', 'lessons', 'lesson_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class ModuleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['course', 'title', 'description', 'order', 'is_published']
