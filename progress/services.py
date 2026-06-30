from decimal import Decimal

from django.db.models import Avg
from django.utils import timezone

from progress.models import StudentProgress
from courses.models import Enrollment, EnrollmentStatus


class ProgressService:
    """Service for calculating and updating student progress."""

    @staticmethod
    def get_or_create_progress(student, course):
        progress, _ = StudentProgress.objects.get_or_create(
            student=student,
            course=course,
        )
        return progress

    @classmethod
    def mark_lesson_complete(cls, student, lesson):
        course = lesson.module.course
        progress = cls.get_or_create_progress(student, course)
        progress.completed_lessons.add(lesson)
        cls.recalculate_completion(progress)
        return progress

    @classmethod
    def recalculate_completion(cls, progress):
        from lessons.models import Lesson

        total_lessons = Lesson.objects.filter(
            module__course=progress.course,
            is_published=True,
        ).count()

        completed_count = progress.completed_lessons.filter(
            is_published=True,
        ).count()

        if total_lessons > 0:
            percentage = Decimal(completed_count / total_lessons * 100).quantize(
                Decimal('0.01')
            )
        else:
            percentage = Decimal('0.00')

        progress.completion_percentage = percentage

        if percentage >= Decimal('100.00') and not progress.completed_at:
            progress.completed_at = timezone.now()
            enrollment = Enrollment.objects.filter(
                student=progress.student,
                course=progress.course,
            ).first()
            if enrollment:
                enrollment.status = EnrollmentStatus.COMPLETED
                enrollment.completed_at = timezone.now()
                enrollment.progress_percentage = percentage
                enrollment.save()

            from certificates.services import CertificateService
            CertificateService.generate_certificate(progress.student, progress.course)

        progress.save()

        enrollment = Enrollment.objects.filter(
            student=progress.student,
            course=progress.course,
        ).first()
        if enrollment:
            enrollment.progress_percentage = progress.completion_percentage
            enrollment.save(update_fields=['progress_percentage'])

        return progress

    @classmethod
    def update_quiz_average(cls, student, course):
        from quizzes.models import QuizAttempt, AttemptStatus

        progress = cls.get_or_create_progress(student, course)
        avg = QuizAttempt.objects.filter(
            student=student,
            quiz__course=course,
            status=AttemptStatus.GRADED,
        ).aggregate(avg=Avg('score'))['avg']

        progress.quiz_average = Decimal(avg or 0).quantize(Decimal('0.01'))
        progress.save(update_fields=['quiz_average'])
        return progress

    @classmethod
    def update_assignment_average(cls, student, course):
        from assignments.models import AssignmentSubmission, SubmissionStatus

        progress = cls.get_or_create_progress(student, course)
        avg = AssignmentSubmission.objects.filter(
            student=student,
            assignment__course=course,
            status=SubmissionStatus.GRADED,
        ).aggregate(avg=Avg('score'))['avg']

        progress.assignment_average = Decimal(avg or 0).quantize(Decimal('0.01'))
        progress.save(update_fields=['assignment_average'])
        return progress

    @classmethod
    def get_dashboard_stats(cls, student):
        progress_records = StudentProgress.objects.filter(student=student)
        enrollments = Enrollment.objects.filter(student=student, is_active=True)

        return {
            'total_enrolled_courses': enrollments.count(),
            'courses_in_progress': progress_records.filter(
                completion_percentage__lt=100,
            ).count(),
            'courses_completed': progress_records.filter(
                completion_percentage=100,
            ).count(),
            'average_completion': progress_records.aggregate(
                avg=Avg('completion_percentage')
            )['avg'] or 0,
            'average_quiz_score': progress_records.aggregate(
                avg=Avg('quiz_average')
            )['avg'] or 0,
            'average_assignment_score': progress_records.aggregate(
                avg=Avg('assignment_average')
            )['avg'] or 0,
        }
