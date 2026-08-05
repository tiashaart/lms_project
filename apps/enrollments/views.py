from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course

from core.access import can_manage_course
from core.permissions import IsAdminOrInstructor, IsStudent

from .models import Enrollment
from .serializers import (
    EnrollRequestSerializer,
    EnrollmentSerializer,
)

from .services import EnrollmentService


User = get_user_model()


class EnrollView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    @extend_schema(
        tags=['Enrollments'],
        request=EnrollRequestSerializer
    )
    def post(self, request):

        serializer = EnrollRequestSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        course = get_object_or_404(
            Course,
            pk=serializer.validated_data["course_id"]
        )

        enrollment = EnrollmentService.enroll(
            request.user,
            course
        )

        return Response(
            {
                "success": True,
                "data": EnrollmentSerializer(enrollment).data,
                "message": "Enrolled successfully."
            },
            status=status.HTTP_201_CREATED
        )



class UnenrollView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    @extend_schema(tags=['Enrollments'])
    def post(self, request, course_id):

        course = get_object_or_404(
            Course,
            pk=course_id
        )

        EnrollmentService.unenroll(
            request.user,
            course
        )

        return Response(
            {
                "success": True,
                "message": "Unenrolled successfully."
            }
        )



class MyEnrollmentsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    @extend_schema(tags=['Enrollments'])
    def get(self, request):

        enrollments = EnrollmentService.get_enrolled_courses(
            request.user
        )

        return Response(
            {
                "success": True,
                "data": EnrollmentSerializer(
                    enrollments,
                    many=True
                ).data
            }
        )



class CourseEnrollmentsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor
    ]

    @extend_schema(tags=['Enrollments'])
    def get(self, request, course_id):

        course = get_object_or_404(
            Course,
            pk=course_id
        )

        if not can_manage_course(request.user, course):

            return Response(
                {
                    "success": False,
                    "error": "Not authorized."
                },
                status=403
            )


        enrollments = EnrollmentService.get_course_enrollments(
            course
        )

        return Response(
            {
                "success": True,
                "data": EnrollmentSerializer(
                    enrollments,
                    many=True
                ).data
            }
        )



class AdminEnrollView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor
    ]

    @extend_schema(tags=['Enrollments'])
    def post(self, request):

        student_id = request.data.get("student_id")
        course_id = request.data.get("course_id")


        student = get_object_or_404(
            User,
            pk=student_id,
            role="student"
        )


        course = get_object_or_404(
            Course,
            pk=course_id
        )


        if (
            request.user.role == "instructor"
            and not can_manage_course(
                request.user,
                course
            )
        ):
            return Response(
                {
                    "success": False,
                    "error": "Not authorized."
                },
                status=403
            )


        enrollment = EnrollmentService.admin_enroll(
            student,
            course
        )


        return Response(
            {
                "success": True,
                "data": EnrollmentSerializer(enrollment).data,
                "message": "Student enrolled."
            },
            status=status.HTTP_201_CREATED
        )



class AdminUnenrollView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor
    ]

    @extend_schema(tags=['Enrollments'])
    def post(self, request, enrollment_id):

        enrollment = get_object_or_404(
            Enrollment,
            pk=enrollment_id
        )


        if not can_manage_course(
            request.user,
            enrollment.course
        ):
            return Response(
                {
                    "success": False,
                    "error": "Not authorized."
                },
                status=403
            )


        EnrollmentService.unenroll(
            enrollment.student,
            enrollment.course
        )


        return Response(
            {
                "success": True,
                "message": "Student unenrolled."
            }
        )