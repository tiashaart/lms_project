from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.enrollments.models import Enrollment
from apps.notifications.services import NotificationService

from .models import Assignment, AssignmentSubmission


class AssignmentService:
    @staticmethod
    def create_assignment(course, created_by, **data):
        assignment = Assignment.objects.create(course=course, created_by=created_by, **data)
        students = Enrollment.objects.filter(
            course=course, status=Enrollment.Status.ACTIVE,
        ).select_related('student')
        for enrollment in students:
            NotificationService.notify_assignment(enrollment.student, assignment)
        return assignment

    @staticmethod
    def submit(assignment, student, file=None, text_submission=''):
        if not Enrollment.objects.filter(
            student=student, course=assignment.course, status=Enrollment.Status.ACTIVE,
        ).exists():
            raise ValidationError('You must be enrolled to submit this assignment.')

        if AssignmentSubmission.objects.filter(assignment=assignment, student=student).exists():
            raise ValidationError('You have already submitted this assignment.')

        if not file and not text_submission:
            raise ValidationError('Please provide a file or text submission.')

        status = AssignmentSubmission.Status.LATE if assignment.is_past_due else AssignmentSubmission.Status.SUBMITTED

        return AssignmentSubmission.objects.create(
            assignment=assignment,
            student=student,
            file=file,
            text_submission=text_submission,
            status=status,
        )

    @staticmethod
    def grade_submission(submission, grade, feedback, graded_by):
        if grade > submission.assignment.max_score:
            raise ValidationError(f'Grade cannot exceed max score of {submission.assignment.max_score}.')

        submission.grade = grade
        submission.feedback = feedback
        submission.status = AssignmentSubmission.Status.GRADED
        submission.graded_at = timezone.now()
        submission.graded_by = graded_by
        submission.save()
        NotificationService.notify_grade(submission.student, submission.assignment, grade)
        return submission
