from rest_framework import serializers

from courses.models import Category, Course, Enrollment, CourseStatus
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon',
            'is_active', 'course_count', 'created_at',
        ]
        read_only_fields = ['slug', 'created_at']

    def get_course_count(self, obj):
        return obj.courses.filter(status=CourseStatus.PUBLISHED).count()


class CourseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.full_name', read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'category',
            'category_name', 'instructor', 'instructor_name', 'thumbnail',
            'price', 'is_free', 'level', 'status', 'duration_hours',
            'enrollment_count', 'published_at', 'created_at',
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True,
    )
    instructor = UserSerializer(read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'category', 'category_id', 'instructor', 'thumbnail',
            'price', 'is_free', 'level', 'status', 'duration_hours',
            'max_students', 'prerequisites', 'learning_objectives',
            'enrollment_count', 'published_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['slug', 'instructor', 'published_at', 'created_at', 'updated_at']


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'short_description', 'category',
            'thumbnail', 'price', 'is_free', 'level', 'status',
            'duration_hours', 'max_students', 'prerequisites',
            'learning_objectives',
        ]

    def validate(self, attrs):
        price = attrs.get('price', 0)
        is_free = attrs.get('is_free', False)
        if is_free:
            attrs['price'] = 0
        elif price <= 0:
            raise serializers.ValidationError(
                {'price': 'Paid courses must have a price greater than zero.'}
            )
        return attrs


class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.filter(status=CourseStatus.PUBLISHED),
        source='course',
        write_only=True,
    )

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'course_id', 'status',
            'enrolled_at', 'completed_at', 'progress_percentage', 'is_active',
        ]
        read_only_fields = [
            'student', 'enrolled_at', 'completed_at', 'progress_percentage',
        ]
