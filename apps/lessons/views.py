from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from apps.courses.models import Course

from core.access import (
    can_manage_course,
)

from .models import (
    Module,
    Lesson,
)

from .serializers import (
    ModuleSerializer,
    ModuleCreateSerializer,
    LessonSerializer,
    LessonCreateSerializer,
    ModuleReorderSerializer,
    LessonReorderSerializer,
)


class ModuleViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request, course_pk=None):

        course = get_object_or_404(
            Course,
            id=course_pk
        )

        modules = Module.objects.filter(
            course=course
        ).prefetch_related(
            "lessons"
        )

        return Response({
            "success": True,
            "data": ModuleSerializer(
                modules,
                many=True
            ).data
        })

    def create(self, request, course_pk=None):
        course = get_object_or_404(
            Course,
            id=course_pk
        )

        if not can_manage_course(
                request.user,
                course
        ):
            return Response(
                {
                    "error": "Permission denied"
                },
                status=403
            )
        serializer = ModuleCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        module = serializer.save(
            course=course
        )

        return Response(
            ModuleSerializer(module).data,
            status=status.HTTP_201_CREATED
        )


class LessonViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    def list(
        self,
        request,
        course_pk=None,
        module_pk=None
    ):

        module = get_object_or_404(
            Module,
            id=module_pk,
            course_id=course_pk
        )

        lessons = Lesson.objects.filter(
            module=module
        )

        return Response({
            "success": True,
            "data": LessonSerializer(
                lessons,
                many=True
            ).data
        })

    def create(
        self,
        request,
        course_pk=None,
        module_pk=None
    ):

        module = get_object_or_404(
            Module,
            id=module_pk,
            course_id=course_pk
        )

        if not can_manage_course(
            request.user,
            module.course
        ):
            return Response(
                {
                    "error": "Permission denied"
                },
                status=403
            )

        serializer = LessonCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        lesson = serializer.save(
            module=module
        )

        return Response(
            LessonSerializer(lesson).data,
            status=status.HTTP_201_CREATED
        )


class ModuleReorderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, course_pk):

        serializer = ModuleReorderSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        for item in serializer.validated_data["modules"]:

            Module.objects.filter(
                id=item["id"],
                course_id=course_pk
            ).update(
                order=item["order"]
            )

        return Response(
            {
                "message": "Modules reordered"
            }
        )


class LessonReorderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(
        self,
        request,
        course_pk,
        module_pk
    ):

        serializer = LessonReorderSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        for item in serializer.validated_data["lessons"]:

            Lesson.objects.filter(
                id=item["id"],
                module_id=module_pk
            ).update(
                order=item["order"]
            )

        return Response(
            {
                "message": "Lessons reordered"
            }
        )