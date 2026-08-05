from rest_framework import serializers

from apps.courses.serializers import CourseListSerializer
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):

    course = CourseListSerializer(
        read_only=True
    )

    class Meta:
        model = Enrollment

        fields = (
            "id",
            "course",
            "is_active",
            "enrolled_at",
            "completed_at",
        )

        read_only_fields = (
            "id",
            "enrolled_at",
            "completed_at",
        )


class EnrollRequestSerializer(serializers.Serializer):

    course_id = serializers.IntegerField()