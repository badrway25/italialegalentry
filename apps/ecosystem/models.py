"""
Ecosystem spaces — thin editorial layer over four pages whose wording is prescribed.

* ``EcosystemSpace`` — one row per page (companies | institutions | universities | pilot). It only
  carries the *editorial* additions: a sober photograph from the media library and an optional
  introductory note. The prescribed texts (``p1.companies.*``, ``p3.institutions.*``,
  ``p3.universities.*``, ``p3.pilot.*``) are never stored here: templates print them from the locked
  registry (gate G0). The publication status of a row governs the editorial layer only; whether a
  *route* answers is decided by the publication gates alone (``ecosystem.services.page_visible``),
  so the Phase 1 page can never go offline by mistake and a Phase 3 page can never go online early.
* ``EcosystemSpaceTranslation`` — translations of the editorial note (gate G10: only PUBLISHED rows
  are rendered).
* ``PilotStep`` — back-office mirror of the prescribed eight-step sequence (``p3.pilot.sequence``)
  plus optional, non-prescribed additions. Locked rows always carry the registry wording, keep the
  prescribed position (``order == locked_index``) and are read-only in the admin; additions come
  strictly after the prescribed sequence and stay hidden until an editor switches them on.
"""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from cms.models import PublishableModel, TranslationBase
from core.models import TimeStampedModel

PILOT_SEQUENCE_KEY = "p3.pilot.sequence"
GATE_PHASE3 = "phase3_public"


class SpaceKey(models.TextChoices):
    COMPANIES = "companies", _("Espace Entreprises (Fase 1)")
    INSTITUTIONS = "institutions", _("Espace Institutions (Fase 3)")
    UNIVERSITIES = "universities", _("Espace Universités et Formation (Fase 3)")
    PILOT = "pilot", _("Projet Pilote Vénétie–Maroc (Fase 3)")


class SpaceGate(models.TextChoices):
    NONE = "", _("Nessun gate (Fase 1 — sempre online)")
    PHASE3 = GATE_PHASE3, _("Gate G3 — Fase 3 (non prima del 2 ottobre 2026)")


# Gate prescribed for each page. Phase 1 must never depend on Phase 3 (Implementation §1.1) and the
# Phase 3 pages must never be published before gate G3 opens (Implementation p.7).
REQUIRED_GATES: dict[str, str] = {
    SpaceKey.COMPANIES: SpaceGate.NONE,
    SpaceKey.INSTITUTIONS: SpaceGate.PHASE3,
    SpaceKey.UNIVERSITIES: SpaceGate.PHASE3,
    SpaceKey.PILOT: SpaceGate.PHASE3,
}


def required_gate(key: str) -> str:
    return str(REQUIRED_GATES.get(key, SpaceGate.PHASE3))


def reject_forbidden_formulations(text: str, field: str) -> None:
    """Editorial wording goes through the same scanner as the public pages (cms.forbidden)."""
    from cms.forbidden import scan

    violations = scan(text or "")
    if violations:
        raise ValidationError({field: _("Formulazione vietata: %(label)s") % {"label": violations[0].label}})


