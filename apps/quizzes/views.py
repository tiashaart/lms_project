from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.enrollments.models import Enrollment

from core.permissions import (
    IsAdminOrInstructor,
    IsStudent
)

from .models import (
    Question,
    Quiz,
    Attempt,
    Choice
)

from .serializers import (
    AttemptSerializer,
    QuestionCreateSerializer,
    QuestionSerializer,
    QuizCreateSerializer,
    QuizSerializer,
    QuizStudentSerializer,
    QuizSubmitSerializer,
)

from .services import QuizService



class QuizListCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    filterset_fields = ['course']
    search_fields = ['title']


    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Quiz.objects.none()


        user = self.request.user


        queryset = Quiz.objects.prefetch_related(
            "questions__choices"
        )


        if user.role == "instructor":

            return queryset.filter(
                course__instructor=user
            )


        if user.role == "student":

            course_ids = Enrollment.objects.filter(
                student=user,
                status="active"
            ).values_list(
                "course_id",
                flat=True
            )


            return queryset.filter(
                course_id__in=course_ids
            )


        return queryset



    def get_serializer_class(self):

        if self.request.method == "POST":
            return QuizCreateSerializer


        if self.request.user.role == "student":
            return QuizStudentSerializer


        return QuizSerializer



    def get_permissions(self):

        if self.request.method == "POST":

            return [
                IsAuthenticated(),
                IsAdminOrInstructor()
            ]


        return [
            IsAuthenticated()
        ]



    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        quiz = Quiz.objects.create(
            created_by=request.user,
            **serializer.validated_data
        )


        return Response(
            {
                "success": True,
                "data": QuizSerializer(quiz).data,
                "message": "Quiz created"
            },
            status=status.HTTP_201_CREATED
        )





class QuizDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Quiz.objects.prefetch_related(
        "questions__choices"
    )

    serializer_class = QuizCreateSerializer



    def get_permissions(self):

        if self.request.method == "GET":

            return [
                IsAuthenticated()
            ]


        return [
            IsAuthenticated(),
            IsAdminOrInstructor()
        ]



    def retrieve(self, request, *args, **kwargs):

        quiz = self.get_object()


        if request.user.role == "student":

            data = QuizStudentSerializer(
                quiz
            ).data

        else:

            data = QuizSerializer(
                quiz
            ).data


        return Response(
            {
                "success": True,
                "data": data
            }
        )





class QuestionListCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor
    ]



    def get(self, request, quiz_pk):

        quiz = get_object_or_404(
            Quiz,
            id=quiz_pk
        )


        questions = quiz.questions.all()


        return Response(
            {
                "success": True,
                "data": QuestionSerializer(
                    questions,
                    many=True
                ).data
            }
        )



    def post(self, request, quiz_pk):

        quiz = get_object_or_404(
            Quiz,
            id=quiz_pk
        )


        serializer = QuestionCreateSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        choices = serializer.validated_data.pop(
            "choices",
            []
        )


        question = Question.objects.create(
            quiz=quiz,
            **serializer.validated_data
        )


        for choice in choices:

            Choice.objects.create(
                question=question,
                **choice
            )


        return Response(
            {
                "success": True,
                "data": QuestionSerializer(
                    question
                ).data,
                "message": "Question created"
            },
            status=status.HTTP_201_CREATED
        )





class QuestionDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor
    ]



    def patch(self, request, quiz_pk, pk):

        question = get_object_or_404(
            Question,
            id=pk,
            quiz_id=quiz_pk
        )


        serializer = QuestionCreateSerializer(
            question,
            data=request.data,
            partial=True
        )


        serializer.is_valid(
            raise_exception=True
        )


        question.text = serializer.validated_data.get(
            "text",
            question.text
        )

        question.order = serializer.validated_data.get(
            "order",
            question.order
        )

        question.points = serializer.validated_data.get(
            "points",
            question.points
        )


        question.save()


        return Response(
            {
                "success": True,
                "data": QuestionSerializer(question).data,
                "message": "Question updated"
            }
        )



    def delete(self, request, quiz_pk, pk):

        question = get_object_or_404(
            Question,
            id=pk,
            quiz_id=quiz_pk
        )


        question.delete()


        return Response(
            {
                "success": True,
                "message": "Question deleted"
            },
            status=status.HTTP_204_NO_CONTENT
        )





class StartQuizView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]



    def post(self, request, pk):

        quiz = get_object_or_404(
            Quiz,
            id=pk
        )


        attempt = QuizService.start_attempt(
            request.user,
            quiz
        )


        return Response(
            {
                "success": True,
                "data": {
                    "attempt_id": attempt.id,
                    "started_at": attempt.started_at,
                    "quiz": QuizStudentSerializer(
                        quiz
                    ).data
                }
            },
            status=status.HTTP_201_CREATED
        )





class SubmitQuizView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]



    def post(self, request, pk):

        quiz = get_object_or_404(
            Quiz,
            id=pk
        )


        serializer = QuizSubmitSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        attempt = QuizService.submit_quiz(
            request.user,
            quiz,
            serializer.validated_data["responses"]
        )


        return Response(
            {
                "success": True,
                "data": QuizService.get_results(
                    attempt
                )
            }
        )





class QuizResultsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]



    def get(self, request, pk):

        attempt = get_object_or_404(
            Attempt,
            id=pk
        )


        return Response(
            {
                "success": True,
                "data": QuizService.get_results(
                    attempt
                )
            }
        )





class MyQuizAttemptsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]



    def get(self, request):

        attempts = Attempt.objects.filter(
            student=request.user
        ).select_related(
            "quiz"
        )


        return Response(
            {
                "success": True,
                "data": AttemptSerializer(
                    attempts,
                    many=True
                ).data
            }
        )