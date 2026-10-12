"""
Legal pages — official Italian text only (document §1.4 and Annexe 1).

The five documents exist as rows from the first migration/seed, in status BLOCKED until the
official « Allegato 1 — Testi legali » is transmitted and pasted verbatim by an authorised
user. The technical team never writes or translates legal text (gate G1).
"""

from __future__ import annotations

import hashlib

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
    def is_available(self) -> bool:
        return self.status == LegalStatus.PUBLISHED and bool(self.body_it.strip())

    def compute_checksum(self) -> str:
        return hashlib.sha256((self.title_it + "\n" + self.body_it).encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        new_checksum = self.compute_checksum()
        if new_checksum != self.checksum:
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
    checksum = models.CharField(max_length=64)
    published_at = models.DateTimeField()
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")

    class Meta:
        ordering = ["-published_at"]
        constraints = [models.UniqueConstraint(fields=["document", "version"], name="uniq_legal_version")]

    def __str__(self) -> str:
        return f"{self.document.kind} v{self.version} ({self.published_at:%Y-%m-%d})"
