from django.urls import path

from reports.views import DashboardReportView, CourseReportView, EnrollmentReportView

urlpatterns = [
    path('dashboard/', DashboardReportView.as_view(), name='report-dashboard'),
    path('courses/<int:course_id>/', CourseReportView.as_view(), name='report-course'),
    path('enrollments/', EnrollmentReportView.as_view(), name='report-enrollments'),
]
