from .models import Notification


class NotificationService:
    @staticmethod
    def create(user, notification_type, title, message, related_object_id=None, related_object_type=''):
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            related_object_id=related_object_id,
            related_object_type=related_object_type,
        )

    @staticmethod
    def notify_enrollment(student, course):
        NotificationService.create(
            user=student,
            notification_type=Notification.NotificationType.ENROLLMENT,
            title='Enrollment Confirmed',
            message=f'You have successfully enrolled in "{course.title}".',
            related_object_id=course.id,
            related_object_type='course',
        )

    @staticmethod
    def notify_assignment(student, assignment):
        NotificationService.create(
            user=student,
            notification_type=Notification.NotificationType.ASSIGNMENT,
            title='New Assignment',
            message=f'New assignment "{assignment.title}" has been posted.',
            related_object_id=assignment.id,
            related_object_type='assignment',
        )

    @staticmethod
    def notify_course_update(students, course, message):
        for student in students:
            NotificationService.create(
                user=student,
                notification_type=Notification.NotificationType.COURSE_UPDATE,
                title=f'Course Update: {course.title}',
                message=message,
                related_object_id=course.id,
                related_object_type='course',
            )

    @staticmethod
    def notify_announcement(students, announcement):
        for student in students:
            NotificationService.create(
                user=student,
                notification_type=Notification.NotificationType.ANNOUNCEMENT,
                title=announcement.title,
                message=announcement.content[:200],
                related_object_id=announcement.id,
                related_object_type='announcement',
            )

    @staticmethod
    def notify_grade(student, assignment, grade):
        NotificationService.create(
            user=student,
            notification_type=Notification.NotificationType.GRADE,
            title='Assignment Graded',
            message=f'Your assignment "{assignment.title}" has been graded. Score: {grade}',
            related_object_id=assignment.id,
            related_object_type='assignment',
        )

    @staticmethod
    def notify_quiz_result(student, quiz, attempt):
        NotificationService.create(
            user=student,
            notification_type=Notification.NotificationType.QUIZ,
            title='Quiz Results',
            message=(
                f'Your quiz "{quiz.title}" score: {attempt.score}%. '
                f'{"Passed" if attempt.passed else "Did not pass"}.'
            ),
            related_object_id=quiz.id,
            related_object_type='quiz',
        )

    @staticmethod
    def notify_new_quiz(students, quiz):
        for student in students:
            NotificationService.create(
                user=student,
                notification_type=Notification.NotificationType.QUIZ,
                title='New Quiz Available',
                message=f'A new quiz "{quiz.title}" is available.',
                related_object_id=quiz.id,
                related_object_type='quiz',
            )

    @staticmethod
    def mark_read(notification):
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    @staticmethod
    def mark_all_read(user):
        Notification.objects.filter(user=user, is_read=False).update(is_read=True)
