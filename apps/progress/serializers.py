from rest_framework import serializers

from .models import StudentProgress


class StudentProgressSerializer(serializers.ModelSerializer):

    course_title = serializers.CharField(
        source="course.title",
        read_only=True
    )

    lesson_title = serializers.CharField(
        source="lesson.title",
        read_only=True
    )

    class Meta:
        model = StudentProgress

        fields = [
            "id",
            "course",
            "course_title",
            "lesson",
            "lesson_title",
            "completed",
            "progress_percentage",
            "last_accessed",
            "completed_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "course_title",
            "lesson_title",
            "progress_percentage",
            "last_accessed",
            "completed_at",
            "created_at",
            "updated_at",
        ]


class MarkCompleteSerializer(serializers.Serializer):

    lesson_id = serializers.IntegerField()