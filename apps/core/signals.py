from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core import flags
from core.models import FeatureFlag


@receiver(post_save, sender=FeatureFlag)
@receiver(post_delete, sender=FeatureFlag)
def _invalidate_flags(sender, **kwargs):
    flags.invalidate()
