"""
Idempotent seeds: the Rovigo edition (2 Oct 2026), its prescribed programme (8 items), the four
speaker functions and two UNAUTHORISED patronage placeholders (logos awaited with written
authorisation — visible in the back-office only, never rendered publicly).
"""

from __future__ import annotations

from cms.models import PublicationStatus
from core.seeds import register_seed
from forum import services
from forum.models import ForumEvent, ForumPartner, PartnerKind

ROVIGO_SLUG = "venetie-maroc-2026"
PLACEHOLDER_PARTNERS = (
    ("Regione del Veneto", PartnerKind.PATRON),
    ("Comune di Rovigo", PartnerKind.PATRON),
)
PLACEHOLDER_NOTE = "loghi da ricevere con autorizzazione"


@register_seed("forum.event", order=40)
def seed_forum_event():
    event, created = ForumEvent.objects.get_or_create(
        slug=ROVIGO_SLUG,
        defaults={
            "is_primary": not ForumEvent.objects.filter(is_primary=True).exists(),
            "status": PublicationStatus.PUBLISHED,
            "editorial_note": "Seed dal registro dei testi bloccati (p2.forum.*)",
        },
    )
    programme = services.ensure_programme(event)
    roles = services.ensure_speaker_roles(event)
    partners = 0
    for order, (name, kind) in enumerate(PLACEHOLDER_PARTNERS, start=1):
        _obj, was_created = ForumPartner.objects.get_or_create(
            event=event,
            name=name,
            defaults={"kind": kind, "order": order * 10, "authorized": False, "note": PLACEHOLDER_NOTE},
        )
        partners += int(was_created)
    return (
        f"event {'created' if created else 'exists'}; programme items +{programme}; speaker roles +{roles}; "
        f"partner placeholders +{partners}"
    )


# The governance module registers its own seeds (the Rovigo 2026 edition and the five commissions of
# FORUM_GOVERNANCE §3). ``core.seeds.discover()`` imports ``<app>.seeds`` and nothing else, so the
# module is imported here — at the bottom, for the same reason ``forum.governance`` is imported at
# the bottom of ``forum.models``: it names this module's ``ROVIGO_SLUG``.
from forum import governance_seeds  # noqa: E402,F401 — registers the governance seeds
