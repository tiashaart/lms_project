from django.urls import path

from .views import (
    AdminEnrollView,
    AdminUnenrollView,
    CourseEnrollmentsView,
    EnrollView,
    MyEnrollmentsView,
    UnenrollView,
)


urlpatterns = [

    path(
        'enroll/',
        EnrollView.as_view(),
        name='enroll'
    ),

    path(
        'unenroll/<int:course_id>/',
        UnenrollView.as_view(),
        name='unenroll'
    ),

    path(
        'my-courses/',
        MyEnrollmentsView.as_view(),
        name='my-enrollments'
    ),

    path(
        'course/<int:course_id>/',
        CourseEnrollmentsView.as_view(),
        name='course-enrollments'
    ),

    path(
        'admin/enroll/',
        AdminEnrollView.as_view(),
        name='admin-enroll'
    ),

    path(
        'admin/<int:enrollment_id>/unenroll/',
        AdminUnenrollView.as_view(),
        name='admin-unenroll'
    ),

]
