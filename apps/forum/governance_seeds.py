"""
Seeds of the Forum Permanent governance module — CONFIGURATION ONLY.

Two kinds of seed exist in this codebase and ``core.seeds.demonstration_data_allowed`` is the line
between them. This module stays entirely on the configuration side:

* it creates the Rovigo 2026 edition and the five commissions of FORUM_GOVERNANCE §3, because those
  are the product — REQ-CFG-03 says explicitly that the five rows are seed data and that adding a
  sixth commission is a back-office operation, not a code change;

* it creates NO account, NO participation profile, NO mandate and NO proposal. Those are records
  about real organisations taking part in a real cooperation, and a seeded one is indistinguishable
  from a real one the moment it is written. There is therefore nothing here for
  ``demonstration_data_allowed()`` to guard — and if a later lane adds a demonstration fixture for
  local work, that is the switch it must sit behind, not ``DEBUG``.

Idempotent by construction: every row is a ``get_or_create`` on its natural key, with the editable
text supplied only as ``defaults``, so re-running the seed after the back-office has rewritten a
commission's scope never undoes that edit.
"""

from __future__ import annotations

import datetime as dt

from core.seeds import register_seed
from forum.governance import Commission, CommissionStatus, EditionStatus, ForumEdition

EDITION_KEY = "rovigo-2026"
EDITION_YEAR = 2026

#: The first edition (FORUM_GOVERNANCE §1): «La prima edizione italiana, a Rovigo il 2 ottobre 2026,
#: è l'avvio pubblico del percorso, non il percorso». The edition is the year of work the event
#: opens; the two hours in the Sala della Gran Guardia are the ``forum.ForumEvent`` it links to.
EDITION_DEFAULTS = {
    "year": EDITION_YEAR,
    "title_fr": "Forum permanent juridique et économique Italie–Maroc — édition de Rovigo",
    "city": "Rovigo",
    "country_code": "IT",
    "starts_on": dt.date(2026, 10, 2),
    "status": EditionStatus.PLANNED,
}

#: The five commissions of FORUM_GOVERNANCE §3, in the order the document lists them. They are DATA:
#: nothing in ``forum.governance`` or ``forum.governance_services`` branches on these keys, and a
#: sixth sectoral commission is added from the back-office «senza modifica del codice».
COMMISSIONS: tuple[tuple[str, str, str], ...] = (
    (
        "mobilite-travail-inclusion",
        "Mobilité régulière, travail et inclusion",
        "Parcours légaux, besoins de main-d’œuvre, formation, inclusion.",
    ),
    (
        "juridique-droit-compare",
        "Juridique et droit comparé",
        "Professionnels, ordres, institutions, formation juridique.",
    ),
    (
        "entreprises-investissements",
        "Entreprises, investissements et coopération économique",
        "Systèmes consulaires, entreprises, territoires, partenariats.",
    ),
    (
        "universites-recherche",
        "Universités, recherche et mobilité académique",
        "Partenariats, mobilité des étudiants et des enseignants, recherche.",
    ),
    (
        "formation-competences",
        "Formation et compétences",
        "Parcours cohérents avec les besoins territoriaux et professionnels.",
    ),
)

#: Written on every seeded commission, once, at creation. It says what the commission is FOR, and
#: what it is not: no commission of this Forum names a physical person in its governance field.
GOVERNANCE_NOTE = (
    "Composition mixte italo-marocaine. La gouvernance de la commission (présidence, rythme des "
    "réunions, rapporteurs) est arrêtée par le secrétariat du Forum et consignée ici sans jamais "
    "nommer de personne physique."
)


@register_seed("forum.governance", order=41)
def seed_forum_governance() -> str:
    """Create the edition and its five commissions if they are absent. Never overwrite an edit."""
    edition, created = ForumEdition.objects.get_or_create(key=EDITION_KEY, defaults=EDITION_DEFAULTS)

    # The bridge to the published event page, set only when it is still empty: an edition may
    # legitimately have no public page, and a back-office change must not be undone on deploy.
    if edition.event_id is None:
        from forum.models import ForumEvent
        from forum.seeds import ROVIGO_SLUG

        event = ForumEvent.objects.filter(slug=ROVIGO_SLUG).first()
        if event is not None:
            edition.event = event
            edition.save(update_fields=["event", "updated_at"])

    commissions = 0
    for order, (key, name, scope) in enumerate(COMMISSIONS, start=1):
        _row, was_created = Commission.objects.get_or_create(
            edition=edition,
            key=key,
            defaults={
                "name_fr": name,
                "scope_fr": scope,
                "governance_fr": GOVERNANCE_NOTE,
                "status": CommissionStatus.ACTIVE,
                "order": order * 10,
            },
        )
        commissions += int(was_created)

    return f"edition {'created' if created else 'exists'}; commissions +{commissions}"
