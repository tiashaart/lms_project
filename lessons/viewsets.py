from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from courses.models import Enrollment
from lessons.models import Module, Lesson
from lessons.serializers import (
    ModuleSerializer,
    ModuleCreateUpdateSerializer,
    LessonSerializer,
    LessonCreateUpdateSerializer,
)
from users.permissions import IsInstructorOrAdmin, IsInstructorOfCourse


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.select_related('course').prefetch_related('lessons').all()
    filterset_fields = ['course', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ModuleCreateUpdateSerializer
        return ModuleSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsInstructorOrAdmin()]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        course_id = self.request.query_params.get('course')

        if not user.is_authenticated:
            return queryset.filter(is_published=True)

        if user.role == 'student':
            enrolled_course_ids = Enrollment.objects.filter(
                student=user, is_active=True,
            ).values_list('course_id', flat=True)
            return queryset.filter(
                models.Q(is_published=True, course_id__in=enrolled_course_ids)
                | models.Q(course__lessons__is_free_preview=True)
            ).distinct()

        if user.role == 'instructor':
            return queryset.filter(course__instructor=user)

        return queryset


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('module__course').all()
    filterset_fields = ['module', 'content_type', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return LessonCreateUpdateSerializer
        return LessonSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsInstructorOrAdmin()]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == 'student':
            enrolled_course_ids = Enrollment.objects.filter(
                student=user, is_active=True,
            ).values_list('course_id', flat=True)
            return queryset.filter(
                models.Q(module__course_id__in=enrolled_course_ids, is_published=True)
                | models.Q(is_free_preview=True, is_published=True)
            )

        if user.role == 'instructor':
            return queryset.filter(module__course__instructor=user)

        return queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        """Mark lesson as completed for the current student."""
        from progress.services import ProgressService

        lesson = self.get_object()
        progress = ProgressService.mark_lesson_complete(request.user, lesson)
        return Response({
            'detail': 'Lesson marked as complete.',
            'progress_percentage': str(progress.completion_percentage),
        })
