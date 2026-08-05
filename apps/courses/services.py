from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from .models import Course

from apps.lessons.models import (
    Lesson,
    Module,
)


class CourseService:

    @staticmethod
    def generate_unique_slug(title):
        base = slugify(title)
        slug = base
        counter = 1

        while Course.objects.filter(slug=slug).exists():
            slug = f'{base}-{counter}'
            counter += 1

        return slug


    @staticmethod
    def publish_course(course):

        course.status = Course.Status.PUBLISHED
        course.published_at = timezone.now()

        course.save(
            update_fields=[
                'status',
                'published_at',
                'updated_at'
            ]
        )

        return course


    @staticmethod
    def archive_course(course):

        course.status = Course.Status.ARCHIVED

        course.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

        return course


    @staticmethod
    @transaction.atomic
    def reorder_lessons(module, lesson_orders):

        for item in lesson_orders:
            Lesson.objects.filter(
                id=item['id'],
                module=module
            ).update(
                order=item['order']
            )


    @staticmethod
    @transaction.atomic
    def reorder_modules(course, module_orders):

        for item in module_orders:
            Module.objects.filter(
                id=item['id'],
                course=course
            ).update(
                order=item['order']
            )


class ModuleService:

    @staticmethod
    def get_next_order(course):

        last = Module.objects.filter(
            course=course
        ).order_by('-order').first()

        if last:
            return last.order + 1

        return 0


class LessonService:

    @staticmethod
    def get_next_order(module):

        last = Lesson.objects.filter(
            module=module
        ).order_by('-order').first()

        if last:
            return last.order + 1

        return 0