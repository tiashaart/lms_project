from django.urls import path

from .views import (
    MyQuizAttemptsView,
    QuestionDetailView,
    QuestionListCreateView,
    QuizDetailView,
    QuizListCreateView,
    QuizResultsView,
    StartQuizView,
    SubmitQuizView,
)

urlpatterns = [
    path('', QuizListCreateView.as_view(), name='quiz-list'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('<int:quiz_pk>/questions/', QuestionListCreateView.as_view(), name='question-list'),
    path('<int:quiz_pk>/questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('<int:pk>/start/', StartQuizView.as_view(), name='quiz-start'),
    path('<int:pk>/submit/', SubmitQuizView.as_view(), name='quiz-submit'),
    path('attempts/<int:pk>/results/', QuizResultsView.as_view(), name='quiz-results'),
    path('my-attempts/', MyQuizAttemptsView.as_view(), name='my-quiz-attempts'),
]
