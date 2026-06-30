from django.utils import timezone
from rest_framework import serializers

from assignments.models import Assignment, AssignmentSubmission, SubmissionStatus
from users.serializers import UserSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = [
            'id', 'course', 'course_title', 'module', 'title',
            'description', 'instructions', 'attachment', 'max_score',
            'due_date', 'allow_late_submission', 'late_penalty_percent',
            'is_published', 'submission_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_submission_count(self, obj):
        return obj.submissions.count()


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    graded_by_name = serializers.CharField(
        source='graded_by.full_name', read_only=True, default=None,
    )

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'assignment_title', 'student',
            'submission_file', 'text_submission', 'status', 'score',
            'feedback', 'graded_by', 'graded_by_name',
            'submitted_at', 'graded_at',
        ]
        read_only_fields = [
            'student', 'status', 'score', 'feedback',
            'graded_by', 'graded_at', 'submitted_at',
        ]


class AssignmentSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'submission_file', 'text_submission']

    def validate(self, attrs):
        assignment = attrs['assignment']
        if not assignment.is_published:
            raise serializers.ValidationError(
                {'assignment': 'Assignment is not published.'}
            )
        now = timezone.now()
        if now > assignment.due_date and not assignment.allow_late_submission:
            raise serializers.ValidationError(
                {'assignment': 'Due date has passed and late submissions are not allowed.'}
            )
        return attrs

    def create(self, validated_data):
        assignment = validated_data['assignment']
        now = timezone.now()
        status_val = SubmissionStatus.SUBMITTED
        if now > assignment.due_date:
            status_val = SubmissionStatus.LATE

        submission, _ = AssignmentSubmission.objects.update_or_create(
            assignment=assignment,
            student=self.context['request'].user,
            defaults={
                **validated_data,
                'status': status_val,
            },
        )
        return submission


class GradeSubmissionSerializer(serializers.Serializer):
    score = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0)
    feedback = serializers.CharField(required=False, allow_blank=True)

    def validate_score(self, value):
        submission = self.context['submission']
        if value > submission.assignment.max_score:
            raise serializers.ValidationError(
                f'Score cannot exceed maximum ({submission.assignment.max_score}).'
            )
        return value
