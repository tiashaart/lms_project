import io
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone

from certificates.models import Certificate


class CertificateService:
    """Generate and manage course completion certificates."""

    @classmethod
    def generate_certificate(cls, student, course):
        """Auto-generate certificate when course is completed."""
        existing = Certificate.objects.filter(student=student, course=course).first()
        if existing:
            return existing

        certificate = Certificate.objects.create(
            student=student,
            course=course,
            certificate_number=Certificate.generate_certificate_number(),
            title=f'Certificate of Completion - {course.title}',
        )

        pdf_content = cls._generate_pdf(certificate)
        if pdf_content:
            filename = f'{certificate.certificate_number}.pdf'
            certificate.pdf_file.save(filename, ContentFile(pdf_content), save=True)

        return certificate

    @classmethod
    def _generate_pdf(cls, certificate):
        """Generate PDF certificate using ReportLab."""
        try:
            from reportlab.lib.pagesizes import landscape, A4
            from reportlab.lib.units import inch
            from reportlab.pdfgen import canvas
        except ImportError:
            return None

        buffer = io.BytesIO()
        width, height = landscape(A4)
        c = canvas.Canvas(buffer, pagesize=landscape(A4))

        c.setFont('Helvetica-Bold', 28)
        c.drawCentredString(width / 2, height - 1.5 * inch, 'Hope Academy LMS')

        c.setFont('Helvetica', 18)
        c.drawCentredString(width / 2, height - 2.2 * inch, 'Certificate of Completion')

        c.setFont('Helvetica', 14)
        c.drawCentredString(
            width / 2, height - 3 * inch,
            'This is to certify that',
        )

        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(
            width / 2, height - 3.6 * inch,
            certificate.student.full_name,
        )

        c.setFont('Helvetica', 14)
        c.drawCentredString(
            width / 2, height - 4.2 * inch,
            'has successfully completed the course',
        )

        c.setFont('Helvetica-Bold', 18)
        c.drawCentredString(
            width / 2, height - 4.8 * inch,
            certificate.course.title,
        )

        c.setFont('Helvetica', 10)
        issued = certificate.issued_at.strftime('%B %d, %Y')
        c.drawCentredString(
            width / 2, height - 5.8 * inch,
            f'Issued on {issued}',
        )
        c.drawCentredString(
            width / 2, height - 6.2 * inch,
            f'Certificate No: {certificate.certificate_number}',
        )

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer.read()

    @classmethod
    def revoke_certificate(cls, certificate, reason=''):
        certificate.is_valid = False
        certificate.revoked_at = timezone.now()
        certificate.revoke_reason = reason
        certificate.save()
        return certificate
