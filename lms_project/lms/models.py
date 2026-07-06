from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# 1. ACCOUNTS - Custom User with roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'), 
        ('teacher', 'Teacher'), 
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

# 2. COURSES - Course, Lesson, Enrollment
class Course(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role':'teacher'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order']

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role':'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('student', 'course')

# 3. QUIZ - Quiz, Question, Option, Result
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    percentage = models.FloatField(default=0)
    taken_at = models.DateTimeField(auto_now_add=True)