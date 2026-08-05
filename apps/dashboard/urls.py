from django.urls import path

from .views import AdminDashboardView, InstructorDashboardView, StudentDashboardView, UnifiedDashboardView

urlpatterns = [
    path('', UnifiedDashboardView.as_view(), name='dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('instructor/', InstructorDashboardView.as_view(), name='instructor-dashboard'),
    path('student/', StudentDashboardView.as_view(), name='student-dashboard'),
]
