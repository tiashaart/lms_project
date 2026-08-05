from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Course
from .services import CourseService

from apps.lessons.serializers import ModuleSerializer


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
        )


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "description",
        )


class InstructorBriefSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
        )


class CourseListSerializer(serializers.ModelSerializer):

    instructor = InstructorBriefSerializer(
        read_only=True
    )

    category = CategorySerializer(
        read_only=True
    )

    module_count = serializers.IntegerField(
        source="modules.count",
        read_only=True
    )

    class Meta:
        model = Course

        fields = (
            "id",
            "title",
            "slug",
            "description",
            "short_description",
            "instructor",
            "category",
            "thumbnail",
            "price",
            "is_free",
            "level",
            "duration_hours",
            "max_students",
            "status",
            "module_count",
            "created_at",
            "published_at",
        )


class CourseDetailSerializer(serializers.ModelSerializer):

    instructor = InstructorBriefSerializer(
        read_only=True
    )

    category = CategorySerializer(
        read_only=True
    )

    modules = ModuleSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Course

        fields = (
            "id",
            "title",
            "slug",
            "description",
            "short_description",
            "instructor",
            "category",
            "thumbnail",
            "price",
            "is_free",
            "level",
            "duration_hours",
            "max_students",
            "status",
            "prerequisites",
            "learning_objectives",
            "modules",
            "created_at",
            "updated_at",
            "published_at",
        )


class CourseCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course

        fields = (
            "title",
            "description",
            "short_description",
            "category",
            "thumbnail",
            "price",
            "is_free",
            "level",
            "duration_hours",
            "max_students",
            "status",
            "prerequisites",
            "learning_objectives",
        )


    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["instructor"] = request.user

        validated_data["slug"] = (
            CourseService.generate_unique_slug(
                validated_data["title"]
            )
        )

        return Course.objects.create(
            **validated_data
        )


    def update(self, instance, validated_data):

        if (
            "title" in validated_data
            and validated_data["title"] != instance.title
        ):
            instance.slug = (
                CourseService.generate_unique_slug(
                    validated_data["title"]
                )
            )

        return super().update(
            instance,
            validated_data
        )


class CourseStudentSerializer(serializers.Serializer):

    id = serializers.IntegerField()

    student_id = serializers.IntegerField(
        source="student.id"
    )

    full_name = serializers.CharField(
        source="student.full_name"
    )

    email = serializers.EmailField(
        source="student.email"
    )

    status = serializers.CharField()

    enrolled_at = serializers.DateTimeField()
