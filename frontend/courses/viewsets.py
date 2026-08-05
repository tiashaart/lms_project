from django.db import models
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from courses.models import Category, Course, Enrollment, CourseStatus, EnrollmentStatus
from courses.serializers import (
    CategorySerializer,
    CourseListSerializer,
    CourseDetailSerializer,
    CourseCreateUpdateSerializer,
    EnrollmentSerializer,
)
from users.permissions import IsInstructor, IsInstructorOrAdmin, IsStudent, IsAdministrator


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdministrator()]


class CourseFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_free = filters.BooleanFilter()
    category = filters.NumberFilter(field_name='category_id')

    class Meta:
        model = Course
        fields = ['category', 'level', 'status', 'is_free', 'instructor']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('category', 'instructor').all()
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'title', 'price', 'published_at']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if self.action in ('list', 'retrieve') and (
            not user.is_authenticated
            or user.role == 'student'
        ):
            return queryset.filter(status=CourseStatus.PUBLISHED)

        if user.is_authenticated and user.role == 'instructor':
            if self.action in ('list', 'retrieve'):
                return queryset.filter(
                    models.Q(status=CourseStatus.PUBLISHED)
                    | models.Q(instructor=user)
                )
            return queryset.filter(instructor=user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return CourseCreateUpdateSerializer
        return CourseDetailSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated(), IsInstructor()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.save(instructor=self.request.user)
        if course.status == CourseStatus.PUBLISHED and not course.published_at:
            course.published_at = timezone.now()
            course.save(update_fields=['published_at'])

    def perform_update(self, serializer):
        course = serializer.save()
        if course.status == CourseStatus.PUBLISHED and not course.published_at:
            course.published_at = timezone.now()
            course.save(update_fields=['published_at'])

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStudent])
    def enroll(self, request, slug=None):
        course = self.get_object()
        if course.status != CourseStatus.PUBLISHED:
            return Response(
                {'detail': 'Cannot enroll in unpublished course.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if course.max_students > 0 and course.enrollment_count >= course.max_students:
            return Response(
                {'detail': 'Course is full.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'status': EnrollmentStatus.ACTIVE, 'is_active': True},
        )
        if not created and not enrollment.is_active:
            enrollment.is_active = True
            enrollment.status = EnrollmentStatus.ACTIVE
            enrollment.save()
        serializer = EnrollmentSerializer(enrollment)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'is_active', 'course']
    search_fields = ['course__title']
    ordering_fields = ['enrolled_at', 'progress_percentage']
    ordering = ['-enrolled_at']

    def get_queryset(self):
        user = self.request.user
        if user.role in ('admin',) or user.is_superuser:
            return Enrollment.objects.select_related('student', 'course').all()
        if user.role == 'instructor':
            return Enrollment.objects.filter(
                course__instructor=user,
            ).select_related('student', 'course')
        return Enrollment.objects.filter(student=user).select_related('student', 'course')

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'])
    def drop(self, request, pk=None):
        enrollment = self.get_object()
        enrollment.status = EnrollmentStatus.DROPPED
        enrollment.is_active = False
        enrollment.save()
        return Response({'detail': 'Successfully dropped course.'})
