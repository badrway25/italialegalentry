"""Signal receivers: erase a person's files when their account is anonymised; clean up on hard delete."""

from __future__ import annotations

from django.db.models.signals import post_delete
from django.dispatch import receiver

from documents.models import PrivateDocument
from documents.storage import private_storage


def on_user_anonymised(sender, *, user_id, **kwargs):
    from documents.services import purge_user_documents

    purge_user_documents(user_id)


@receiver(post_delete, sender=PrivateDocument, dispatch_uid="documents.remove_file_on_delete")
def remove_file_on_delete(sender, instance: PrivateDocument, **kwargs):
    storage = private_storage()
    if storage.exists(instance.relative_path):
        storage.delete(instance.relative_path)
