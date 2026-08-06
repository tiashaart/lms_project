from django.urls import path

from .views import (
    CourseProgressView,
    InstructorCourseProgressView,
    MarkLessonCompleteView,
    MarkLessonIncompleteView,
    ProgressReportView,
)

urlpatterns = [
    path('mark-complete/', MarkLessonCompleteView.as_view(), name='mark-complete'),
    path('mark-incomplete/', MarkLessonIncompleteView.as_view(), name='mark-incomplete'),
    path('course/<int:course_id>/', CourseProgressView.as_view(), name='course-progress'),
    path('course/<int:course_id>/students/', InstructorCourseProgressView.as_view(), name='instructor-progress'),
    path('report/', ProgressReportView.as_view(), name='progress-report'),
]
