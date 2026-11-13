"""
The links to the legal pages that exist — the footer's «Informations légales» and the console's foot (V5.12 Q2, the
owner's answer of 28 Oct 2026; V5.14 §13, «privacy is not blocked by Allegato 1»).

A legal page is linked only once it is published and showable (``LegalDocument.is_available``): the privacy notice and
the cookie information (categories A and B, lane P) as soon as they are; the official notices, the terms and the
disclaimer (C and D) only with their verified Italian source. An unpublished page is ABSENT — never a link to «Page en
cours de préparation». When none is published the caller draws nothing: the footer's column leaves, the grid reflows.

The per-document gate is lane P's ``legal.services.document_available`` (cached per kind); the signals below call
``legal.services.invalidate()`` whenever a legal document is saved or deleted, so a publication shows in the footer at
once, whichever path saved it.
"""

from __future__ import annotations

from django import template
from django.db.models.signals import post_delete, post_save
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _

register = template.Library()

#: The order and the words of the footer's list (the binding glossary, docs/I18N_RTL.md §5: «Privacy Policy» and
#: «Cookie Policy» stay in the original in every language). ``lang`` marks the English names inside another language.
LEGAL_LINKS: tuple[tuple[str, object, str], ...] = (
    ("notices", _("Mentions légales"), ""),
    ("privacy", "Privacy Policy", "en"),
    ("cookies", "Cookie Policy", "en"),
    ("terms", _("Conditions d’utilisation"), ""),
    ("disclaimer", _("Avertissement"), ""),
)


def _forget(**_kwargs) -> None:
    from legal import services

    services.invalidate()


def _connect() -> None:
    from legal.models import LegalDocument

    post_save.connect(_forget, sender=LegalDocument, weak=False, dispatch_uid="legal_links.saved")
    post_delete.connect(_forget, sender=LegalDocument, weak=False, dispatch_uid="legal_links.deleted")


_connect()


def available_kinds() -> frozenset[str]:
    """The kinds of the legal documents a visitor may open now."""
    from legal import services

    return frozenset(kind for kind, _label, _lang in LEGAL_LINKS if services.document_available(kind))


@register.simple_tag
def legal_links(*kinds: str) -> list[dict[str, str]]:
    """``{% legal_links as links %}`` — or ``{% legal_links "privacy" "terms" as links %}`` for a subset, in the
    footer's order: [{kind, label, lang, url}] of the PUBLISHED legal pages only."""
    wanted = set(kinds) if kinds else None
    available = available_kinds()
    rows = []
    for kind, label, lang in LEGAL_LINKS:
        if (wanted is not None and kind not in wanted) or kind not in available:
            continue
        try:
            url = reverse(f"legal:{kind}")
        except NoReverseMatch:  # pragma: no cover - the legal URLs are not mounted
            continue
        rows.append({"kind": kind, "label": str(label), "lang": lang, "url": url})
    return rows
