import logging

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    ChangePasswordSerializer,
    EmailVerificationSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserRegistrationSerializer,
)
from .services import AuthService
from .tokens import EmailTokenObtainPairSerializer

User = get_user_model()
logger = logging.getLogger('hope_academy')


class AuthThrottle(AnonRateThrottle):
    scope = 'auth'


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Register a new user')
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Registration successful.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "role": user.role
                    }
                },
                status=status.HTTP_201_CREATED
            )

        # This will show the real error
        print("REGISTRATION ERROR:", serializer.errors)

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Login and obtain JWT tokens')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        return Response({
            'success': True,
            'data': {
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'full_name': user.full_name,
                    'email_verified': user.email_verified,
                },
            },
        })


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Authentication'], summary='Refresh JWT access token')
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data = {'success': True, 'data': response.data}
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Authentication'], summary='Logout and blacklist refresh token')
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'success': False, 'error': {'message': 'Refresh token is required.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as exc:
            logger.warning('Logout blacklist failed: %s', exc)
            return Response(
                {'success': False, 'error': {'message': 'Invalid or expired refresh token.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'success': True, 'message': 'Logged out successfully.'})


class LogoutAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Authentication'], summary='Logout from all devices')
    def post(self, request):
        _, message = AuthService.logout_all(request.user)
        return Response({'success': True, 'message': message})


class ResendVerificationView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Resend email verification')
    def post(self, request):
        success, message = AuthService.resend_verification(request.user)
        if not success:
            return Response(
                {'success': False, 'error': {'message': message}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'success': True, 'message': message})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Authentication'], summary='Change password')
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message = AuthService.change_password(
            request.user,
            serializer.validated_data['old_password'],
            serializer.validated_data['new_password'],
        )
        if not success:
            return Response(
                {'success': False, 'error': {'message': message}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'success': True, 'message': message})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Request password reset email')
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.request_password_reset(serializer.validated_data['email'])
        return Response({
            'success': True,
            'message': 'If the email exists, a reset link has been sent.',
        })


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Confirm password reset')
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message = AuthService.reset_password(
            serializer.validated_data['token'],
            serializer.validated_data['new_password'],
        )
        if not success:
            return Response(
                {'success': False, 'error': {'message': message}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'success': True, 'message': message})


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Authentication'], summary='Verify email address')
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message = AuthService.verify_email(serializer.validated_data['token'])
        if not success:
            return Response(
                {'success': False, 'error': {'message': message}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'success': True, 'message': message})
