"""
Legal pages — four categories (owner directive V5.14, 28 Oct 2026; DECISIONS §13).

* **A — privacy** and **B — cookies / technical storage**: drafted from the processing this software
  ACTUALLY performs (``docs/compliance/PRIVACY_PROCESSING_AUDIT.md``; sentence → evidence in
  ``docs/legal/PRIVACY_NOTICE_SOURCES.md``). The Italian text is the master; French, English and Arabic are
  courtesy translations, flagged «pending legal-lead review» in ``translation_status``. They do not depend
  on Allegato 1 and are published on their own.
* **C — substantive content** (disclaimer) and **D — governance** (legal notices, terms): the official Italian
  text of « Allegato 1 — Testi legali » only, pasted verbatim by an authorised user. The technical team never
  writes or translates them.

Every document is published separately. Gate G1 (``legal.services.all_official_pages_published``) still asks
for all five, so publishing A and B alone opens no form that depends on Allegato 1.

An essential fact that cannot be verified is written in the text as an OPEN FIELD, «[DA COMPLETARE — …]».
The preview shows it highlighted; production refuses to publish or show a document that still carries one
(``open_fields_allowed``).
"""

from __future__ import annotations

import hashlib
import json
import re

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class LegalKind(models.TextChoices):
    PRIVACY = "privacy", "Privacy Policy"
    COOKIES = "cookies", "Cookie Policy"
    NOTICES = "notices", _("Note legali")
    TERMS = "terms", _("Condizioni di utilizzo")
    DISCLAIMER = "disclaimer", _("Avvertenze (Disclaimer)")


class LegalStatus(models.TextChoices):
    BLOCKED = "blocked", "BLOCKED_BY_MISSING_OFFICIAL_SOURCE"
    DRAFT = "draft", _("Bozza (testo ufficiale inserito, non ancora pubblicato)")
    PUBLISHED = "published", _("Pubblicato")


LEGAL_SLUGS = {
    LegalKind.PRIVACY: "privacy-policy",
    LegalKind.COOKIES: "cookie-policy",
    LegalKind.NOTICES: "note-legali",
    LegalKind.TERMS: "condizioni-di-utilizzo",
    LegalKind.DISCLAIMER: "avvertenze",
}
LEGAL_URL_NAMES = {
    LegalKind.PRIVACY: "legal:privacy",
    LegalKind.COOKIES: "legal:cookies",
    LegalKind.NOTICES: "legal:notices",
    LegalKind.TERMS: "legal:terms",
    LegalKind.DISCLAIMER: "legal:disclaimer",
}
#: The directive's categories (V5.14 §7): A privacy, B cookie/technical storage, C substantive content, D governance.
LEGAL_CATEGORY = {
    LegalKind.PRIVACY: "A",
    LegalKind.COOKIES: "B",
    LegalKind.DISCLAIMER: "C",
    LegalKind.NOTICES: "D",
    LegalKind.TERMS: "D",
}
#: Written from the verified processing of this software, not from Allegato 1 (V5.14 §2).
VERIFIED_PROCESSING_KINDS = (LegalKind.PRIVACY, LegalKind.COOKIES)
#: Languages of the courtesy translations of an A/B document (the Italian text prevails).
TRANSLATION_LANGUAGES = ("fr", "en", "ar")
#: The open-field marker, the same prefix in every language: «[DA COMPLETARE — OF-02: …]».
OPEN_FIELD_PREFIX = "[DA COMPLETARE"
OPEN_FIELD_RE = re.compile(r"\[DA COMPLETARE[^\]]*\]")
OPEN_FIELD_ID_RE = re.compile(r"\bOF-\d+\b")
#: V5.16 (28 Oct 2026): every open field carries ONE class, written in the marker after its id and in English in every
#: language — «[DA COMPLETARE — OF-02 — PRODUCTION CONFIGURATION REQUIRED: …]». The class says who closes it: the real
#: production infrastructure (it blocks PRODUCTION_CONFIG_COMPLETE), the owner (OF-01, the controller), or the legal
#: review (bases, art. 9, roles, DPO status, retention policies; COMPLIANCE_REVIEW_COMPLETE, V5.17). Whatever the class,
#: production refuses to publish the text while the marker is there.
OPEN_FIELD_CLASSES = {
    "PRODUCTION CONFIGURATION REQUIRED": "production-config",
    "OWNER CONFIRMATION REQUIRED": "owner-confirmation",
    "LEGAL REVIEW REQUIRED": "legal-review",
}
OPEN_FIELD_CLASS_RE = re.compile(r"\b(" + "|".join(OPEN_FIELD_CLASSES) + r")\b")


