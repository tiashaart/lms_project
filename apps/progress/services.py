from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.lessons.models import Lesson
from apps.enrollments.models import Enrollment

from .models import StudentProgress


class ProgressService:

    @staticmethod
    def _validate_enrollment(student, course):
        if not Enrollment.objects.filter(
            student=student,
            course=course,
            status=Enrollment.Status.ACTIVE,
        ).exists():
            raise ValidationError(
                "You must be enrolled in this course."
            )

    @staticmethod
    @transaction.atomic
    def mark_lesson_complete(student, lesson):

        course = lesson.module.course

        ProgressService._validate_enrollment(
            student,
            course,
        )

        progress, _ = StudentProgress.objects.get_or_create(
            student=student,
            course=course,
            lesson=lesson,
        )

        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()

        ProgressService.update_course_progress(
            student,
            course,
        )

        return progress

    @staticmethod
    @transaction.atomic
    def mark_lesson_incomplete(student, lesson):

        course = lesson.module.course

        ProgressService._validate_enrollment(
            student,
            course,
        )

        progress = StudentProgress.objects.filter(
            student=student,
            course=course,
            lesson=lesson,
        ).first()

        if progress:
            progress.completed = False
            progress.completed_at = None
            progress.save()

        ProgressService.update_course_progress(
            student,
            course,
        )

        return progress

    @staticmethod
    def update_course_progress(student, course):

        total_lessons = Lesson.objects.filter(
            module__course=course,
        ).count()

        completed_lessons = StudentProgress.objects.filter(
            student=student,
            course=course,
            completed=True,
            lesson__isnull=False,
        ).count()

        percentage = Decimal("0.00")

        if total_lessons > 0:
            percentage = (
                Decimal(completed_lessons)
                / Decimal(total_lessons)
            ) * Decimal("100")

        course_progress, _ = StudentProgress.objects.get_or_create(
            student=student,
            course=course,
            lesson=None,
        )

        course_progress.progress_percentage = percentage.quantize(
            Decimal("0.01")
        )

        course_progress.last_accessed = timezone.now()

        course_progress.save()

        if percentage >= 100:
            from apps.enrollments.services import EnrollmentService

            EnrollmentService.complete_enrollment(
                student,
                course,
            )

        return course_progress

    @staticmethod
    def get_course_progress(student, course):

        ProgressService._validate_enrollment(
            student,
            course,
        )

        return StudentProgress.objects.filter(
            student=student,
            course=course,
            lesson=None,
        ).first()

    @staticmethod
    def get_lesson_progress(student, course):

        ProgressService._validate_enrollment(
            student,
            course,
        )

        return StudentProgress.objects.filter(
            student=student,
            course=course,
            lesson__isnull=False,
        ).select_related(
            "lesson",
        )

    @staticmethod
    def get_progress_report(student):

        return StudentProgress.objects.filter(
            student=student,
            lesson=None,
        ).select_related(
            "course",
        )

    @staticmethod
    def get_instructor_course_progress(course):

        return StudentProgress.objects.filter(
            course=course,
            lesson=None,
        ).select_related(
            "student",
        )