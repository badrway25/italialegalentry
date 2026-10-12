from __future__ import annotations

from django.conf import settings
from django.utils import translation

from cms import locked_content
from consents.models import ConsentPurpose, ConsentRecord, ConsentText
from core import clock
from core.privacy import hashed_client_ip, truncated_user_agent

# Purposes whose wording is prescribed verbatim by the implementation document.
LOCKED_CONSENT_KEYS = {
    ConsentPurpose.COMPANY_NEEDS: "p1.companies.form.consent",
    ConsentPurpose.FORUM_REGISTRATION: "p2.forum.registration.consent",
    ConsentPurpose.NEWSLETTER: "p3.news.newsletter_consent",
}
# Purposes without a prescribed sentence reuse the §1.1 wording («… pour le suivi de la présente
# demande») — flagged CONTENT_PENDING_LEGAL_REVIEW in docs/CONTENT_SOURCE_MAP.md.
REUSED_CONSENT_KEYS = {
    ConsentPurpose.INSTITUTION_PROPOSAL: "p1.companies.form.consent",
    ConsentPurpose.UNIVERSITY_PROPOSAL: "p1.companies.form.consent",
    ConsentPurpose.CONTACT: "p1.companies.form.consent",
    ConsentPurpose.ORIENTATION: "p1.companies.form.consent",
}
UI_CONSENT_TEXTS = {
    ConsentPurpose.ACCOUNT_TERMS: "J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation.",
    ConsentPurpose.COMMUNITY: "J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation du Forum Virtuel.",
}


def consent_text_for(purpose: str, language: str | None = None) -> ConsentText:
    """Return the current wording (French official source; other languages fall back)."""
    lang = (language or translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    qs = ConsentText.objects.filter(purpose=purpose, is_current=True)
    row = (
        qs.filter(language=lang).order_by("-version").first()
        or qs.filter(language=settings.CONTENT_FALLBACK_LANGUAGE).order_by("-version").first()
    )
    if row:
        return row
    return ensure_consent_text(purpose)


def ensure_consent_text(purpose: str) -> ConsentText:
    """Idempotently create the v1 French wording of a purpose from the locked registry."""
    key = LOCKED_CONSENT_KEYS.get(purpose) or REUSED_CONSENT_KEYS.get(purpose)
    if key:
        text = locked_content.text(key, "fr")
        source = f"locked:{key}"
    else:
        text = UI_CONSENT_TEXTS[purpose]
        source = "ui-string (CONTENT_PENDING_LEGAL_REVIEW)"
    row, _created = ConsentText.objects.get_or_create(
        purpose=purpose,
        language="fr",
        version=1,
        defaults={"text": text, "locked_key": key or "", "source": source, "effective_from": clock.now()},
    )
    return row


def record_consent(request, purpose: str, email: str, user=None, language: str | None = None) -> ConsentRecord:
    text_row = consent_text_for(purpose, language)
    return ConsentRecord.objects.create(
        purpose=purpose,
        consent_text=text_row,
        email=email.lower().strip(),
        user=user if getattr(user, "is_authenticated", False) else None,
        given_at=clock.now(),
        ip_hash=hashed_client_ip(request) if request else "",
        user_agent=truncated_user_agent(request) if request else "",
        language=(language or (translation.get_language() or "fr")).split("-")[0],
    )


def withdraw(record: ConsentRecord, note: str = "") -> None:
    record.withdrawn_at = clock.now()
    record.withdrawal_note = note[:200]
    record.save(update_fields=["withdrawn_at", "withdrawal_note"])
