from django.db.models import Avg, Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from courses.models import Course, Enrollment, CourseStatus
from users.models import User, UserRole
from payments.models import Payment, PaymentStatus
from progress.models import StudentProgress
from quizzes.models import QuizAttempt, AttemptStatus
from users.permissions import IsInstructorOrAdmin, IsAdministrator


class DashboardReportView(APIView):
    """Admin dashboard statistics."""

    permission_classes = [IsAuthenticated, IsAdministrator]

    def get(self, request):
        return Response({
            'users': {
                'total': User.objects.count(),
                'students': User.objects.filter(role=UserRole.STUDENT).count(),
                'instructors': User.objects.filter(role=UserRole.INSTRUCTOR).count(),
                'admins': User.objects.filter(role=UserRole.ADMIN).count(),
            },
            'courses': {
                'total': Course.objects.count(),
                'published': Course.objects.filter(status=CourseStatus.PUBLISHED).count(),
                'draft': Course.objects.filter(status=CourseStatus.DRAFT).count(),
            },
            'enrollments': {
                'total': Enrollment.objects.count(),
                'active': Enrollment.objects.filter(is_active=True).count(),
            },
            'revenue': {
                'total': str(
                    Payment.objects.filter(
                        status=PaymentStatus.COMPLETED,
                    ).aggregate(total=Sum('amount'))['total'] or 0
                ),
                'pending': Payment.objects.filter(status=PaymentStatus.PENDING).count(),
            },
        })


class CourseReportView(APIView):
    """Per-course analytics for instructors and admins."""

    permission_classes = [IsAuthenticated, IsInstructorOrAdmin]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=404)

        user = request.user
        if user.role == UserRole.INSTRUCTOR and course.instructor != user:
            return Response({'detail': 'Not authorized.'}, status=403)

        enrollments = Enrollment.objects.filter(course=course)
        progress = StudentProgress.objects.filter(course=course)

        return Response({
            'course': {
                'id': course.id,
                'title': course.title,
                'status': course.status,
            },
            'enrollments': {
                'total': enrollments.count(),
                'active': enrollments.filter(is_active=True).count(),
                'completed': enrollments.filter(status='completed').count(),
            },
            'progress': {
                'average_completion': progress.aggregate(
                    avg=Avg('completion_percentage')
                )['avg'] or 0,
                'average_quiz_score': progress.aggregate(
                    avg=Avg('quiz_average')
                )['avg'] or 0,
                'average_assignment_score': progress.aggregate(
                    avg=Avg('assignment_average')
                )['avg'] or 0,
            },
            'quiz_attempts': QuizAttempt.objects.filter(
                quiz__course=course, status=AttemptStatus.GRADED,
            ).aggregate(
                total=Count('id'),
                average_score=Avg('score'),
                pass_rate=Avg('passed'),
            ),
        })


class EnrollmentReportView(APIView):
    """Enrollment trends report."""

    permission_classes = [IsAuthenticated, IsAdministrator]

    def get(self, request):
        from django.db.models.functions import TruncMonth

        monthly = (
            Enrollment.objects
            .annotate(month=TruncMonth('enrolled_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        return Response({
            'monthly_enrollments': list(monthly),
            'by_course': list(
                Enrollment.objects.values('course__title')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            ),
        })
