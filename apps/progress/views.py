from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course
from apps.lessons.models import Lesson

from core.access import can_manage_course
from core.permissions import IsAdminOrInstructor, IsStudent

from .serializers import (
    StudentProgressSerializer,
    MarkCompleteSerializer,
)
from .services import ProgressService


class MarkLessonCompleteView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(
        tags=["Progress"],
        request=MarkCompleteSerializer,
    )
    def post(self, request):

        serializer = MarkCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = get_object_or_404(
            Lesson,
            id=serializer.validated_data["lesson_id"],
        )

        progress = ProgressService.mark_lesson_complete(
            request.user,
            lesson,
        )

        return Response({
            "success": True,
            "data": StudentProgressSerializer(progress).data,
            "message": "Lesson marked as complete.",
        })


class MarkLessonIncompleteView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(
        tags=["Progress"],
        request=MarkCompleteSerializer,
    )
    def post(self, request):

        serializer = MarkCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = get_object_or_404(
            Lesson,
            id=serializer.validated_data["lesson_id"],
        )

        progress = ProgressService.mark_lesson_incomplete(
            request.user,
            lesson,
        )

        return Response({
            "success": True,
            "data": StudentProgressSerializer(progress).data if progress else None,
            "message": "Lesson marked as incomplete.",
        })


class CourseProgressView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(tags=["Progress"])
    def get(self, request, course_id):

        course = get_object_or_404(
            Course,
            id=course_id,
        )

        course_progress = ProgressService.get_course_progress(
            request.user,
            course,
        )

        lessons = ProgressService.get_lesson_progress(
            request.user,
            course,
        )

        return Response({
            "success": True,
            "data": {
                "course_progress": StudentProgressSerializer(
                    course_progress
                ).data if course_progress else None,

                "lessons": StudentProgressSerializer(
                    lessons,
                    many=True,
                ).data,
            },
        })


class InstructorCourseProgressView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor,
    ]

    @extend_schema(tags=["Progress"])
    def get(self, request, course_id):

        course = get_object_or_404(
            Course,
            id=course_id,
        )

        if not can_manage_course(request.user, course):
            return Response(
                {
                    "success": False,
                    "message": "Not authorized.",
                },
                status=403,
            )

        progress_records = ProgressService.get_instructor_course_progress(
            course,
        )

        data = []

        for progress in progress_records:
            data.append({
                "student_id": progress.student.id,
                "student_name": getattr(progress.student, "full_name", ""),
                "student_email": progress.student.email,
                "progress_percentage": progress.progress_percentage,
                "last_accessed": progress.last_accessed,
            })

        return Response({
            "success": True,
            "data": data,
        })


class ProgressReportView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(tags=["Progress"])
    def get(self, request):

        report = ProgressService.get_progress_report(
            request.user,
        )

        return Response({
            "success": True,
            "data": StudentProgressSerializer(
                report,
                many=True,
            ).data,
        })