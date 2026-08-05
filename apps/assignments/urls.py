from django.urls import path

from .views import (
    AssignmentDetailView,
    AssignmentListCreateView,
    AssignmentSubmissionsView,
    GradeSubmissionView,
    MyAssignmentSubmissionView,
    MySubmissionsView,
    SubmissionDownloadView,
    SubmitAssignmentView,
)

urlpatterns = [
    path('', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('<int:pk>/submit/', SubmitAssignmentView.as_view(), name='assignment-submit'),
    path('<int:pk>/my-submission/', MyAssignmentSubmissionView.as_view(), name='my-assignment-submission'),
    path('<int:pk>/submissions/', AssignmentSubmissionsView.as_view(), name='assignment-submissions'),
    path('submissions/<int:pk>/grade/', GradeSubmissionView.as_view(), name='submission-grade'),
    path('submissions/<int:pk>/download/', SubmissionDownloadView.as_view(), name='submission-download'),
    path('my-submissions/', MySubmissionsView.as_view(), name='my-submissions'),
]