def open_field_class(marker: str) -> str:
    """The class of one marker («PRODUCTION CONFIGURATION REQUIRED», …), or «?» when it names none or several."""
    found = set(OPEN_FIELD_CLASS_RE.findall(marker))
    return found.pop() if len(found) == 1 else "?"


def open_fields_allowed() -> bool:
    """True only in a preview (development settings): there an open field is shown highlighted.

    ``config/settings/prod.py`` forces it to False, whatever the environment says: production never publishes or
    shows a document that still carries an open field.
    """
    return bool(getattr(settings, "ILE_LEGAL_OPEN_FIELDS_ALLOWED", False))


class TranslationStatus(models.TextChoices):
    PENDING = "pending_legal_review", "Traduzione in attesa di revisione del responsabile legale"
    REVIEWED = "reviewed", "Traduzione rivista dal responsabile legale"


COURTESY_KEYS = {
    LegalKind.PRIVACY: "legal.privacy.fr_courtesy",
    LegalKind.COOKIES: "legal.cookies.fr_courtesy",
    LegalKind.NOTICES: "legal.notices.fr_courtesy",
    LegalKind.TERMS: "legal.terms.fr_courtesy",
    LegalKind.DISCLAIMER: "legal.disclaimer.fr_courtesy",
}


class LegalDocument(TimeStampedModel):
    kind = models.CharField(max_length=12, choices=LegalKind.choices, unique=True)
    status = models.CharField(max_length=10, choices=LegalStatus.choices, default=LegalStatus.BLOCKED, db_index=True)
    title_it = models.CharField(_("titolo ufficiale (IT)"), max_length=200, blank=True)
    body_it = models.TextField(
        _("testo ufficiale (IT)"),
        blank=True,
        help_text=_(
            "Incollare INTEGRALMENTE il testo dell’Allegato 1 — Testi legali (sezione corrispondente), "
            "senza riformulazioni. Paragrafi separati da una riga vuota; titoli di sezione su riga propria "
            "preceduti da «## ». Non pubblicare la nota operativa interna della Cookie Policy."
        ),
    )
    source_reference = models.CharField(
        _("riferimento della fonte"),
        max_length=200,
        blank=True,
        help_text=_("es. «Allegato 1 — Testi legali, sez. 1, trasmesso il 2026-09-…»"),
    )
    version = models.PositiveIntegerField(default=0, editable=False)
    effective_date = models.DateField(_("data di efficacia"), null=True, blank=True)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True, editable=False)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    checksum = models.CharField(max_length=64, blank=True, editable=False)
    courtesy_fr_enabled = models.BooleanField(
        _("mostra la traduzione di cortesia FR accanto al testo italiano"),
        default=False,
        help_text=_("Solo dopo conferma scritta dell’Avv. Badrane (Annexe 1, istruzioni)."),
    )

    translations = models.JSONField(
        "traduzioni di cortesia (FR/EN/AR)",
        default=dict,
        blank=True,
        help_text=(
            "Solo informativa privacy e cookie: {lingua: {title, body, notice, italian_link, pending}}. "
            "Il testo italiano prevale."
        ),
    )
    translation_status = models.CharField(
        "stato delle traduzioni",
        max_length=24,
        choices=TranslationStatus.choices,
        default=TranslationStatus.PENDING,
    )
    seed_checksum = models.CharField(max_length=64, blank=True, editable=False)

    class Meta:
        verbose_name = _("pagina legale")
        verbose_name_plural = _("pagine legali")
        ordering = ["kind"]
        permissions = [("publish_legaldocument", "Can publish official legal documents")]

    def __str__(self) -> str:
        return f"{self.get_kind_display()} [{self.status}]"

    @property
    def slug(self) -> str:
        return LEGAL_SLUGS[self.kind]

    @property
    def url_name(self) -> str:
        return LEGAL_URL_NAMES[self.kind]

    @property
    def courtesy_key(self) -> str:
        return COURTESY_KEYS[self.kind]

    @property
    def category(self) -> str:
        return LEGAL_CATEGORY[self.kind]

    @property
    def is_available(self) -> bool:
        if self.status != LegalStatus.PUBLISHED or not self.body_it.strip():
            return False
        return open_fields_allowed() or not self.open_fields()

    def open_fields(self) -> list[str]:
        """Every distinct open-field marker in the Italian text and its translations, in reading order."""
        texts = [self.title_it, self.body_it]
        for lang in sorted(self.translations or {}):
            entry = self.translations[lang] or {}
            texts.extend(str(value) for value in entry.values())
        seen: list[str] = []
        for text in texts:
            for marker in OPEN_FIELD_RE.findall(text or ""):
                if marker not in seen:
                    seen.append(marker)
        return seen

    def open_field_ids(self) -> list[str]:
        """The owner's questions still open in this document («OF-02», …), sorted; «?» for a marker without one."""
        ids: set[str] = set()
        for marker in self.open_fields():
            ids.update(OPEN_FIELD_ID_RE.findall(marker) or ["?"])
        return sorted(ids, key=lambda i: (len(i), i))

    def open_field_classes(self) -> list[tuple[str, list[str]]]:
        """[(class, [OF ids])] in the order of ``OPEN_FIELD_CLASSES`` (then «?»): the preview, the back office."""
        by_class: dict[str, set[str]] = {}
        for marker in self.open_fields():
            ids = OPEN_FIELD_ID_RE.findall(marker) or ["?"]
            by_class.setdefault(open_field_class(marker), set()).update(ids)
        order = [*OPEN_FIELD_CLASSES, "?"]
        return [(label, sorted(by_class[label], key=lambda i: (len(i), i))) for label in order if label in by_class]

    def translation_for(self, language: str | None) -> dict | None:
        """The courtesy translation for ``language``, or None (Italian, or no translation)."""
        if not language or language == "it":
            return None
        entry = (self.translations or {}).get(language)
        if not entry or not str(entry.get("body", "")).strip():
            return None
        return entry

    def compute_checksum(self) -> str:
        payload = self.title_it + "\n" + self.body_it
        if self.translations:  # empty for the C/D documents: their checksum is unchanged
            payload += "\n" + json.dumps(self.translations, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        new_checksum = self.compute_checksum()
        if new_checksum != self.checksum:
            if self.status == LegalStatus.PUBLISHED and self.checksum and not getattr(self, "_publishing", False):
                # A published text changed outside legal.services.publish (the back office's change form, a shell):
                # it goes back to DRAFT, so it is online again only through publish() — the permission, the source,
                # the open-field check and the LegalDocumentVersion snapshot that privacy notice §11 promises.
                self.status = LegalStatus.DRAFT
            self.version += 1
            self.checksum = new_checksum
        if self.status == LegalStatus.PUBLISHED and not self.body_it.strip():
            self.status = LegalStatus.BLOCKED
        super().save(*args, **kwargs)

    def paragraphs(self) -> list[tuple[str, str]]:
        """[(kind, text)] where kind is 'h' for a section heading or 'p' for a paragraph."""
        out: list[tuple[str, str]] = []
        for block in self.body_it.replace("\r\n", "\n").split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if block.startswith("## "):
                out.append(("h", block[3:].strip()))
            else:
                out.append(("p", block))
        return out


class LegalDocumentVersion(models.Model):
    """Immutable snapshot taken at every publication so staff can prove which text was online when."""

    document = models.ForeignKey(LegalDocument, on_delete=models.CASCADE, related_name="versions")
    version = models.PositiveIntegerField()
    title_it = models.CharField(max_length=200, blank=True)
    body_it = models.TextField()
    translations = models.JSONField(default=dict, blank=True)
    checksum = models.CharField(max_length=64)
    published_at = models.DateTimeField()
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")

    class Meta:
        ordering = ["-published_at"]
        constraints = [models.UniqueConstraint(fields=["document", "version"], name="uniq_legal_version")]

    def __str__(self) -> str:
        return f"{self.document.kind} v{self.version} ({self.published_at:%Y-%m-%d})"
