"""
Publication gates (docs/LEGAL_AND_PUBLICATION_GATES.md).

These functions are the single source of truth used by views, templates, admin dashboard and
tests. They never raise; they return booleans (and a human-readable reason where useful).
"""

from __future__ import annotations

from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _

from core import clock, flags


@dataclass(frozen=True)
class GateStatus:
    key: str
    open: bool
    reason: str


def legal_pages_available() -> bool:
    """G1 — the five legal pages are published in their official Italian version."""
    from legal.services import all_official_pages_published

    return all_official_pages_published()


def public_forms_enabled() -> GateStatus:
    """G2 — public forms requiring the privacy information are enabled only when G1 passes."""
    if legal_pages_available():
        return GateStatus("public_forms", True, str(_("Pagine legali pubblicate.")))
    if flags.is_enabled("forms_override_without_legal"):
        return GateStatus(
            "public_forms",
            True,
            str(_("Override amministrativo attivo (forms_override_without_legal) — tracciato in audit.")),
        )
    return GateStatus(
        "public_forms",
        False,
        str(_("I form pubblici sono disattivati finché le pagine legali ufficiali non sono pubblicate.")),
    )


def phase3_public() -> bool:
    """G3 — Phase 3 content is public only with explicit authorisation AND from 2 Oct 2026."""
    return flags.is_enabled("phase3_public")


def forum_banner_visible() -> bool:
    """G4a — homepage Forum banner until 2 Oct 2026 (CMS schedulable)."""
    return flags.is_enabled("forum_banner")


def forum_permanent_mode() -> bool:
    """G4b — Forum page in 'Forum Permanent' mode after the Rovigo event."""
    return flags.is_enabled("forum_permanent_mode")


def virtual_forum_enabled() -> bool:
    """G11 — Virtual Forum behind a flag until after the Morocco forum, and never before G1.

    ``core.phases`` declares ``depends_on=("legal_pages_available",)`` and the phase console tells the administrator
    that a closed dependency blocks the flag: the gate enforces it (W4-D part 2, F-3). An organisation publishes there
    under participation rules the legal pages carry, and its «Créer un compte» leads to G2's sign-up.
    """
    return flags.is_enabled("virtual_forum") and legal_pages_available()


def newsletter_enabled() -> bool:
    """The newsletter's form and sending: its flag, and G1 — the consent text lives in the legal pages (``core.phases``
    ``depends_on``; W4-D part 2, F-3). G2's QA override opens the forms only, never this."""
    return flags.is_enabled("newsletter") and legal_pages_available()


def snapshot() -> dict:
    forms = public_forms_enabled()
    return {
        "now": clock.now(),
        "legal_pages_available": legal_pages_available(),
        "public_forms_enabled": forms.open,
        "public_forms_reason": forms.reason,
        "phase3_public": phase3_public(),
        "forum_banner_visible": forum_banner_visible(),
        "forum_permanent_mode": forum_permanent_mode(),
        "virtual_forum_enabled": virtual_forum_enabled(),
        "newsletter_enabled": newsletter_enabled(),
    }
