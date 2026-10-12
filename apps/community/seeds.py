"""
Community seeds: the four thematic rooms and the consent wording (idempotent).

Rooms are created once; editorial changes (name, description, categories, publication) are never
overwritten. The whole feature stays invisible until FeatureFlag ``virtual_forum`` is enabled.
"""

from community.models import ParticipantCategory, Room, RoomKind
from consents.models import ConsentPurpose
from consents.services import ensure_consent_text
from core.seeds import register_seed

ROOMS = (
    {
        "slug": "espace-commun",
        "name_fr": "Espace commun",
        "description_fr": "Échanges ouverts à tous les participants du Forum : annonces, questions générales, "
        "suivi des projets nés du Forum.",
        "kind": RoomKind.GENERAL,
        "allowed_categories": [],
        "order": 1,
    },
    {
        "slug": "entreprises",
        "name_fr": "Entreprises",
        "description_fr": "Besoins professionnels, formation et parcours réguliers : espace des entreprises, "
        "associations professionnelles et Chambres de Commerce.",
        "kind": RoomKind.ENTERPRISES,
        "allowed_categories": [
            ParticipantCategory.COMPANY,
            ParticipantCategory.PROFESSIONAL_ASSOCIATION_CHAMBER,
            ParticipantCategory.PROFESSIONAL,
        ],
        "order": 2,
    },
    {
        "slug": "universites-formation",
        "name_fr": "Universités et formation",
        "description_fr": "Formation avant le départ et après l’arrivée, mobilité académique, programmes conjoints.",
        "kind": RoomKind.UNIVERSITIES,
        "allowed_categories": [ParticipantCategory.UNIVERSITY_TRAINING, ParticipantCategory.PROFESSIONAL],
        "order": 3,
    },
    {
        "slug": "institutions",
        "name_fr": "Institutions",
        "description_fr": "Coopération institutionnelle Vénétie–Maroc, organismes du travail et représentations "
        "diplomatiques et consulaires.",
        "kind": RoomKind.INSTITUTIONS,
        "allowed_categories": [
            ParticipantCategory.INSTITUTION,
            ParticipantCategory.LABOUR_BODY,
            ParticipantCategory.DIPLOMATIC_CONSULAR,
        ],
        "order": 4,
    },
)


@register_seed("community.rooms", order=70)
def seed_rooms():
    created = 0
    for row in ROOMS:
        defaults = {k: v for k, v in row.items() if k != "slug"}
        defaults["published"] = True
        defaults["is_moderated"] = True
        _obj, was_created = Room.objects.get_or_create(slug=row["slug"], defaults=defaults)
        created += int(was_created)
    return f"{created} room(s) created"


@register_seed("community.consent_text", order=71)
def seed_consent_text():
    ensure_consent_text(ConsentPurpose.COMMUNITY)
    return "community consent wording ensured (CONTENT_PENDING_LEGAL_REVIEW)"
