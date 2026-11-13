"""
Idempotent seed of the eight prescribed pathways (structural skeleton only).

* Keys, order, titles and descriptions come from the locked registry (``p3.persons.pathways``).
* Rows are created SCHEDULED for the Phase 3 date (gate G3); editors may publish/unpublish later.
* Steps are a neutral, non-legal skeleton flagged ``pending_legal_review`` (headings only are public).
* Authorities are generic designations literally present in the locked texts — no URL is invented.
* The seed never overwrites editorial changes: only the locked attributes (order, locked flag) are enforced,
  and the step skeleton is created only when a pathway has no steps at all.
"""

from __future__ import annotations

from django.conf import settings

from cms.models import PublicationStatus
from core.seeds import register_seed
from pathways.models import Pathway, PathwayStep, locked_pathway_entries
from pathways.services import DEFAULT_ICONS

# CONTENT_PENDING_LEGAL_REVIEW — generic orientation steps, identical for every pathway. They describe
# the platform's accompaniment logic (orientation → preparation → regular procedure → before departure →
# after arrival) and contain no eligibility criterion, deadline or legal condition.
GENERIC_STEPS_FR: tuple[str, ...] = (
    "S’orienter",
    "Préparer la documentation généralement requise",
    "Suivre la procédure régulière auprès des acteurs compétents",
    "Se préparer avant le départ",
    "Accompagnement après l’arrivée",
)

# Only names that appear verbatim in the locked glossary / FAQ texts. ``url`` intentionally blank.
_UNIVERSAL_AUTHORITIES: tuple[str, ...] = (
    "représentations diplomatiques et consulaires italiennes",
    "Questura",
    "Prefettura",
)
_SPORTELLO_UNICO = "Sportello Unico per l’Immigrazione"
# The locked glossary describes the Sportello Unico as competent for "certaines entrées pour travail ou
# regroupement familial": it is pre-filled only for those pathways.
_SPORTELLO_PATHWAYS: frozenset[str] = frozenset(
    {"salaried_work", "skilled_work_eu_blue_card", "family_reunification", "other_regular_routes"}
)

EDITORIAL_NOTE = "CONTENT_PENDING_LEGAL_REVIEW — squelette structurel généré ; contenus détaillés à vérifier"


def default_authorities(key: str) -> list[dict]:
    names = list(_UNIVERSAL_AUTHORITIES)
    if key in _SPORTELLO_PATHWAYS:
        names.insert(1, _SPORTELLO_UNICO)
    return [{"name": name, "url": ""} for name in names]


def _ensure_steps(pathway: Pathway) -> int:
    if pathway.steps.exists():
        return 0
    created = 0
    for position, title in enumerate(GENERIC_STEPS_FR, start=1):
        PathwayStep.objects.create(
            pathway=pathway, order=position, title_fr=title, text_fr="", pending_legal_review=True
        )
        created += 1
    return created


def _enforce_order(rows: dict[str, Pathway]) -> int:
    """Re-align ``order`` with the prescribed sequence without violating the unique constraint."""
    entries = locked_pathway_entries()
    wanted = {entry["key"]: position for position, entry in enumerate(entries, start=1)}
    drifted = [rows[key] for key, position in wanted.items() if key in rows and rows[key].order != position]
    if not drifted:
        return 0
    for row in drifted:  # park on temporary values first
        row.order = 1000 + wanted[row.key]
        row.save(update_fields=["order", "updated_at"])
    for row in drifted:
        row.order = wanted[row.key]
        row.save(update_fields=["order", "updated_at"])
    return len(drifted)


@register_seed("pathways.pathways", order=40)
def seed_pathways() -> str:
    created_rows = created_steps = 0
    for position, entry in enumerate(locked_pathway_entries(), start=1):
        key = entry["key"]
        pathway, was_created = Pathway.objects.get_or_create(
            key=key,
            defaults={
                "order": position,
                "locked": True,
                "icon": DEFAULT_ICONS.get(key, ""),
                "status": PublicationStatus.SCHEDULED,
                "publish_at": settings.ILE["PHASE3_DATE"],
                "authorities": default_authorities(key),
                "editorial_note": EDITORIAL_NOTE,
            },
        )
        created_rows += int(was_created)
        if not pathway.locked:
            pathway.locked = True
            pathway.save(update_fields=["locked", "updated_at"])
        created_steps += _ensure_steps(pathway)
    realigned = _enforce_order({p.key: p for p in Pathway.objects.all()})
    return (
        f"{created_rows} pathway(s) created, {created_steps} skeleton step(s) created, "
        f"{realigned} order(s) realigned (status SCHEDULED for Phase 3; content CONTENT_PENDING_LEGAL_REVIEW)"
    )
