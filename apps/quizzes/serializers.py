from rest_framework import serializers

from .models import (
    Quiz,
    Question,
    Choice,
    Attempt,
    Answer
)


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = [
            "id",
            "text",
            "is_correct",
        ]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = [
            "id",
            "question",
            "selected_choice",
        ]


class QuestionSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "order",
            "points",
            "choices",
        ]


class QuestionCreateSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Question
        fields = [
            "text",
            "order",
            "points",
            "choices",
        ]

    def create(self, validated_data):

        choices_data = validated_data.pop(
            "choices",
            []
        )

        question = Question.objects.create(
            **validated_data
        )

        for choice_data in choices_data:
            Choice.objects.create(
                question=question,
                **choice_data
            )

        return question


class QuizSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Quiz
        fields = [
            "id",
            "course",
            "module",
            "title",
            "description",
            "passing_score",
            "time_limit_minutes",
            "max_attempts",
            "created_by",
            "questions",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]


class QuizCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = [
            "course",
            "module",
            "title",
            "description",
            "passing_score",
            "time_limit_minutes",
            "max_attempts",
        ]


class QuizStudentSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "passing_score",
            "time_limit_minutes",
            "questions",
        ]


class AttemptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attempt
        fields = [
            "id",
            "quiz",
            "student",
            "score",
            "passed",
            "started_at",
            "completed_at",
        ]

        read_only_fields = [
            "id",
            "score",
            "passed",
            "started_at",
            "completed_at",
        ]


class QuizSubmitSerializer(serializers.Serializer):

    attempt_id = serializers.IntegerField(
        required=False
    )

    responses = serializers.ListField(
        child=serializers.DictField()
    )