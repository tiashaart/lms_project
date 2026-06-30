from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import (
    User,
    UserRole,
    StudentProfile,
    InstructorProfile,
    AdministratorProfile,
)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create role-specific profile on user registration."""
    if not created:
        return

    if instance.role == UserRole.STUDENT:
        StudentProfile.objects.get_or_create(user=instance)
    elif instance.role == UserRole.INSTRUCTOR:
        InstructorProfile.objects.get_or_create(user=instance)
    elif instance.role == UserRole.ADMIN:
        AdministratorProfile.objects.get_or_create(user=instance)
