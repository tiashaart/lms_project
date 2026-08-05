from django.db.models import Q
from django.shortcuts import get_object_or_404

from django_filters import rest_framework as filters

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import action

from apps.lessons.models import Module, Lesson

from core.access import (
    can_manage_course,
    can_view_course,
)

from core.permissions import (
    IsAdmin,
    IsAdminOrInstructor
)

from .models import Category, Course

from .serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
    CourseListSerializer,
    CourseDetailSerializer,
    CourseCreateUpdateSerializer,
)


# -------------------------
# Course Filtering
# -------------------------

class CourseFilter(filters.FilterSet):

    category = filters.NumberFilter(
        field_name="category_id"
    )

    instructor = filters.NumberFilter(
        field_name="instructor_id"
    )

    status = filters.ChoiceFilter(
        choices=Course.Status.choices
    )


    class Meta:
        model = Course
        fields = [
            "category",
            "instructor",
            "status"
        ]



# -------------------------
# Category API
# -------------------------

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()

    def get_serializer_class(self):

        if self.action in [
            "create",
            "update",
            "partial_update"
        ]:
            return CategoryCreateSerializer

        return CategorySerializer



    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy"
        ]:
            return [
                IsAuthenticated(),
                IsAdmin()
            ]

        return [
            IsAuthenticated()
        ]



# -------------------------
# Course API
# -------------------------

class CourseViewSet(viewsets.ModelViewSet):

    filterset_class = CourseFilter


    def get_queryset(self):

        queryset = Course.objects.select_related(
            "category",
            "instructor"
        ).prefetch_related(
            "modules"
        )


        user = self.request.user


        if user.role == "admin":
            return queryset


        if user.role == "student":

            return queryset.filter(
                status=Course.Status.PUBLISHED
            )


        if user.role == "instructor":

            return queryset.filter(
                Q(instructor=user) |
                Q(status=Course.Status.PUBLISHED)
            )


        return queryset.none()



    def get_serializer_class(self):

        if self.action == "retrieve":
            return CourseDetailSerializer


        if self.action in [
            "create",
            "update",
            "partial_update"
        ]:
            return CourseCreateUpdateSerializer


        return CourseListSerializer



    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "publish"
        ]:
            return [
                IsAuthenticated(),
                IsAdminOrInstructor()
            ]

        return [
            IsAuthenticated()
        ]



    def perform_create(self, serializer):

        serializer.save(
            instructor=self.request.user
        )



    def retrieve(self, request, *args, **kwargs):

        course = self.get_object()

        if not can_view_course(
            request.user,
            course
        ):
            return Response(
                {
                    "error":
                    "You cannot access this course"
                },
                status=403
            )


        serializer = self.get_serializer(course)

        return Response(
            {
                "success":True,
                "data":serializer.data
            }
        )



    @action(
        detail=True,
        methods=["post"]
    )
    def publish(self, request, pk=None):

        course = self.get_object()


        if not can_manage_course(
            request.user,
            course
        ):
            return Response(
                {
                    "error":
                    "Permission denied"
                },
                status=403
            )


        course.status = Course.Status.PUBLISHED
        course.save()



        return Response(
            {
                "success":True,
                "message":
                "Course published"
            }
        )