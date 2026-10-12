"""
Seed of the nine prescribed FAQ entries (Implementation document §3.8.2, key ``p3.faq.items``).

Idempotent: rows are matched by ``key``; only the locked columns (question/answer FR, is_locked)
are re-synchronised from the registry. Editorial fields (order, category, status, dates,
translations) are never overwritten once the row exists.
"""

from __future__ import annotations

import datetime as dt

from cms.models import PublicationStatus
from core.seeds import register_seed
from faq import registry
from faq.models import GENERAL_CATEGORY_SLUG, FAQCategory, FAQItem

# Date of the written transmission of the prescribed texts (Implementation document, 14 Sept 2026).
LOCKED_SOURCE_DATE = dt.date(2026, 9, 14)
LOCKED_EDITORIAL_NOTE = "Testo bloccato — Documento di implementazione 14/09/2026 §3.8.2 (p3.faq.items)"


def ensure_general_category() -> FAQCategory:
    category, _created = FAQCategory.objects.get_or_create(
        slug=GENERAL_CATEGORY_SLUG, defaults={"name_fr": "Général", "order": 0}
    )
    return category


@register_seed("faq.locked_items", order=40)
def seed_locked_faq_items() -> str:
    category = ensure_general_category()
    created = resynced = 0
    for position, entry in enumerate(registry.items(), start=1):
        existing = FAQItem.objects.filter(key=entry["key"]).first()
        if existing is None:
            FAQItem.objects.create(
                key=entry["key"],
                category=category,
                order=position * 10,
                is_locked=True,
                question_fr=entry["question"],
                answer_fr=entry["answer"],
                status=PublicationStatus.PUBLISHED,
                last_updated=LOCKED_SOURCE_DATE,
                editorial_note=LOCKED_EDITORIAL_NOTE,
            )
            created += 1
            continue
        drifted = (
            not existing.is_locked or existing.question_fr != entry["question"] or existing.answer_fr != entry["answer"]
        )
        if drifted:
            existing.is_locked = True
            existing.save()  # save() re-asserts the registry wording
            resynced += 1
    return f"{created} locked FAQ item(s) created, {resynced} re-synchronised, {len(registry.keys())} total locked"
