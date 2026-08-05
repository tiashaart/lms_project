from rest_framework import serializers

from core.validators import validate_assignment_file
from .models import Assignment, AssignmentSubmission


class AssignmentSerializer(serializers.ModelSerializer):
    is_past_due = serializers.BooleanField(read_only=True)
    submission_count = serializers.IntegerField(source='submissions.count', read_only=True)

    class Meta:
        model = Assignment
        fields = (
            'id', 'course', 'title', 'description', 'due_date',
            'max_score', 'is_past_due', 'submission_count', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('course', 'title', 'description', 'due_date', 'max_score')

    def validate_due_date(self, value):
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError('Due date must be in the future.')
        return value


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = (
            'id', 'assignment', 'student', 'student_email', 'file', 'text_submission',
            'submitted_at', 'grade', 'feedback', 'status', 'graded_at',
        )
        read_only_fields = ('id', 'student', 'submitted_at', 'grade', 'feedback', 'status', 'graded_at')


class SubmitAssignmentSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    text_submission = serializers.CharField(required=False, allow_blank=True)

    def validate_file(self, value):
        if value:
            validate_assignment_file(value)
        return value

    def validate(self, attrs):
        if not attrs.get('file') and not attrs.get('text_submission'):
            raise serializers.ValidationError('Provide a file or text submission.')
        return attrs


class GradeSubmissionSerializer(serializers.Serializer):
    grade = serializers.DecimalField(max_digits=5, decimal_places=2)
    feedback = serializers.CharField(required=False, allow_blank=True)
