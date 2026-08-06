from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdmin

from .serializers import AdminUserCreateSerializer, AdminUserSerializer, AdminUserUpdateSerializer

User = get_user_model()


class AdminUserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all().order_by('-created_at')
    filterset_fields = ['role', 'is_active', 'email_verified']
    search_fields = ['email', 'username', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminUserCreateSerializer
        return AdminUserSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'success': True, 'data': response.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'success': True, 'data': AdminUserSerializer(user).data, 'message': 'User created.'},
            status=status.HTTP_201_CREATED,
        )


class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()
    serializer_class = AdminUserUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        return Response({'success': True, 'data': AdminUserSerializer(user).data})

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user = self.get_object()
        return Response({
            'success': True,
            'data': AdminUserSerializer(user).data,
            'message': 'User updated.',
        })

    @extend_schema(tags=['Admin'], summary='Deactivate user')
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {'success': False, 'error': {'message': 'Cannot deactivate your own account.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({'success': True, 'message': 'User deactivated.'})
