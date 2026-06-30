from rest_framework import permissions

from users.models import UserRole


class IsStudent(permissions.BasePermission):
    """Allow access only to student users."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.STUDENT
        )


class IsInstructor(permissions.BasePermission):
    """Allow access only to instructor users."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.INSTRUCTOR
        )


class IsAdministrator(permissions.BasePermission):
    """Allow access only to administrator users."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.role == UserRole.ADMIN
                or request.user.is_superuser
            )
        )


class IsInstructorOrAdmin(permissions.BasePermission):
    """Allow access to instructors and administrators."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in (UserRole.INSTRUCTOR, UserRole.ADMIN)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access to object owner or administrators."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRole.ADMIN or request.user.is_superuser:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsInstructorOfCourse(permissions.BasePermission):
    """Allow access to the instructor who owns the course."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRole.ADMIN or request.user.is_superuser:
            return True
        course = getattr(obj, 'course', obj)
        if hasattr(course, 'instructor'):
            return course.instructor == request.user
        return False


class ReadOnly(permissions.BasePermission):
    """Allow read-only access."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
