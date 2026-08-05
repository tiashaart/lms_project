from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course
from core.permissions import IsAdminOrInstructor, IsStudent

from .models import Assignment, AssignmentSubmission
from .serializers import (
    AssignmentCreateSerializer,
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    GradeSubmissionSerializer,
    SubmitAssignmentSerializer,
)
from .services import AssignmentService


class AssignmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filterset_fields = ['course']
    search_fields = ['title']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Assignment.objects.none()
        user = self.request.user
        qs = Assignment.objects.select_related('course')
        if user.role == 'instructor':
            return qs.filter(course__instructor=user)
        if user.role == 'student':
            from apps.enrollments.models import Enrollment
            course_ids = Enrollment.objects.filter(
                student=user, status='active',
            ).values_list('course_id', flat=True)
            return qs.filter(course_id__in=course_ids)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AssignmentCreateSerializer
        return AssignmentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrInstructor()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'success': True, 'data': response.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data['course']
        if request.user.role == 'instructor' and course.instructor_id != request.user.id:
            return Response({'success': False, 'error': {'message': 'Not authorized.'}}, status=403)
        assignment = AssignmentService.create_assignment(
            course=course, created_by=request.user,
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            due_date=serializer.validated_data['due_date'],
            max_score=serializer.validated_data.get('max_score', 100),
        )
        return Response(
            {'success': True, 'data': AssignmentSerializer(assignment).data, 'message': 'Assignment created.'},
            status=status.HTTP_201_CREATED,
        )


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentCreateSerializer
    queryset = Assignment.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminOrInstructor()]

    def get_object(self):
        assignment = super().get_object()
        user = self.request.user
        if user.role == 'student':
            from apps.enrollments.models import Enrollment
            if not Enrollment.objects.filter(
                student=user, course=assignment.course, status=Enrollment.Status.ACTIVE,
            ).exists():
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('You must be enrolled to view this assignment.')
        elif user.role == 'instructor' and assignment.course.instructor_id != user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Not authorized.')
        return assignment

    def retrieve(self, request, *args, **kwargs):
        assignment = self.get_object()
        return Response({'success': True, 'data': AssignmentSerializer(assignment).data})

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        if request.user.role == 'instructor' and assignment.course.instructor_id != request.user.id:
            return Response({'success': False, 'error': {'message': 'Not authorized.'}}, status=403)
        response = super().update(request, *args, **kwargs)
        assignment.refresh_from_db()
        return Response({'success': True, 'data': AssignmentSerializer(assignment).data, 'message': 'Assignment updated.'})

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()
        if request.user.role == 'instructor' and assignment.course.instructor_id != request.user.id:
            return Response({'success': False, 'error': {'message': 'Not authorized.'}}, status=403)
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyAssignmentSubmissionView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    @extend_schema(tags=['Assignments'])
    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        submission = AssignmentSubmission.objects.filter(
            assignment=assignment, student=request.user,
        ).first()
        if not submission:
            return Response({'success': True, 'data': None, 'message': 'No submission yet.'})
        return Response({'success': True, 'data': AssignmentSubmissionSerializer(submission).data})


class SubmissionDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Assignments'])
    def get(self, request, pk):
        submission = get_object_or_404(AssignmentSubmission, pk=pk)
        user = request.user
        if user.role == 'student' and submission.student_id != user.id:
            return Response({'success': False, 'error': {'message': 'Not authorized.'}}, status=403)
        if user.role == 'instructor' and submission.assignment.course.instructor_id != user.id:
            return Response({'success': False, 'error': {'message': 'Not authorized.'}}, status=403)
        if not submission.file:
            return Response({'success': False, 'error': {'message': 'No file attached.'}}, status=404)
        from django.http import FileResponse
        return FileResponse(
            submission.file.open('rb'),
            as_attachment=True,
            filename=submission.file.name.split('/')[-1],
        )


class SubmitAssignmentView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(tags=['Assignments'], request=SubmitAssignmentSerializer)
    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        serializer = SubmitAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = AssignmentService.submit(
            assignment, request.user,
            file=serializer.validated_data.get('file'),
            text_submission=serializer.validated_data.get('text_submission', ''),
        )
        return Response(
            {'success': True, 'data': AssignmentSubmissionSerializer(submission).data, 'message': 'Assignment submitted.'},
            status=status.HTTP_201_CREATED,
        )


class GradeSubmissionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrInstructor]

    @extend_schema(tags=['Assignments'], request=GradeSubmissionSerializer)
    def post(self, request, pk):
        submission = get_object_or_404(AssignmentSubmission, pk=pk)
        if request.user.role == 'instructor' and submission.assignment.course.instructor_id != request.user.id:
            return Response({'success': False, 'error': {'message': 'Not authorized.'}}, status=403)
        serializer = GradeSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = AssignmentService.grade_submission(
            submission,
            serializer.validated_data['grade'],
            serializer.validated_data.get('feedback', ''),
            request.user,
        )
        return Response({
            'success': True,
            'data': AssignmentSubmissionSerializer(submission).data,
            'message': 'Submission graded.',
        })


class MySubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    @extend_schema(tags=['Assignments'])
    def get(self, request):
        submissions = AssignmentSubmission.objects.filter(student=request.user).select_related('assignment')
        return Response({
            'success': True,
            'data': AssignmentSubmissionSerializer(submissions, many=True).data,
        })


class AssignmentSubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrInstructor]

    @extend_schema(tags=['Assignments'])
    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        if request.user.role == 'instructor' and assignment.course.instructor_id != request.user.id:
            return Response({'success': False, 'error': {'message': 'Not authorized.'}}, status=403)
        submissions = assignment.submissions.select_related('student')
        return Response({
            'success': True,
            'data': AssignmentSubmissionSerializer(submissions, many=True).data,
        })
