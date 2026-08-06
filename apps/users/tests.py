from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.courses.models import Category, Course, LearningMaterial, Lesson, Module
from apps.enrollments.models import Enrollment

User = get_user_model()


class AuthTests(APITestCase):
    def test_register_student(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'student@test.com',
            'username': 'student1',
            'first_name': 'Test',
            'last_name': 'Student',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'role': 'student',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='student@test.com').exists())

    def test_register_instructor_blocked(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'instr@test.com',
            'username': 'instr1',
            'first_name': 'Test',
            'last_name': 'Instructor',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'role': 'instructor',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        User.objects.create_user(
            email='login@test.com', username='loginuser',
            password='TestPass123!', role='student', email_verified=True,
        )
        response = self.client.post('/api/auth/login/', {
            'email': 'login@test.com',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])

    def test_logout_blacklists_token(self):
        user = User.objects.create_user(
            email='logout@test.com', username='logoutuser',
            password='TestPass123!', role='student',
        )
        refresh = RefreshToken.for_user(user)
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/auth/logout/', {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CourseAccessTests(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            email='inst@test.com', username='inst', password='TestPass123!',
            role='instructor', email_verified=True,
        )
        self.student = User.objects.create_user(
            email='stud@test.com', username='stud', password='TestPass123!',
            role='student', email_verified=True,
        )
        self.other_instructor = User.objects.create_user(
            email='other@test.com', username='other', password='TestPass123!',
            role='instructor', email_verified=True,
        )
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.draft_course = Course.objects.create(
            title='Draft Course', slug='draft-course', description='Draft',
            instructor=self.instructor, category=self.category, status=Course.Status.DRAFT,
        )
        self.published_course = Course.objects.create(
            title='Published Course', slug='published-course', description='Pub',
            instructor=self.instructor, category=self.category, status=Course.Status.PUBLISHED,
        )

    def test_student_cannot_view_draft_course(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f'/api/courses/{self.draft_course.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_instructor_cannot_view_other_draft(self):
        other_draft = Course.objects.create(
            title='Other Draft', slug='other-draft', description='Other',
            instructor=self.other_instructor, status=Course.Status.DRAFT,
        )
        self.client.force_authenticate(user=self.instructor)
        response = self.client.get(f'/api/courses/{other_draft.id}/')
        self.assertIn(response.status_code, [403, 404])

    def test_material_download_requires_enrollment(self):
        module = Module.objects.create(course=self.published_course, title='M1', order=0)
        lesson = Lesson.objects.create(module=module, title='L1', order=0)
        from django.core.files.uploadedfile import SimpleUploadedFile
        material = LearningMaterial.objects.create(
            lesson=lesson, title='Test PDF',
            file=SimpleUploadedFile('test.pdf', b'pdf content'),
            file_type='pdf',
        )
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f'/api/courses/materials/{material.id}/download/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        Enrollment.objects.create(student=self.student, course=self.published_course)
        response = self.client.get(f'/api/courses/materials/{material.id}/download/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HealthCheckTests(APITestCase):
    def test_health_check(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['checks']['database'])