class EcosystemSpace(PublishableModel):
    key = models.CharField(_("spazio"), max_length=16, choices=SpaceKey.choices, unique=True)
    order = models.PositiveSmallIntegerField(_("ordine"), default=0, db_index=True)
    hero_image = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("fotografia"),
        help_text=_("Immagine sobria dalla libreria (imprese, formazione, università, cooperazione)."),
    )
    intro_note_fr = models.TextField(
        _("nota editoriale (FR — sorgente)"),
        blank=True,
        help_text=_(
            "Facoltativa. Non sostituisce né riformula i testi prescritti; nessun contenuto giuridico, "
            "nessuna promessa di esito."
        ),
    )
    requires_gate = models.CharField(
        _("gate di pubblicazione"),
        max_length=40,
        blank=True,
        choices=SpaceGate.choices,
        default=SpaceGate.NONE,
        help_text=_("Determinato dallo spazio: non modificabile dal back-office."),
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("spazio dell’ecosistema")
        verbose_name_plural = _("spazi dell’ecosistema")
        constraints = [
            models.CheckConstraint(condition=Q(key__in=SpaceKey.values), name="ecosystem_space_key_valid"),
            # Phase 1 never gated, Phase 3 always gated — enforced by the database, not by convention.
            models.CheckConstraint(
                condition=(
                    Q(key=SpaceKey.COMPANIES, requires_gate=SpaceGate.NONE)
                    | (~Q(key=SpaceKey.COMPANIES) & Q(requires_gate=SpaceGate.PHASE3))
                ),
                name="ecosystem_space_gate_matches_phase",
            ),
        ]

    def __str__(self) -> str:
        return str(self.get_key_display())

    def clean(self):
        super().clean()
        if self.key and self.requires_gate != required_gate(self.key):
            raise ValidationError({"requires_gate": _("Il gate è determinato dallo spazio e non può essere cambiato.")})
        reject_forbidden_formulations(self.intro_note_fr, "intro_note_fr")

    def save(self, *args, **kwargs):
        # The gate is a property of the page, not an editorial choice.
        self.requires_gate = required_gate(self.key)
        super().save(*args, **kwargs)


class EcosystemSpaceTranslation(TranslationBase):
    master = models.ForeignKey(EcosystemSpace, on_delete=models.CASCADE, related_name="translations")
    intro_note = models.TextField(_("nota editoriale tradotta"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_ecosystem_space_translation"),
        ]
        verbose_name = _("traduzione dello spazio")
        verbose_name_plural = _("traduzioni dello spazio")

    def __str__(self) -> str:
        return f"{self.master_id} [{self.language}] {self.get_status_display()}"

    def clean(self):
        super().clean()
        if self.language == settings.CONTENT_FALLBACK_LANGUAGE:
            raise ValidationError({"language": _("La versione francese è il testo sorgente, non una traduzione.")})
        reject_forbidden_formulations(self.intro_note, "intro_note")


def pilot_sequence() -> list[str]:
    """The prescribed labels, in the prescribed order (always the French source of the registry)."""
    value, _lang = locked_content.get(PILOT_SEQUENCE_KEY, locked_content.FALLBACK_LANGUAGE)
    return list(value)


class PilotStepQuerySet(models.QuerySet):
    def locked(self):
        return self.filter(is_locked=True)

    def additions(self):
        return self.filter(is_locked=False)

    def visible_additions(self):
        return self.filter(is_locked=False, is_visible=True)


class PilotStep(TimeStampedModel):
    order = models.PositiveSmallIntegerField(
        _("posizione"),
        unique=True,
        help_text=_("1–8: sequenza prescritta. Le aggiunte editoriali seguono la sequenza (da 9 in poi)."),
    )
    locked_index = models.PositiveSmallIntegerField(
        _("indice nella sequenza prescritta"), null=True, blank=True, unique=True, editable=False
    )
    label_fr = models.CharField(_("etichetta (FR — sorgente)"), max_length=120)
    is_locked = models.BooleanField(
        _("testo bloccato"),
        default=False,
        editable=False,
        help_text=_("Vero per le otto tappe prescritte: l’etichetta proviene dal registro e non è modificabile."),
    )
    is_visible = models.BooleanField(
        _("visibile nel diagramma"),
        default=False,
        help_text=_("Solo per le aggiunte editoriali; le otto tappe prescritte sono sempre visibili."),
    )

    objects = PilotStepQuerySet.as_manager()

    class Meta:
        ordering = ["order"]
        verbose_name = _("tappa del progetto pilota")
        verbose_name_plural = _("tappe del progetto pilota")
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(is_locked=True, locked_index__gte=1, locked_index__lte=8, order=F("locked_index"))
                    | Q(is_locked=False, locked_index__isnull=True, order__gt=8)
                ),
                name="ecosystem_pilotstep_locked_position",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.order:02d} — {self.label_fr}"

    def registry_label(self) -> str | None:
        if not self.locked_index:
            return None
        sequence = pilot_sequence()
        if 1 <= self.locked_index <= len(sequence):
            return sequence[self.locked_index - 1]
        return None

    def clean(self):
        super().clean()
        if self.is_locked:
            if self.registry_label() is None:
                raise ValidationError(
                    _("Solo le tappe presenti nel registro dei testi bloccati possono essere bloccate.")
                )
        elif self.order is not None and self.order <= len(pilot_sequence()):
            raise ValidationError(
                {"order": _("Le aggiunte editoriali non possono inserirsi nella sequenza prescritta (posizione ≥ 9).")}
            )
        if not self.is_locked:
            reject_forbidden_formulations(self.label_fr, "label_fr")

    def save(self, *args, **kwargs):
        if self.is_locked:
            label = self.registry_label()
            if label is not None:
                # Gate G0: the prescribed wording and position always win, whatever was submitted.
                self.label_fr = label
                self.order = self.locked_index
            self.is_visible = True
        super().save(*args, **kwargs)
