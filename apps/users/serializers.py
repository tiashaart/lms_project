from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.validators import validate_profile_picture

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'password', 'password_confirm', 'role',
        )
        read_only_fields = ('id',)
        extra_kwargs = {'role': {'default': 'student'}}

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        role = attrs.get('role', 'student')
        if role not in ('student',):
            raise serializers.ValidationError({'role': 'Only student self-registration is allowed.'})
        attrs['role'] = 'student'
        return attrs

    def create(self, validated_data):
        from .services import AuthService
        return AuthService.create_user(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'role', 'bio', 'phone', 'profile_picture', 'email_verified',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'email', 'role', 'email_verified', 'created_at', 'updated_at')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'bio', 'phone')


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_picture',)

    def validate_profile_picture(self, value):
        validate_profile_picture(value)
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Passwords do not match.'})
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Passwords do not match.'})
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()


class AdminUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'role', 'is_active', 'email_verified', 'created_at',
        )
        read_only_fields = ('id', 'email_verified', 'created_at')


class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'password', 'is_active')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        if user.role != 'student':
            user.email_verified = True
        user.save()
        return user


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'role', 'is_active')
