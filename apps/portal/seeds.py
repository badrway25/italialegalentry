"""
Reserved-area seeds — nothing is published by the seed.

One DRAFT notice is created so the back-office shows how ``PortalNotice`` works. It is a practical
reminder about data minimisation (team UI text, no legal content) and stays invisible until an
editor reviews and publishes it. Editorial changes are never overwritten (``get_or_create`` on the
stable ``editorial_note`` marker, defaults only on creation).
"""

from cms.models import PublicationStatus
from core.seeds import register_seed
from portal.models import NoticeAudience, PortalNotice

DRAFT_NOTICE_MARKER = "seed:portal.documents_reminder"


@register_seed("portal.draft_notice", order=80)
def seed_draft_notice():
    _obj, created = PortalNotice.objects.get_or_create(
        editorial_note=DRAFT_NOTICE_MARKER,
        defaults={
            "audience": NoticeAudience.ALL,
            "heading_fr": "Vos documents",
            "body_fr": (
                "Ne téléversez que les documents qui vous sont demandés dans le cadre du suivi de votre demande. "
                "Vous pouvez les supprimer à tout moment depuis la rubrique « Mes documents »."
            ),
            "order": 10,
            "status": PublicationStatus.DRAFT,
        },
    )
    return f"{int(created)} draft portal notice created (unpublished)"
