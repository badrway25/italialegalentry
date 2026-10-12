from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

from cms.admin import PUBLICATION_FIELDSET, PublishableAdminMixin
from core.admin_base import BaseModelAdmin, BaseTabularInline
from pages import services
from pages.models import HomeSection, HomeSectionTranslation

EDITORIAL_FIELDS = ("heading_fr", "intro_fr", "note_fr")


class HomeSectionTranslationInline(BaseTabularInline):
    model = HomeSectionTranslation
    fields = ("language", "heading", "intro", "note", "status", "source", "reviewed_by")
    autocomplete_fields = ("reviewed_by",)
    verbose_name_plural = _("Traductions des textes éditoriaux (seules les traductions « publiées » sont affichées)")


@admin.register(HomeSection)
class HomeSectionAdmin(PublishableAdminMixin, BaseModelAdmin):
    """
    Homepage composition. Reordering needs no drag and drop: edit the « ordre » column in the list
    and save. Prescribed texts are never editable here — they are shown read-only for reference.
    """

    list_display = ("section_label", "order", "is_enabled", "requires_gate", "gate_state", "status", "heading_fr")
    list_display_links = ("section_label",)
    list_editable = ("order", "is_enabled")
    list_filter = ("is_enabled", "status")
    search_fields = ("key", "heading_fr", "intro_fr")
    ordering = ("order", "id")
    inlines = (HomeSectionTranslationInline,)
    readonly_fields = PublishableAdminMixin.readonly_fields + ("locked_texts",)
    fieldsets = (
        (
            None,
            {
                "description": _(
                    "La page d’accueil est composée des sections actives, publiées et dont le gate est ouvert, "
                    "dans l’ordre indiqué. Une section sans contenu n’est pas affichée."
                ),
                "fields": ("key", "order", "is_enabled", "requires_gate"),
            },
        ),
        (
            _("Textes éditoriaux (non prescrits)"),
            {
                "description": _(
                    "Titres et introductions rédigés par l’équipe. Ne jamais recopier, abréger ou reformuler un "
                    "texte prescrit : ceux-ci proviennent du registre verrouillé et s’affichent automatiquement."
                ),
                "fields": EDITORIAL_FIELDS,
            },
        ),
        (
            _("Textes prescrits (lecture seule)"),
            {"fields": ("locked_texts",)},
        ),
        PUBLICATION_FIELDSET,
    )

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            fields.append("key")  # the identifier of an existing section never changes
            if obj.is_fully_locked:
                fields += [f for f in EDITORIAL_FIELDS if f not in fields]
            elif obj.has_locked_heading and "heading_fr" not in fields:
                fields.append("heading_fr")
        return fields

    def has_delete_permission(self, request, obj=None):
        # Sections are disabled (« activée »), never deleted: the seed would recreate them anyway.
        return False

    @admin.display(description=_("section"), ordering="key")
    def section_label(self, obj) -> str:
        return obj.get_key_display()

    @admin.display(boolean=True, description=_("gate ouvert maintenant"))
    def gate_state(self, obj) -> bool:
        from core import gates

        return services.section_gate_open(obj, gates.phase3_public())

    @admin.display(description=_("clés du registre verrouillé affichées par cette section"))
    def locked_texts(self, obj):
        if obj is None or not obj.locked_keys:
            return _("Aucun texte prescrit dans cette section.")
        return format_html(
            "<ul>{}</ul><p>{}</p>",
            format_html_join("", "<li><code>{}</code></li>", ((key,) for key in obj.locked_keys)),
            _("Ces textes ne sont modifiables que sur transmission écrite (voir docs/CONTENT_SOURCE_MAP.md)."),
        )
