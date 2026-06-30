from rest_framework import serializers

from certificates.models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title',
            'certificate_number', 'title', 'issued_at', 'pdf_file',
            'is_valid', 'revoked_at', 'revoke_reason',
        ]
        read_only_fields = [
            'certificate_number', 'title', 'issued_at',
            'pdf_file', 'is_valid', 'revoked_at', 'revoke_reason',
        ]
