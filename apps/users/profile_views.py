from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    ChangePasswordSerializer,
    ProfilePictureSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from .services import AuthService


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(tags=['Profile'], summary='View current user profile')
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({'success': True, 'data': response.data})


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(tags=['Profile'], summary='Update profile')
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        profile = UserProfileSerializer(self.get_object()).data
        return Response({'success': True, 'data': profile, 'message': 'Profile updated.'})


class ProfilePictureUploadView(generics.UpdateAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    @extend_schema(tags=['Profile'], summary='Upload profile picture')
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': {'profile_picture': self.get_object().profile_picture.url},
            'message': 'Profile picture updated.',
        })


class ProfileChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Profile'], summary='Change password from profile')
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
