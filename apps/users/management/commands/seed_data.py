from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.users.models import User
from apps.courses.models import Category, Course, Lesson, Module


class Command(BaseCommand):
    help = 'Seed demo data for Hope Academy LMS'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            email='admin@hopeacademy.com',
            defaults={
                'username': 'admin',
                'first_name': 'System',
                'last_name': 'Admin',
                'role': 'admin',
                'email_verified': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('AdminPass123!')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin: admin@hopeacademy.com / AdminPass123!'))

        instructor, created = User.objects.get_or_create(
            email='instructor@hopeacademy.com',
            defaults={
                'username': 'instructor',
                'first_name': 'Jane',
                'last_name': 'Instructor',
                'role': 'instructor',
                'email_verified': True,
            },
        )
        if created:
            instructor.set_password('InstructorPass123!')
            instructor.save()
            self.stdout.write(self.style.SUCCESS('Created instructor: instructor@hopeacademy.com'))

        student, created = User.objects.get_or_create(
            email='student@hopeacademy.com',
            defaults={
                'username': 'student',
                'first_name': 'John',
                'last_name': 'Student',
                'role': 'student',
                'email_verified': True,
            },
        )
        if created:
            student.set_password('StudentPass123!')
            student.save()
            self.stdout.write(self.style.SUCCESS('Created student: student@hopeacademy.com'))

        category, _ = Category.objects.get_or_create(
            slug='programming',
            defaults={'name': 'Programming', 'description': 'Software development courses'},
        )

        course, created = Course.objects.get_or_create(
            slug='intro-to-python',
            defaults={
                'title': 'Introduction to Python',
                'description': 'Learn Python programming from scratch.',
                'instructor': instructor,
                'category': category,
                'status': Course.Status.PUBLISHED,
                'duration_hours': 20,
            },
        )
        if created:
            module = Module.objects.create(course=course, title='Getting Started', order=0)
            Lesson.objects.create(
                module=module, title='What is Python?', content='Python basics...', order=0,
            )
            Lesson.objects.create(
                module=module, title='Variables and Types', content='Learn variables...', order=1,
            )
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))

        self.stdout.write(self.style.SUCCESS('Seed data complete.'))
