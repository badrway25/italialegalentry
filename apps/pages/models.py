"""
Homepage composition (master brief §21).

The homepage is an institutional entry point made of a fixed set of sections. Editors may
reorder, disable, schedule and re-title them from the back-office; they can never edit a prescribed
text: those come from the locked registry (``cms.locked_content``) at render time and are not
stored here. ``HomeSection`` therefore holds only the *non-prescribed* heading / intro / note.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import PublishableModel, PublishableQuerySet, TranslationBase


class SectionKey(models.TextChoices):
    HERO = "hero", _("Hero")
    BANNER = "banner", _("Notice institutionnelle (bannière Forum)")
    ENTRANCES = "entrances", _("Quatre accès de l’écosystème")
    ORIENTATION = "orientation", _("Orientation")
    PATHWAYS = "pathways", _("Parcours réguliers")
    PILOT = "pilot", _("Projet pilote")
    TRUST = "trust", _("Confiance et transparence")
    ANTIFRAUD = "antifraud", _("Attention aux fraudes")
    NEWS = "news", _("Actualités")
    ECOSYSTEM = "ecosystem", _("Écosystème institutionnel")
    RESERVED = "reserved", _("Espace réservé")


# Sections whose visible texts are entirely prescribed (locked registry): the editorial heading /
# intro / note of these rows are never rendered and are read-only in the back-office.
FULLY_LOCKED_SECTIONS: frozenset[str] = frozenset({SectionKey.HERO, SectionKey.BANNER})

# Sections whose *heading* is prescribed (the intro / note stay editorial).
LOCKED_HEADING_SECTIONS: frozenset[str] = frozenset({SectionKey.PILOT, SectionKey.ANTIFRAUD, SectionKey.RESERVED})

# Locked registry keys rendered by each section — shown to editors, used by the compliance tests.
LOCKED_KEYS_BY_SECTION: dict[str, tuple[str, ...]] = {
    # The hero's path carries the stations of the pilot sequence (design V5.4, W2-D): the Morocco → Italy model is
    # said once, there; the pilot chapter keeps the prescribed title and links the pilot's own page.
    SectionKey.HERO: (
        "p3.hero.title",
        "p3.hero.subtitle",
        "p3.hero.body",
        "p1.persons.replacement_1",
        "p3.pilot.sequence",
    ),
    SectionKey.BANNER: (
        "p2.home.banner.title",
        "p2.home.banner.meta",
        "p2.home.banner.quote",
        "p2.home.banner.button",
    ),
    SectionKey.ENTRANCES: tuple(
        f"p3.entrances.{actor}.{part}"
        for actor in ("person", "company", "institution", "university")
        for part in ("title", "text", "button")
    ),
    SectionKey.ORIENTATION: ("p3.persons.how_it_works",),
    SectionKey.PATHWAYS: ("p3.persons.pathways",),
    SectionKey.PILOT: ("p3.pilot.title",),
    SectionKey.TRUST: ("p3.faq.items", "p1.persons.replacement_1", "p1.persons.replacement_2"),
    SectionKey.ANTIFRAUD: ("p3.antifraud.title", "p3.antifraud.body"),
    SectionKey.NEWS: (),
    SectionKey.ECOSYSTEM: ("p3.faq.items",),
    SectionKey.RESERVED: ("p3.reserved.title", "p3.reserved.body", "p3.reserved.button"),
}


def editorial_errors(instance, field_names: tuple[str, ...]) -> dict[str, str]:
    """
    Validation shared by the French source row and its translations: an editorial column may hold
    neither a forbidden formulation nor a hand-copied fragment of a prescribed text (those are
    rendered from the locked registry only, so that their checksum and their gate always apply).
    """
    from cms.forbidden import scan
    from pages import prescribed

    errors: dict[str, str] = {}
    for name in field_names:
        value = getattr(instance, name, "") or ""
        violations = scan(value)
        if violations:
            errors[name] = _("Formulation interdite : « %(label)s ».") % {"label": violations[0].label}
        elif prescribed.any_phase(value):
            errors[name] = _(
                "Ce champ reprend un texte prescrit. Les textes prescrits s’affichent automatiquement depuis le "
                "registre verrouillé : ne jamais les recopier ni les reformuler ici."
            )
    return errors


class HomeSectionQuerySet(PublishableQuerySet):
    def ordered(self):
        return self.order_by("order", "id")

    def visible(self, at=None):
        """Enabled rows that are live right now (gates are evaluated by ``pages.services``)."""
        return self.live(at).filter(is_enabled=True).ordered()


class HomeSection(PublishableModel):
    key = models.SlugField(
        _("section"),
        max_length=20,
        unique=True,
        choices=SectionKey.choices,
        help_text=_("Identifiant technique de la section. Une seule ligne par section."),
    )
    order = models.PositiveSmallIntegerField(
        _("ordre"),
        default=0,
        db_index=True,
        help_text=_("Ordre d’affichage sur la page d’accueil (du plus petit au plus grand)."),
    )
    is_enabled = models.BooleanField(
        _("activée"),
        default=True,
        help_text=_("Décocher pour retirer la section de la page d’accueil sans la supprimer."),
    )
    requires_gate = models.CharField(
        _("visible seulement si le gate est ouvert"),
        max_length=40,
        blank=True,
        help_text=_(
            "ex. phase3_public, forum_banner. Les sections dont les textes relèvent de la Phase 3 restent "
            "de toute façon masquées tant que le gate Phase 3 est fermé."
        ),
    )
    heading_fr = models.CharField(
        _("titre de section (FR)"),
        max_length=160,
        blank=True,
        help_text=_("Titre éditorial non prescrit. Ignoré lorsque le titre provient du registre des textes prescrits."),
    )
    intro_fr = models.TextField(
        _("introduction (FR)"),
        blank=True,
        help_text=_("Courte introduction éditoriale. Ne jamais y recopier ni reformuler un texte prescrit."),
    )
    note_fr = models.TextField(
        _("note (FR)"),
        blank=True,
        help_text=_("Note ou avertissement court affiché en fin de section (facultatif)."),
    )

    objects = HomeSectionQuerySet.as_manager()

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("section de la page d’accueil")
        verbose_name_plural = _("sections de la page d’accueil")

    def __str__(self) -> str:
        return self.get_key_display()

    def clean(self):
        super().clean()
        errors = editorial_errors(self, self.rendered_editorial_fields)
        if errors:
            raise ValidationError(errors)

    @property
    def rendered_editorial_fields(self) -> tuple[str, ...]:
        """Editorial columns this section actually renders (the others are read-only in the back-office)."""
        if self.is_fully_locked:
            return ()
        names = ("heading_fr", "intro_fr", "note_fr")
        return names[1:] if self.has_locked_heading else names

    @property
    def is_fully_locked(self) -> bool:
        return self.key in FULLY_LOCKED_SECTIONS

    @property
    def has_locked_heading(self) -> bool:
        return self.key in FULLY_LOCKED_SECTIONS or self.key in LOCKED_HEADING_SECTIONS

    @property
    def locked_keys(self) -> tuple[str, ...]:
        return LOCKED_KEYS_BY_SECTION.get(self.key, ())


class HomeSectionTranslation(TranslationBase):
    master = models.ForeignKey(HomeSection, on_delete=models.CASCADE, related_name="translations")
    heading = models.CharField(_("titre de section"), max_length=160, blank=True)
    intro = models.TextField(_("introduction"), blank=True)
    note = models.TextField(_("note"), blank=True)

    class Meta:
        verbose_name = _("traduction de section")
        verbose_name_plural = _("traductions de section")
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="pages_homesectiontranslation_unique"),
        ]

    def __str__(self) -> str:
        return f"{self.master_id}:{self.language}"

    def clean(self):
        super().clean()
        errors = editorial_errors(self, ("heading", "intro", "note"))
        if errors:
            raise ValidationError(errors)
