# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .services import link_user

@receiver(post_save, sender=User)
def create_user_mapping(sender, instance, created, **kwargs):
    if created:
        # Replace this with however you store Supabase UUID
        supabase_uuid = getattr(instance, "supabase_uuid", None)
        if supabase_uuid:
            link_user(instance.id, supabase_uuid)