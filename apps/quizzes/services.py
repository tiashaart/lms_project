from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.enrollments.models import Enrollment
from apps.notifications.services import NotificationService

from .models import (
    Quiz,
    Question,
    Choice,
    Attempt,
    Answer,
)


class QuizService:

    @staticmethod
    @transaction.atomic
    def create_quiz_with_questions(
        course,
        created_by,
        quiz_data,
        questions_data
    ):

        quiz = Quiz.objects.create(
            course=course,
            created_by=created_by,
            **quiz_data
        )

        for question_data in questions_data:

            choices_data = question_data.pop(
                "choices",
                []
            )

            question = Question.objects.create(
                quiz=quiz,
                **question_data
            )

            for choice_data in choices_data:

                Choice.objects.create(
                    question=question,
                    **choice_data
                )

        return quiz


    @staticmethod
    def _validate_enrollment(student, quiz):

        if not Enrollment.objects.filter(
            student=student,
            course=quiz.course,
            status=Enrollment.Status.ACTIVE
        ).exists():

            raise ValidationError(
                "You must be enrolled to take this quiz."
            )


    @staticmethod
    def start_attempt(student, quiz):

        QuizService._validate_enrollment(
            student,
            quiz
        )

        attempts = Attempt.objects.filter(
            quiz=quiz,
            student=student
        )

        completed_attempts = attempts.filter(
            completed_at__isnull=False
        ).count()


        if completed_attempts >= quiz.max_attempts:

            raise ValidationError(
                f"Maximum attempts ({quiz.max_attempts}) reached."
            )


        current_attempt = attempts.filter(
            completed_at__isnull=True
        ).first()


        if current_attempt:
            return current_attempt


        return Attempt.objects.create(
            quiz=quiz,
            student=student
        )


    @staticmethod
    def _check_time_limit(attempt):

        quiz = attempt.quiz


        if not quiz.time_limit_minutes:
            return


        elapsed_minutes = (
            timezone.now() -
            attempt.started_at
        ).total_seconds() / 60


        if elapsed_minutes > quiz.time_limit_minutes:

            raise ValidationError(
                "Time limit exceeded for this quiz attempt."
            )


    @staticmethod
    @transaction.atomic
    def submit_quiz(
        student,
        quiz,
        responses_data,
        attempt_id=None
    ):

        if attempt_id:

            attempt = Attempt.objects.filter(
                id=attempt_id,
                quiz=quiz,
                student=student,
                completed_at__isnull=True
            ).first()


            if not attempt:

                raise ValidationError(
                    "Invalid or completed attempt."
                )

        else:

            attempt = QuizService.start_attempt(
                student,
                quiz
            )


        QuizService._check_time_limit(
            attempt
        )


        if attempt.answers.exists():

            raise ValidationError(
                "This attempt already submitted."
            )


        total_points = 0
        earned_points = 0


        for response in responses_data:

            question = Question.objects.get(
                id=response["question_id"],
                quiz=quiz
            )


            total_points += question.points


            selected_choice = None


            if "choice_id" in response:

                selected_choice = Choice.objects.filter(
                    id=response["choice_id"],
                    question=question
                ).first()


                if (
                    selected_choice and
                    selected_choice.is_correct
                ):

                    earned_points += question.points



            Answer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice=selected_choice
            )


        if total_points:

            score = (
                Decimal(earned_points)
                /
                Decimal(total_points)
                *
                100
            )

        else:

            score = Decimal(0)



        attempt.score = score.quantize(
            Decimal("0.01")
        )


        attempt.passed = (
            attempt.score >= quiz.passing_score
        )


        attempt.completed_at = timezone.now()


        attempt.save()


        NotificationService.notify_quiz_result(
            student,
            quiz,
            attempt
        )


        return attempt



    @staticmethod
    def get_results(attempt):

        return {

            "attempt_id": attempt.id,

            "score": attempt.score,

            "passed": attempt.passed,

            "passing_score": attempt.quiz.passing_score,


            "answers": [

                {
                    "question":
                        answer.question.text,

                    "selected_choice":
                        answer.selected_choice.text
                        if answer.selected_choice
                        else None

                }

                for answer in attempt.answers.select_related(
                    "question",
                    "selected_choice"
                )

            ]

        }
