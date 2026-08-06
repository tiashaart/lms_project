from django.conf import settings
from django.db import models

from apps.courses.models import Course
from apps.lessons.models import Module


class Quiz(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )

    module = models.ForeignKey(
        Module,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quizzes"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    passing_score = models.PositiveIntegerField(default=70)

    time_limit_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    max_attempts = models.PositiveIntegerField(default=3)

    is_published = models.BooleanField(default=False)

    shuffle_questions = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quizzes_created"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "quizzes_quiz"


    def __str__(self):
        return self.title



class Question(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    text = models.TextField()

    order = models.PositiveIntegerField(default=0)

    points = models.PositiveIntegerField(default=1)


    class Meta:
        db_table = "quizzes_question"
        ordering = ["order"]


    def __str__(self):
        return self.text



class Choice(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    text = models.CharField(max_length=500)

    is_correct = models.BooleanField(default=False)


    class Meta:
        db_table = "quizzes_choice"


    def __str__(self):
        return self.text



class Attempt(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts"
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    passed = models.BooleanField(default=False)

    started_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )


    class Meta:
        db_table = "quizzes_attempt"


    def __str__(self):
        return f"{self.student} - {self.quiz}"



class Answer(models.Model):

    attempt = models.ForeignKey(
        Attempt,
        on_delete=models.CASCADE,
        related_name="answers",
        null=True,
        blank=True
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="answers"
    )


    class Meta:
        db_table = "quizzes_answer"


    def __str__(self):
        return f"{self.attempt} - {self.question}"