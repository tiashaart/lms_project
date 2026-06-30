"""
Unit and API tests for HALMS users app.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, UserRole, StudentProfile


class UserModelTests(APITestCase):
    def test_create_student_user(self):
        user = User.objects.create_user(
            email='student@test.com',
            password='TestPass123!',
            first_name='Test',
            last_name='Student',
            role=UserRole.STUDENT,
        )
        self.assertEqual(user.email, 'student@test.com')
        self.assertTrue(user.is_student)
        self.assertTrue(StudentProfile.objects.filter(user=user).exists())

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User',
        )
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, UserRole.ADMIN)


class UserAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            'email': 'newuser@test.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User',
            'role': UserRole.STUDENT,
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])

    def test_user_login(self):
        User.objects.create_user(
            email='login@test.com',
            password='LoginPass123!',
            first_name='Login',
            last_name='Test',
        )
        response = self.client.post(self.login_url, {
            'email': 'login@test.com',
            'password': 'LoginPass123!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_registration_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'email': 'bad@test.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!',
            'first_name': 'Bad',
            'last_name': 'User',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
