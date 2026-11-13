"""Partner services — the only place that decides what the public may see (gate G6)."""

from __future__ import annotations

from dataclasses import dataclass

from django.db.models import QuerySet

from cms.translation import resolve
from partners.models import Partner, PartnerKind


def authorized_partners(kind: str | None = None) -> QuerySet[Partner]:
    """Publicly visible partners: live editorial status AND written authorisation."""
    qs = Partner.objects.authorized().select_related("logo").prefetch_related("translations")
    if kind:
        qs = qs.filter(kind=kind)
    return qs.order_by("order", "name")


@dataclass(frozen=True)
class PartnerCard:
    partner: Partner
    description: str
    lang: str
    is_fallback: bool


@dataclass(frozen=True)
class PartnerGroup:
    kind: str
    label: str
    cards: list[PartnerCard]


def card_for(partner: Partner, lang: str) -> PartnerCard:
    row, effective, is_fallback = resolve(partner, lang)
    description = row.description if row and row.description else partner.description_fr
    if not (row and row.description):
        effective, is_fallback = "fr", lang.split("-")[0] != "fr"
    return PartnerCard(partner=partner, description=description, lang=effective, is_fallback=is_fallback)


def grouped_by_kind(lang: str = "fr") -> list[PartnerGroup]:
    """Authorised partners grouped in the fixed order of ``PartnerKind`` (empty groups omitted)."""
    by_kind: dict[str, list[PartnerCard]] = {}
    for partner in authorized_partners():
        by_kind.setdefault(partner.kind, []).append(card_for(partner, lang))
    return [
        PartnerGroup(kind=value, label=str(label), cards=by_kind[value])
        for value, label in PartnerKind.choices
        if value in by_kind
    ]
