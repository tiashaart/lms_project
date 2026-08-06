from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        if getattr(settings, 'REQUIRE_EMAIL_VERIFICATION', False):
            if not self.user.email_verified:
                raise serializers.ValidationError(
                    'Email not verified. Please check your inbox or request a new verification email.'
                )
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        return token
