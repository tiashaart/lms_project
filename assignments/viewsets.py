from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from assignments.models import Assignment, AssignmentSubmission, SubmissionStatus
from assignments.serializers import (
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    AssignmentSubmissionCreateSerializer,
    GradeSubmissionSerializer,
)
from users.permissions import IsInstructorOrAdmin, IsStudent


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('course', 'module').all()
    serializer_class = AssignmentSerializer
    filterset_fields = ['course', 'module', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['due_date']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return self.queryset.filter(course__instructor=user)
        if user.role == 'student':
            from courses.models import Enrollment
            enrolled_ids = Enrollment.objects.filter(
                student=user, is_active=True,
            ).values_list('course_id', flat=True)
            return self.queryset.filter(
                course_id__in=enrolled_ids, is_published=True,
            )
        return self.queryset


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    filterset_fields = ['assignment', 'status']
    ordering_fields = ['submitted_at', 'score']
    ordering = ['-submitted_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentSubmissionCreateSerializer
        return AssignmentSubmissionSerializer

    def get_permissions(self):
        if self.action == 'grade':
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        if self.action == 'create':
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = AssignmentSubmission.objects.select_related(
            'student', 'assignment', 'graded_by',
        )
        if user.role in ('admin',) or user.is_superuser:
            return qs.all()
        if user.role == 'instructor':
            return qs.filter(assignment__course__instructor=user)
        return qs.filter(student=user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], url_path='grade')
    def grade(self, request, pk=None):
        submission = self.get_object()
        serializer = GradeSubmissionSerializer(
            data=request.data,
            context={'submission': submission},
        )
        serializer.is_valid(raise_exception=True)

        submission.score = serializer.validated_data['score']
        submission.feedback = serializer.validated_data.get('feedback', '')
        submission.status = SubmissionStatus.GRADED
        submission.graded_by = request.user
        submission.graded_at = timezone.now()
        submission.save()

        from progress.services import ProgressService
        ProgressService.update_assignment_average(
            submission.student, submission.assignment.course,
        )

        return Response(AssignmentSubmissionSerializer(submission).data)
