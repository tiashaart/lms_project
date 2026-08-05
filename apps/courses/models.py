



from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        db_table = "courses_category"
        ordering = ["name"]


    def __str__(self):
        return self.name



class Course(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"


    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"



    title = models.CharField(
        max_length=255
    )


    slug = models.SlugField(
        unique=True
    )


    description = models.TextField()



    short_description = models.CharField(
        max_length=300,
        blank=True,
        default=""
    )



    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses_taught"
    )



    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses"
    )



    thumbnail = models.ImageField(
        upload_to="course_thumbnails/",
        blank=True,
        null=True
    )



    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )



    is_free = models.BooleanField(
        default=False
    )



    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER
    )



    duration_hours = models.PositiveIntegerField(
        default=0
    )



    max_students = models.PositiveIntegerField(
        default=0
    )



    prerequisites = models.TextField(
        blank=True,
        default=""
    )



    learning_objectives = models.TextField(
        blank=True,
        default=""
    )



    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )



    published_at = models.DateTimeField(
        null=True,
        blank=True
    )



    created_at = models.DateTimeField(
        auto_now_add=True
    )



    updated_at = models.DateTimeField(
        auto_now=True
    )



    class Meta:
        db_table = "courses_course"
        ordering = ["-created_at"]



    def __str__(self):
        return self.title



    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)