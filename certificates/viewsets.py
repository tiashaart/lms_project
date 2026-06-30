from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from certificates.models import Certificate
from certificates.serializers import CertificateSerializer
from certificates.services import CertificateService
from users.permissions import IsAdministrator


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['course', 'is_valid']
    search_fields = ['certificate_number', 'course__title']
    ordering_fields = ['issued_at']
    ordering = ['-issued_at']

    def get_queryset(self):
        user = self.request.user
        qs = Certificate.objects.select_related('student', 'course')
        if user.role in ('admin',) or user.is_superuser:
            return qs.all()
        if user.role == 'instructor':
            return qs.filter(course__instructor=user)
        return qs.filter(student=user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        certificate = self.get_object()
        if not certificate.pdf_file:
            CertificateService.generate_certificate(
                certificate.student, certificate.course,
            )
            certificate.refresh_from_db()

        if not certificate.pdf_file:
            return Response(
                {'detail': 'Certificate PDF not available.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return FileResponse(
            certificate.pdf_file.open('rb'),
            as_attachment=True,
            filename=f'{certificate.certificate_number}.pdf',
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsAdministrator],
    )
    def revoke(self, request, pk=None):
        certificate = self.get_object()
        reason = request.data.get('reason', '')
        CertificateService.revoke_certificate(certificate, reason)
        return Response(CertificateSerializer(certificate).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='verify/(?P<cert_number>[^/.]+)',
    )
    def verify(self, request, cert_number=None):
        try:
            cert = Certificate.objects.get(certificate_number=cert_number)
            return Response({
                'valid': cert.is_valid,
                'student': cert.student.full_name,
                'course': cert.course.title,
                'issued_at': cert.issued_at,
            })
        except Certificate.DoesNotExist:
            return Response(
                {'valid': False, 'detail': 'Certificate not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
