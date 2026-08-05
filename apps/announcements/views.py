from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdminOrInstructor

from .models import Announcement
from .serializers import AnnouncementCreateSerializer, AnnouncementSerializer
from .services import AnnouncementService


class AnnouncementListCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    filterset_fields = [
        'course',
        'is_published'
    ]

    search_fields = [
        'title',
        'content'
    ]

    ordering_fields = [
        'created_at',
        'published_at'
    ]


    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Announcement.objects.none()


        user = self.request.user


        qs = Announcement.objects.select_related(
            'author',
            'course'
        )


        # Admin and instructors can see their announcements
        if user.role in ('admin', 'instructor'):

            if user.role == 'instructor':
                return (
                    qs.filter(course__instructor=user)
                    |
                    qs.filter(author=user)
                )

            return qs



        # Student announcements
        from apps.enrollments.models import Enrollment


        course_ids = Enrollment.objects.filter(
            student=user,
            is_active=True
        ).values_list(
            'course_id',
            flat=True
        )


        return (
            qs.filter(
                is_published=True,
                course_id__in=course_ids
            )
            |
            qs.filter(
                is_published=True,
                course__isnull=True
            )
        )



    def get_serializer_class(self):

        if self.request.method == 'POST':
            return AnnouncementCreateSerializer

        return AnnouncementSerializer



    def get_permissions(self):

        if self.request.method == 'POST':
            return [
                IsAuthenticated(),
                IsAdminOrInstructor()
            ]

        return [
            IsAuthenticated()
        ]



    def list(self, request, *args, **kwargs):

        response = super().list(
            request,
            *args,
            **kwargs
        )

        return Response(
            {
                'success': True,
                'data': response.data
            }
        )



    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        announcement = Announcement.objects.create(
            author=request.user,
            **serializer.validated_data
        )


        return Response(
            {
                'success': True,
                'data': AnnouncementSerializer(
                    announcement
                ).data,
                'message': 'Announcement created.'
            },
            status=status.HTTP_201_CREATED
        )





class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor
    ]

    queryset = Announcement.objects.all()

    serializer_class = AnnouncementCreateSerializer



    def retrieve(self, request, *args, **kwargs):

        announcement = self.get_object()

        return Response(
            {
                'success': True,
                'data': AnnouncementSerializer(
                    announcement
                ).data
            }
        )



    def update(self, request, *args, **kwargs):

        announcement = self.get_object()


        if (
            request.user.role == 'instructor'
            and announcement.author_id != request.user.id
        ):
            return Response(
                {
                    'success': False,
                    'error': {
                        'message': 'Not authorized.'
                    }
                },
                status=403
            )


        response = super().update(
            request,
            *args,
            **kwargs
        )


        announcement.refresh_from_db()


        return Response(
            {
                'success': True,
                'data': AnnouncementSerializer(
                    announcement
                ).data,
                'message': 'Announcement updated.'
            }
        )



    def destroy(self, request, *args, **kwargs):

        announcement = self.get_object()


        if (
            request.user.role == 'instructor'
            and announcement.author_id != request.user.id
        ):
            return Response(
                {
                    'success': False,
                    'error': {
                        'message': 'Not authorized.'
                    }
                },
                status=403
            )


        super().destroy(
            request,
            *args,
            **kwargs
        )


        return Response(
            {
                'success': True,
                'message': 'Announcement deleted.'
            },
            status=status.HTTP_204_NO_CONTENT
        )





class PublishAnnouncementView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrInstructor
    ]


    @extend_schema(tags=['Announcements'])
    def post(self, request, pk):

        announcement = get_object_or_404(
            Announcement,
            pk=pk
        )


        if (
            request.user.role == 'instructor'
            and announcement.author_id != request.user.id
        ):
            return Response(
                {
                    'success': False,
                    'error': {
                        'message': 'Not authorized.'
                    }
                },
                status=403
            )


        AnnouncementService.publish(
            announcement
        )


        return Response(
            {
                'success': True,
                'data': AnnouncementSerializer(
                    announcement
                ).data,
                'message': 'Announcement published.'
            }
        )
