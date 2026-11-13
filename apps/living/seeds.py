"""
Living seeds — idempotent: the 10 initial topics are created as PUBLISHED categories.
No sheet is seeded (content is CONTENT_PENDING_LEGAL_REVIEW); editorial changes are never overwritten.
"""

from __future__ import annotations

from django.contrib.auth.models import Group, Permission

from cms.models import PublicationStatus
from core.seeds import register_seed
from living.catalogue import INITIAL_TOPICS
from living.models import LivingTopic


@register_seed("living.topics", order=45)
def seed_topics() -> str:
    created = 0
    for spec in INITIAL_TOPICS:
        _obj, was_created = LivingTopic.objects.get_or_create(
            slug=spec.slug,
            defaults={
                "name_fr": spec.name_fr,
                "icon": spec.icon,
                "order": spec.order,
                "status": PublicationStatus.PUBLISHED,
                "editorial_note": "Seed initial — intro_fr: CONTENT_PENDING_LEGAL_REVIEW",
            },
        )
        created += int(was_created)
    return f"{created} topic(s) created, {len(INITIAL_TOPICS)} ensured; no sheet seeded (CONTENT_PENDING_LEGAL_REVIEW)"


@register_seed("living.publish_permission", order=46)
def seed_publish_permission() -> str:
    perm = Permission.objects.filter(content_type__app_label="living", codename="publish_livingsheet").first()
    if perm is None:
        return "publish_livingsheet permission not yet available"
    group, _created = Group.objects.get_or_create(name="role:administrator")
    group.permissions.add(perm)
    return "living.publish_livingsheet granted to role:administrator"
