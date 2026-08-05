import os

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_extension(value, allowed_extensions):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Unsupported file type "{ext}". Allowed: {", ".join(allowed_extensions)}'
        )


def validate_file_size(value, max_size=None):
    max_size = max_size or settings.MAX_UPLOAD_SIZE
    if value.size > max_size:
        raise ValidationError(
            f'File size exceeds maximum allowed ({max_size // (1024 * 1024)}MB).'
        )


def validate_image(value):
    validate_file_extension(value, settings.ALLOWED_IMAGE_EXTENSIONS)
    validate_file_size(value)


def validate_video(value):
    validate_file_extension(value, settings.ALLOWED_VIDEO_EXTENSIONS)
    validate_file_size(value)


def validate_document(value):
    validate_file_extension(value, settings.ALLOWED_DOCUMENT_EXTENSIONS)
    validate_file_size(value)
