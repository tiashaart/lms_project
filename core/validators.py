import os

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_extension(file, allowed_extensions):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Unsupported file type "{ext}". Allowed: {", ".join(allowed_extensions)}'
        )


def validate_file_size(file, max_size=None):
    max_size = max_size or settings.MAX_UPLOAD_SIZE
    if file.size > max_size:
        raise ValidationError(
            f'File size exceeds maximum allowed ({max_size // (1024 * 1024)} MB).'
        )


def validate_learning_material(file):
    validate_file_extension(file, settings.ALLOWED_MATERIAL_EXTENSIONS)
    validate_file_size(file)


def validate_profile_picture(file):
    validate_file_extension(file, settings.ALLOWED_IMAGE_EXTENSIONS)
    validate_file_size(file, max_size=5 * 1024 * 1024)


def validate_assignment_file(file):
    validate_file_extension(file, settings.ALLOWED_ASSIGNMENT_EXTENSIONS)
    validate_file_size(file)
