"""Shared course and content access helpers."""

from apps.courses.models import Course
from apps.enrollments.models import Enrollment


def is_enrolled(student, course):
    return Enrollment.objects.filter(
        student=student,
        course=course,
        status=Enrollment.Status.ACTIVE,
    ).exists()


def can_view_course(user, course):
    if user.role == 'admin':
        return True

    if user.role in ['teacher', 'instructor'] and course.instructor_id == user.id:
        return True

    if user.role == 'student':
        if course.status == Course.Status.PUBLISHED:
            return True
        return is_enrolled(user, course)

    return False


def can_manage_course(user, course):
    if user.role == 'admin':
        return True

    return (
        user.role in ['teacher', 'instructor']
        and course.instructor_id == user.id
    )


def can_access_course_content(user, course):
    """Read modules/lessons/materials."""

    if can_manage_course(user, course):
        return True

    if user.role == 'student':
        return is_enrolled(user, course)

    return False