from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from django.utils import timezone

from apps.assignments.models import Assignment, AssignmentSubmission
from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from apps.notifications.models import Notification
from apps.progress.models import StudentProgress
from apps.quizzes.models import Quiz, Attempt


User = get_user_model()


class DashboardService:

    @staticmethod
    def admin_stats():

        return {
            "total_users": User.objects.count(),

            "total_students":
                User.objects.filter(
                    role="student"
                ).count(),

            "total_instructors":
                User.objects.filter(
                    role="instructor"
                ).count(),

            "total_courses":
                Course.objects.count(),

            "total_enrollments":
                Enrollment.objects.filter(
                    status=Enrollment.Status.ACTIVE
                ).count(),

            "total_assignments":
                Assignment.objects.count(),

            "published_courses":
                Course.objects.filter(
                    status=Course.Status.PUBLISHED
                ).count(),
        }



    @staticmethod
    def instructor_stats(instructor):

        courses = Course.objects.filter(
            instructor=instructor
        )

        course_ids = courses.values_list(
            "id",
            flat=True
        )


        enrollments = Enrollment.objects.filter(
            course_id__in=course_ids,
            status=Enrollment.Status.ACTIVE
        )


        assignments = Assignment.objects.filter(
            course_id__in=course_ids
        )


        submissions = AssignmentSubmission.objects.filter(
            assignment__course_id__in=course_ids
        )


        return {

            "courses_created":
                courses.count(),


            "published_courses":
                courses.filter(
                    status=Course.Status.PUBLISHED
                ).count(),


            "student_count":
                enrollments.values(
                    "student"
                ).distinct().count(),


            "total_enrollments":
                enrollments.count(),


            "assignment_count":
                assignments.count(),


            "submission_count":
                submissions.count(),


            "graded_count":
                submissions.filter(
                    status=AssignmentSubmission.Status.GRADED
                ).count(),


            "quiz_count":
                Quiz.objects.filter(
                    course_id__in=course_ids
                ).count(),


            "average_grade":
                submissions.filter(
                    status=AssignmentSubmission.Status.GRADED
                ).aggregate(
                    avg=Avg("grade")
                )["avg"] or 0,


            "course_performance": [

                {
                    "course_id": course.id,

                    "course_title":
                        course.title,

                    "enrollment_count":
                        course.enrollments.filter(
                            status=Enrollment.Status.ACTIVE
                        ).count(),

                    "assignment_count":
                        course.assignments.count(),
                }

                for course in courses[:10]

            ],
        }





    @staticmethod
    def student_stats(student):

        enrollments = Enrollment.objects.filter(
            student=student,
            status=Enrollment.Status.ACTIVE
        ).select_related(
            "course"
        )


        # Course progress stored as StudentProgress
        # lesson=None means course level progress

        progress = StudentProgress.objects.filter(
            student=student,
            lesson=None
        ).select_related(
            "course"
        )



        upcoming = Assignment.objects.filter(
            course__enrollments__student=student,
            course__enrollments__status=Enrollment.Status.ACTIVE,
            due_date__gte=timezone.now(),
        ).order_by(
            "due_date"
        )[:5]



        notifications = Notification.objects.filter(
            user=student,
            is_read=False
        ).order_by(
            "-created_at"
        )[:5]



        return {


            "enrolled_courses":
                enrollments.count(),



            "courses": [

                {
                    "course_id":
                        enrollment.course.id,

                    "course_title":
                        enrollment.course.title,

                    "enrolled_at":
                        enrollment.enrolled_at,
                }

                for enrollment in enrollments

            ],



            "progress": [

                {
                    "course_id":
                        item.course.id,

                    "course_title":
                        item.course.title,

                    "progress_percentage":
                        item.progress_percentage,
                }

                for item in progress

            ],



            "upcoming_assignments": [

                {
                    "id":
                        assignment.id,

                    "title":
                        assignment.title,

                    "course_title":
                        assignment.course.title,

                    "due_date":
                        assignment.due_date,
                }

                for assignment in upcoming

            ],



            "recent_notifications": [

                {
                    "id":
                        notification.id,

                    "title":
                        notification.title,

                    "message":
                        notification.message,

                    "created_at":
                        notification.created_at,
                }

                for notification in notifications

            ],



            "unread_notifications":
                Notification.objects.filter(
                    user=student,
                    is_read=False
                ).count(),



            "quiz_attempts":
                Attempt.objects.filter(
                    student=student
                ).count(),



            "quizzes_passed":
                Attempt.objects.filter(
                    student=student,
                    passed=True
                ).count(),

        }




    @staticmethod
    def get_stats_for_user(user):

        if user.role == "admin":
            return DashboardService.admin_stats()


        if user.role == "instructor":
            return DashboardService.instructor_stats(
                user
            )


        if user.role == "student":
            return DashboardService.student_stats(
                user
            )


        return {}
