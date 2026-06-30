from rest_framework import serializers

from progress.models import StudentProgress
from courses.serializers import CourseListSerializer
from lessons.serializers import LessonSerializer


class StudentProgressSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    completed_lesson_details = LessonSerializer(
        source='completed_lessons', many=True, read_only=True,
    )
    completed_lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = StudentProgress
        fields = [
            'id', 'student', 'course', 'completion_percentage',
            'completed_lesson_count', 'completed_lesson_details',
            'quiz_average', 'assignment_average',
            'last_accessed_at', 'started_at', 'completed_at',
        ]
        read_only_fields = [
            'student', 'completion_percentage', 'quiz_average',
            'assignment_average', 'last_accessed_at', 'started_at', 'completed_at',
        ]

    def get_completed_lesson_count(self, obj):
        return obj.completed_lessons.count()


class DashboardStatsSerializer(serializers.Serializer):
    total_enrolled_courses = serializers.IntegerField()
    courses_in_progress = serializers.IntegerField()
    courses_completed = serializers.IntegerField()
    average_completion = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_quiz_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_assignment_score = serializers.DecimalField(max_digits=5, decimal_places=2)
