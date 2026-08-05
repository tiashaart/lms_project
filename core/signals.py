import logging

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

logger = logging.getLogger('hope_academy')


def _delete_file(field):
    if field and field.name:
        try:
            field.delete(save=False)
        except Exception as exc:
            logger.warning('Failed to delete file %s: %s', field.name, exc)


@receiver(pre_delete)
def delete_model_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.get_internal_type() in ('FileField', 'ImageField'):
            _delete_file(getattr(instance, field.name, None))


@receiver(pre_save)
def delete_replaced_files(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    for field in instance._meta.fields:
        if field.get_internal_type() not in ('FileField', 'ImageField'):
            continue
        old_file = getattr(old, field.name, None)
        new_file = getattr(instance, field.name, None)
        if old_file and old_file != new_file:
            _delete_file(old_file)
