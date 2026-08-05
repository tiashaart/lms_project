from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdmin, IsInstructor, IsStudent

from .services import DashboardService


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Dashboard'], summary='Admin dashboard statistics')
    def get(self, request):
        return Response({'success': True, 'data': DashboardService.admin_stats()})


class InstructorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    @extend_schema(tags=['Dashboard'], summary='Instructor dashboard statistics')
    def get(self, request):
        return Response({'success': True, 'data': DashboardService.instructor_stats(request.user)})


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    @extend_schema(tags=['Dashboard'], summary='Student dashboard statistics')
    def get(self, request):
        return Response({'success': True, 'data': DashboardService.student_stats(request.user)})


class UnifiedDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Dashboard'], summary='Role-based dashboard (auto-routes by role)')
    def get(self, request):
        return Response({'success': True, 'data': DashboardService.get_stats_for_user(request.user)})
