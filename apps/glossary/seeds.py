"""
Seed of the ten prescribed glossary terms (Implementation document §3.8.3, key ``p3.glossary.terms``).

Idempotent: rows are matched by ``key``; only the locked columns (term, definition FR, is_locked)
are re-synchronised from the registry. Editorial fields (status, source, related terms, review
date, translations) are never overwritten once the row exists.
"""

from __future__ import annotations

import datetime as dt

from django.conf import settings

from cms.models import PublicationStatus
from core.seeds import register_seed
from glossary import registry
from glossary.models import Term

# Date of the written transmission of the prescribed texts (Implementation document, 14 Sept 2026).
LOCKED_SOURCE_DATETIME = dt.datetime(2026, 9, 14, 12, 0, tzinfo=settings.ROME)
LOCKED_SOURCE_LABEL = "Document d’implémentation Italy Legal Entry™ — 14 septembre 2026, §3.8.3"
LOCKED_EDITORIAL_NOTE = "Testo bloccato — Documento di implementazione 14/09/2026 §3.8.3 (p3.glossary.terms)"

# Prescribed terms that naturally reference each other (navigation aid only — no new content).
INITIAL_RELATIONS: tuple[tuple[str, str], ...] = (
    ("visto_ingresso", "permesso_di_soggiorno"),
    ("visto_ingresso", "nulla_osta"),
    ("permesso_di_soggiorno", "questura_prefettura"),
    ("nulla_osta", "decreto_flussi"),
    ("nulla_osta", "ricongiungimento_familiare"),
    ("carta_blu_ue", "permesso_di_soggiorno"),
    ("legalizzazione_apostille", "dichiarazione_di_valore"),
)


@register_seed("glossary.locked_terms", order=41)
def seed_locked_terms() -> str:
    created = resynced = 0
    created_keys: set[str] = set()
    for entry in registry.terms():
        existing = Term.objects.filter(key=entry["key"]).first()
        if existing is None:
            Term.objects.create(
                key=entry["key"],
                term=entry["term"],
                definition_fr=entry["definition"],
                is_locked=True,
                status=PublicationStatus.PUBLISHED,
                source=LOCKED_SOURCE_LABEL,
                last_reviewed_at=LOCKED_SOURCE_DATETIME,
                editorial_note=LOCKED_EDITORIAL_NOTE,
            )
            created += 1
            created_keys.add(entry["key"])
            continue
        drifted = (
            not existing.is_locked or existing.term != entry["term"] or existing.definition_fr != entry["definition"]
        )
        if drifted:
            existing.is_locked = True
            existing.save()  # save() re-asserts the registry wording
            resynced += 1
    # Initial related-term links are only proposed for freshly created rows (editors keep control).
    by_key = {t.key: t for t in Term.objects.filter(key__in=registry.keys())}
    for left, right in INITIAL_RELATIONS:
        if left in created_keys or right in created_keys:
            by_key[left].related.add(by_key[right])
    return f"{created} locked term(s) created, {resynced} re-synchronised, {len(registry.keys())} total locked"
