from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    STUDENT = 'student', _('Student')
    INSTRUCTOR = 'instructor', _('Instructor')
    ADMIN = 'admin', _('Administrator')

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email address is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.ADMIN)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with role-based access control."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        db_index=True,
    )
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'users_user'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role', 'is_active']),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    @property
    def is_student(self):
        return self.role == UserRole.STUDENT

    @property
    def is_instructor(self):
        return self.role == UserRole.INSTRUCTOR

    @property
    def is_administrator(self):
        return self.role == UserRole.ADMIN or self.is_superuser


class StudentProfile(models.Model):
    """Extended profile for student users."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': UserRole.STUDENT},
    )
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=100, blank=True)
    academic_level = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'users_student_profile'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f'Student: {self.user.email}'

    def save(self, *args, **kwargs):
        if not self.student_id:
            import uuid
            self.student_id = f'STU-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)


class InstructorProfile(models.Model):
    """Extended profile for instructor users."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_profile',
        limit_choices_to={'role': UserRole.INSTRUCTOR},
    )
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    qualifications = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'users_instructor_profile'
        verbose_name = 'Instructor Profile'
        verbose_name_plural = 'Instructor Profiles'

    def __str__(self):
        return f'Instructor: {self.user.email}'

    def save(self, *args, **kwargs):
        if not self.employee_id:
            import uuid
            self.employee_id = f'INS-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)


class AdministratorProfile(models.Model):
    """Extended profile for administrator users."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='administrator_profile',
        limit_choices_to={'role': UserRole.ADMIN},
    )
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('standard', 'Standard'),
            ('senior', 'Senior'),
            ('super', 'Super Admin'),
        ],
        default='standard',
    )

    class Meta:
        db_table = 'users_administrator_profile'
        verbose_name = 'Administrator Profile'
        verbose_name_plural = 'Administrator Profiles'

    def __str__(self):
        return f'Admin: {self.user.email}'

    def save(self, *args, **kwargs):
        if not self.employee_id:
            import uuid
            self.employee_id = f'ADM-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)
