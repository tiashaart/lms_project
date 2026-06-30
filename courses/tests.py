"""
Unit and API tests for HALMS courses app.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, UserRole
from courses.models import Category, Course, Enrollment, CourseStatus


class CourseModelTests(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            email='instructor@test.com',
            password='TestPass123!',
            first_name='Inst',
            last_name='Ructor',
            role=UserRole.INSTRUCTOR,
        )
        self.category = Category.objects.create(name='Programming')

    def test_create_course(self):
        course = Course.objects.create(
            title='Python Basics',
            description='Learn Python',
            category=self.category,
            instructor=self.instructor,
            status=CourseStatus.PUBLISHED,
        )
        self.assertTrue(course.slug)
        self.assertEqual(course.instructor, self.instructor)

    def test_enrollment_unique(self):
        student = User.objects.create_user(
            email='student@test.com',
            password='TestPass123!',
            first_name='Stu',
            last_name='Dent',
            role=UserRole.STUDENT,
        )
        course = Course.objects.create(
            title='Django Course',
            description='Learn Django',
            instructor=self.instructor,
            status=CourseStatus.PUBLISHED,
        )
        Enrollment.objects.create(student=student, course=course)
        with self.assertRaises(Exception):
            Enrollment.objects.create(student=student, course=course)


class CourseAPITests(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            email='instructor2@test.com',
            password='TestPass123!',
            first_name='Inst',
            last_name='Ructor',
            role=UserRole.INSTRUCTOR,
        )
        self.client.force_authenticate(user=self.instructor)
        self.category = Category.objects.create(name='Web Development')

    def test_create_course(self):
        url = reverse('course-list')
        data = {
            'title': 'REST API Development',
            'description': 'Build REST APIs with Django',
            'category': self.category.id,
            'price': 49.99,
            'level': 'intermediate',
            'status': 'draft',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

    def test_list_published_courses_anonymous(self):
        Course.objects.create(
            title='Public Course',
            description='Available to all',
            instructor=self.instructor,
            status=CourseStatus.PUBLISHED,
        )
        self.client.force_authenticate(user=None)
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
