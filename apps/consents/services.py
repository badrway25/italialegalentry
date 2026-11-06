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
# V5.16 §3 — the forms' legal-basis UX (docs/compliance/FORMS_LEGAL_BASIS_UX.md):
# * category A (REQUIRED processing — answering the request, providing the requested service): the team's own wording
#   is an ACKNOWLEDGEMENT («J’ai lu …»), never a consent;
# * category B (OPTIONAL processing): a separate, specific, unticked consent, and only where such a purpose exists
#   (the newsletter, prescribed; the selection's identity disclosure, per request).
# Until V5.16 the purposes without a prescribed sentence reused the company form's locked sentence, «… et je consens
# au traitement de mes données pour le suivi de la présente demande» (CONTENT_PENDING_LEGAL_REVIEW): a consent asked
# for processing that is necessary to answer the request. That reuse was the team's choice, not a prescription, so it
# is replaced by the team's acknowledgement. The prescribed sentences themselves are unchanged (LOCKED COPY below).
REUSED_CONSENT_KEYS: dict[str, str] = {}
#: The locked key the earlier reuse pointed at: a current text row still carrying it is versioned to the
#: acknowledgement.
RETIRED_REUSE_KEY = "p1.companies.form.consent"
#: French only, like the prescribed sentences it sits beside (they too fall back to French, `lang="fr"`): it is the
#: first half of a locked sentence, so the catalogue's locked-fragment rule keeps it out of the .po files until the
#: legal lead approves it with P-1/P-2 (FORMS_LEGAL_BASIS_UX.md §3) and lane D adds its translations.
ACKNOWLEDGEMENT_TEXT = "J’ai lu l’information sur le traitement des données personnelles."
ACKNOWLEDGEMENT_PURPOSES = (
    ConsentPurpose.INSTITUTION_PROPOSAL,
    ConsentPurpose.UNIVERSITY_PROPOSAL,
    ConsentPurpose.CONTACT,
    ConsentPurpose.ORIENTATION,
)
UI_CONSENT_TEXTS = {
    # category A: acknowledgement of the notice + acceptance of the terms (a contract), not a consent
    ConsentPurpose.ACCOUNT_TERMS: "J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation.",
    ConsentPurpose.COMMUNITY: "J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation du Forum Virtuel.",
    **dict.fromkeys(ACKNOWLEDGEMENT_PURPOSES, ACKNOWLEDGEMENT_TEXT),
}
#: LOCKED COPY — LEGAL REVIEW REQUIRED (V5.16 §3). The implementation document prescribes these sentences verbatim
#: (IMPL p.2 §1.1, p.5 §2.1); the team never rewords them. Each asks a «consent» for processing that ANX §3 founds on
#: art. 6(1)(b) — the conflict OF-09. The proposed compliant wording (an acknowledgement, no consent) is the owner's and
#: the legal lead's to approve: docs/compliance/FORMS_LEGAL_BASIS_UX.md §3. Both forms depend on Allegato 1 and stay
#: closed (G2). The newsletter's prescribed consent (p3.news.newsletter_consent) is a real optional consent (category
#: B, art. 6(1)(a), ANX §3) on its own form, and is compliant as prescribed.
#: Category B (V5.16 §3): the only purposes recorded here that are a real, optional and revocable consent. Every other
#: purpose's record is the acknowledgement of a notice (or acceptance of terms), not a consent that can be withdrawn —
#: the back office's withdrawal action should be limited to these (request to the owner of apps/consents/admin.py).
CONSENT_PURPOSES = (ConsentPurpose.NEWSLETTER,)
LOCKED_COPY_LEGAL_REVIEW_REQUIRED = {
    ConsentPurpose.COMPANY_NEEDS: "p1.companies.form.consent",
    ConsentPurpose.FORUM_REGISTRATION: "p2.forum.registration.consent",
}


def consent_text_for(purpose: str, language: str | None = None) -> ConsentText:
    """Return the current wording (French official source; other languages fall back)."""
    lang = (language or translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    qs = ConsentText.objects.filter(purpose=purpose, is_current=True)
    row = (
        qs.filter(language=lang).order_by("-version").first()
        or qs.filter(language=settings.CONTENT_FALLBACK_LANGUAGE).order_by("-version").first()
    )
    if row and not (purpose in ACKNOWLEDGEMENT_PURPOSES and row.locked_key == RETIRED_REUSE_KEY):
        return row
    # no row yet, or the earlier reuse of the company form's consent still current (a database migrated but not yet
    # re-seeded): ensure_consent_text versions it to the acknowledgement, so a record never points at a consent
    # sentence the form no longer shows (review v516-p2, minor 1)
    return ensure_consent_text(purpose)


def ensure_consent_text(purpose: str) -> ConsentText:
    """Idempotently create the v1 French wording of a purpose from the locked registry."""
    key = LOCKED_CONSENT_KEYS.get(purpose) or REUSED_CONSENT_KEYS.get(purpose)
    if key:
        text = locked_content.text(key, "fr")
        source = f"locked:{key}"
    elif purpose in ACKNOWLEDGEMENT_PURPOSES:
        text = UI_CONSENT_TEXTS[purpose]
        source = "ui-string (acknowledgement, V5.16 §3; CONTENT_PENDING_LEGAL_REVIEW)"
    else:
        text = UI_CONSENT_TEXTS[purpose]
        source = "ui-string (CONTENT_PENDING_LEGAL_REVIEW)"
    if purpose in ACKNOWLEDGEMENT_PURPOSES:
        current = (
            ConsentText.objects.filter(purpose=purpose, language="fr", is_current=True).order_by("-version").first()
        )
        if current and current.locked_key == RETIRED_REUSE_KEY:
            # the earlier reuse of the company form's consent: a NEW version, so the records keep what was shown
            ConsentText.objects.filter(purpose=purpose, language="fr").update(is_current=False)
            return ConsentText.objects.create(
                purpose=purpose,
                language="fr",
                version=current.version + 1,
                text=text,
                locked_key="",
                source=source,
                effective_from=clock.now(),
            )
        if current:
            return current
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
