from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer
from .services import NotificationService


class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            qs = qs.filter(is_read=is_read.lower() == 'true')
        return qs

    @extend_schema(tags=['Notifications'])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated = self.get_paginated_response(serializer.data)
            paginated.data = {
                'success': True,
                'data': {
                    **paginated.data,
                    'unread_count': unread_count,
                },
            }
            return paginated

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'notifications': serializer.data,
                'unread_count': unread_count,
            },
        })


class NotificationDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'success': True, 'data': response.data})

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Notifications'])
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        NotificationService.mark_read(notification)
        return Response({'success': True, 'message': 'Notification marked as read.'})


class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Notifications'])
    def post(self, request):
        NotificationService.mark_all_read(request.user)
        return Response({'success': True, 'message': 'All notifications marked as read.'})
