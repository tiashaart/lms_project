from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.notifications.services import NotificationService

from .models import Enrollment


class EnrollmentService:


    @staticmethod
    @transaction.atomic
    def enroll(student, course):

        existing = Enrollment.objects.filter(
            student=student,
            course=course
        ).first()


        if existing and existing.is_active:
            raise ValidationError(
                "You are already enrolled in this course."
            )


        if course.status != course.Status.PUBLISHED:
            raise ValidationError(
                "This course is not available for enrollment."
            )


        if existing:
            # Re-activate previous enrollment
            existing.is_active = True
            existing.save(
                update_fields=[
                    "is_active"
                ]
            )

            enrollment = existing

        else:
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
                is_active=True
            )


        NotificationService.notify_enrollment(
            student,
            course
        )


        return enrollment



    @staticmethod
    @transaction.atomic
    def unenroll(student, course):

        enrollment = Enrollment.objects.filter(
            student=student,
            course=course,
            is_active=True
        ).first()


        if not enrollment:
            raise ValidationError(
                "You are not enrolled in this course."
            )


        enrollment.is_active = False

        enrollment.save(
            update_fields=[
                "is_active"
            ]
        )


        return enrollment



    @staticmethod
    def admin_enroll(student, course):

        if course.status == course.Status.ARCHIVED:
            raise ValidationError(
                "Cannot enroll in an archived course."
            )


        return EnrollmentService.enroll(
            student,
            course
        )



    @staticmethod
    def get_enrolled_courses(student):

        return Enrollment.objects.filter(
            student=student,
            is_active=True
        ).select_related(
            "course",
            "course__instructor",
            "course__category"
        )



    @staticmethod
    def get_course_enrollments(course):

        return Enrollment.objects.filter(
            course=course,
            is_active=True
        ).select_related(
            "student"
        )