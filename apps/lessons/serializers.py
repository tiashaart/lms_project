from rest_framework import serializers

from .models import (
    Module,
    Lesson,
)


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson

        fields = (
            "id",
            "title",
            "description",
            "content_type",
            "text_content",
            "duration_minutes",
            "order",
            "is_published",
            "is_free_preview",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )



class LessonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson

        fields = (
            "title",
            "description",
            "content_type",
            "text_content",
            "duration_minutes",
            "order",
            "is_published",
            "is_free_preview",
        )



class ModuleSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(
        many=True,
        read_only=True
    )


    class Meta:
        model = Module

        fields = (
            "id",
            "title",
            "description",
            "order",
            "is_published",
            "lessons",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )



class ModuleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module

        fields = (
            "title",
            "description",
            "order",
            "is_published",
        )



class LessonReorderSerializer(serializers.Serializer):

    lessons = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )


    def validate_lessons(self, value):

        for item in value:
            if "id" not in item or "order" not in item:
                raise serializers.ValidationError(
                    "Each item must have id and order"
                )

        return value



class ModuleReorderSerializer(serializers.Serializer):

    modules = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )


    def validate_modules(self, value):

        for item in value:
            if "id" not in item or "order" not in item:
                raise serializers.ValidationError(
                    "Each item must have id and order"
                )

        return value