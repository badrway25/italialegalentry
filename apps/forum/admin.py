"""Back-office of the Forum (django-unfold). Gates G4/G5/G6 are enforced by models and services."""

from __future__ import annotations

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from cms.admin import PUBLICATION_FIELDSET, PUBLICATION_READONLY, PublishableAdminMixin
from core import gates
from core.admin_base import BaseModelAdmin, BaseTabularInline
from forum import services
from forum.models import (
    ForumAgreement,
    ForumDocument,
    ForumEvent,
    ForumIntervention,
    ForumMedia,
    ForumMode,
    ForumNextEvent,
    ForumOutcome,
    ForumPartner,
    ForumProgramItem,
    ForumRegistration,
    RegistrationStatus,
    SpeakerRole,
)

SPEAKER_WARNING = _(
    "Aucun nom de personnalité institutionnelle ne doit être publié sans transmission écrite de l’Avv. Badrane. "
    "Le nom n’apparaît publiquement que si « nom autorisé » est coché (avec référence) ET si le drapeau "
    "forum_speaker_names_authorized est actif."
)
LOGO_WARNING = _(
    "Les logos de la Région de la Vénétie et de la Commune de Rovigo seront transmis avec leurs autorisations : "
    "ne jamais télécharger ni inventer un logo. Un partenaire non autorisé n’est jamais affiché publiquement."
)


class ForumProgramItemInline(BaseTabularInline):
    model = ForumProgramItem
    fields = ("order", "time_label", "title_fr", "description_fr", "is_visible", "is_locked_seed")
    readonly_fields = ("is_locked_seed",)
    ordering_field = "order"
    hide_ordering_field = False
    extra = 0
    verbose_name = _("point du programme")
    verbose_name_plural = _("Programme (modifiable — action « Réinitialiser » pour revenir au programme prescrit)")


class SpeakerRoleInline(BaseTabularInline):
    model = SpeakerRole
    fields = (
        "order",
        "role_label_fr",
        "person_name",
        "organisation",
        "names_authorized",
        "authorization_reference",
        "is_visible",
        "name_public",
    )
    readonly_fields = ("name_public",)
    ordering_field = "order"
    hide_ordering_field = False
    extra = 0
    verbose_name_plural = _("Intervenants — fonctions (les noms restent masqués : gate G5)")

    @admin.display(description=_("Nom publié ?"), boolean=True)
    def name_public(self, obj: SpeakerRole) -> bool:
        return bool(obj.pk and obj.public_name(services.speaker_names_visible()))


class ForumPartnerInline(BaseTabularInline):
    model = ForumPartner
    fields = ("order", "name", "kind", "logo", "authorized", "authorization_reference", "note", "logo_public")
    readonly_fields = ("logo_public",)
    autocomplete_fields = ("logo",)
    ordering_field = "order"
    hide_ordering_field = False
    extra = 0
    verbose_name_plural = _("Partenaires et logos (affichés seulement si autorisés : gate G6)")

    @admin.display(description=_("Logo affiché ?"), boolean=True)
    def logo_public(self, obj: ForumPartner) -> bool:
        return bool(obj.pk and obj.is_public)


@admin.register(ForumEvent)
class ForumEventAdmin(PublishableAdminMixin, BaseModelAdmin):
    list_display = ("slug", "date", "city", "current_mode", "registration_open", "registrations_total", "status")
    list_filter = ("status", "mode_override", "registration_open")
    search_fields = ("slug", "city", "venue")
    readonly_fields = PUBLICATION_READONLY + ("current_mode", "gate_summary", "registrations_total")
    autocomplete_fields = ("hero_image",)
    inlines = (ForumProgramItemInline, SpeakerRoleInline, ForumPartnerInline)
    actions = ("reset_programme",)
    fieldsets = (
        (None, {"fields": ("slug", "is_primary", "locked_key_prefix", "hero_image", "gate_summary")}),
        (
            _("Événement"),
            {"fields": ("date", "start_time", "end_time", "venue", "city", "country_code")},
        ),
        (_("Mode de la page (gate G4)"), {"fields": ("mode_override", "current_mode")}),
        (
            _("Inscriptions"),
            {"fields": ("registration_open", "registration_deadline", "capacity", "registrations_total")},
        ),
        PUBLICATION_FIELDSET,
    )

    @admin.display(description=_("Mode actuel"))
    def current_mode(self, obj: ForumEvent) -> str:
        if obj is None or obj.pk is None:
            return "—"
        return f"{obj.get_mode_override_display()} → {ForumMode(obj.effective_mode()).label}"

    @admin.display(description=_("Inscriptions reçues"))
    def registrations_total(self, obj: ForumEvent) -> int:
        return obj.registrations.count() if obj.pk else 0

    @admin.display(description=_("Gates"))
    def gate_summary(self, obj: ForumEvent) -> str:
        forms = gates.public_forms_enabled()
        rows = [
            (_("Formulaires publics (G2)"), forms.open, forms.reason),
            (_("Mode Forum permanent (G4)"), obj.pk is not None and obj.is_permanent(), ""),
            (_("Noms des intervenants (G5, drapeau)"), services.speaker_names_visible(), str(SPEAKER_WARNING)),
            (_("Forum Virtuel (G11)"), gates.virtual_forum_enabled(), ""),
        ]
        items = format_html_join(
            "",
            "<li><strong>{}</strong> : {} {}</li>",
            ((label, "✔" if ok else "✖", reason) for label, ok, reason in rows),
        )
        return format_html("<ul>{}</ul><p>{}</p>", items, LOGO_WARNING)

    @admin.action(description=_("Réinitialiser le programme au programme prescrit (8 points)"))
    def reset_programme(self, request, queryset):
        total = 0
        for event in queryset:
            total += services.reset_programme(event, request)
        self.message_user(
            request, _("Programme réinitialisé : %(n)d point(s) recréé(s).") % {"n": total}, messages.SUCCESS
        )


@admin.register(SpeakerRole)
class SpeakerRoleAdmin(BaseModelAdmin):
    list_display = ("role_label_fr", "event", "order", "names_authorized", "name_public", "is_visible")
    list_filter = ("event", "names_authorized", "is_visible")
    search_fields = ("role_label_fr", "organisation")
    readonly_fields = ("name_public", "authorized_at", "is_locked_seed", "warning")
    fieldsets = (
        (None, {"fields": ("event", "order", "role_label_fr", "organisation", "is_visible", "is_locked_seed")}),
        (
            _("Nom de la personne (gate G5)"),
            {
                "fields": (
                    "warning",
                    "person_name",
                    "names_authorized",
                    "authorization_reference",
                    "authorized_at",
                    "name_public",
                ),
            },
        ),
    )

    @admin.display(description=_("Avertissement"))
    def warning(self, obj=None) -> str:
        return format_html('<p class="text-red-700 font-semibold">{}</p>', SPEAKER_WARNING)

    @admin.display(description=_("Nom publié ?"), boolean=True)
    def name_public(self, obj: SpeakerRole) -> bool:
        return bool(obj.pk and obj.public_name(services.speaker_names_visible()))


@admin.register(ForumPartner)
class ForumPartnerAdmin(BaseModelAdmin):
    list_display = ("name", "event", "kind", "authorized", "logo_public", "order")
    list_filter = ("event", "kind", "authorized")
    search_fields = ("name", "note")
    autocomplete_fields = ("logo",)
    readonly_fields = ("logo_public", "warning")
    fieldsets = (
        (None, {"fields": ("event", "order", "name", "kind", "website", "note")}),
        (_("Logo (gate G6)"), {"fields": ("warning", "logo", "authorized", "authorization_reference", "logo_public")}),
    )

    @admin.display(description=_("Avertissement"))
    def warning(self, obj=None) -> str:
        return format_html('<p class="text-red-700 font-semibold">{}</p>', LOGO_WARNING)

    @admin.display(description=_("Logo affiché ?"), boolean=True)
    def logo_public(self, obj: ForumPartner) -> bool:
        return bool(obj.pk and obj.is_public)


class OrderedPublishableAdmin(PublishableAdminMixin, BaseModelAdmin):
    list_filter = ("event", "status")
    ordering = ("order", "id")


@admin.register(ForumRegistration)
class ForumRegistrationAdmin(BaseModelAdmin):
    list_display = (
        "created_at",
        "last_name",
        "first_name",
        "organisation",
        "category",
        "country",
        "status",
        "anonymised",
    )
    list_filter = ("status", "category", "country", "language", "event", "invited_to_virtual_forum")
    search_fields = ("last_name", "first_name", "email", "organisation")
    date_hierarchy = "created_at"
    readonly_fields = (
        "event",
        "first_name",
        "last_name",
        "organisation",
        "role",
        "email",
        "phone",
        "country",
        "category",
        "sector_of_interest",
        "consent",
        "consent_version",
        "language",
        "ip_hash",
        "user_agent",
        "user",
        "anonymised_at",
    )
    fieldsets = (
        (None, {"fields": ("event", "status", "admin_notes", "invited_to_virtual_forum", "last_contact_at")}),
        (
            _("Participant"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "organisation",
                    "role",
                    "email",
                    "phone",
                    "country",
                    "category",
                    "sector_of_interest",
                )
            },
        ),
        (_("Consentement (preuve)"), {"fields": ("consent", "consent_version", "language")}),
        (_("Technique"), {"fields": ("ip_hash", "user_agent", "user", "anonymised_at", "created_at", "updated_at")}),
    )
    actions = ("export_csv", "mark_confirmed", "mark_attended", "mark_cancelled", "anonymise")

    def has_add_permission(self, request):
        return False  # registrations only come from the public form (consent proof required)

    @admin.display(description=_("Anonymisée"), boolean=True)
    def anonymised(self, obj: ForumRegistration) -> bool:
        return obj.is_anonymised

    @admin.display(description=_("Version du consentement"))
    def consent_version(self, obj: ForumRegistration) -> str:
        return services.consent_version(obj) if obj.pk else ""

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        status = gates.public_forms_enabled()
        if not status.open:
            self.message_user(
                request, _("Formulaires publics désactivés (gate G2) : %(r)s") % {"r": status.reason}, messages.WARNING
            )
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description=_("Exporter en CSV (UTF-8 BOM, avec version et horodatage du consentement)"))
    def export_csv(self, request, queryset):
        payload = services.export_csv(queryset.order_by("created_at"), request)
        response = HttpResponse(payload, content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="forum-inscriptions.csv"'
        return response

    def _set_status(self, request, queryset, status):
        n = services.set_status(queryset, status, request)
        self.message_user(
            request, ngettext("%(n)d inscription mise à jour.", "%(n)d inscriptions mises à jour.", n) % {"n": n}
        )

    @admin.action(description=_("Marquer comme confirmées"))
    def mark_confirmed(self, request, queryset):
        self._set_status(request, queryset, RegistrationStatus.CONFIRMED)

    @admin.action(description=_("Marquer comme présentes"))
    def mark_attended(self, request, queryset):
        self._set_status(request, queryset, RegistrationStatus.ATTENDED)

    @admin.action(description=_("Marquer comme annulées"))
    def mark_cancelled(self, request, queryset):
        self._set_status(request, queryset, RegistrationStatus.CANCELLED)

    @admin.action(description=_("Anonymiser (effacement RGPD — irréversible)"))
    def anonymise(self, request, queryset):
        n = 0
        for registration in queryset:
            if not registration.is_anonymised:
                services.anonymise_registration(registration, request)
                n += 1
        self.message_user(
            request, ngettext("%(n)d inscription anonymisée.", "%(n)d inscriptions anonymisées.", n) % {"n": n}
        )


@admin.register(ForumMedia)
class ForumMediaAdmin(OrderedPublishableAdmin):
    list_display = ("__str__", "event", "kind", "order", "status", "publish_at")
    list_filter = ("event", "kind", "status")
    search_fields = ("caption", "credit")
    autocomplete_fields = ("asset",)
    fieldsets = (
        (None, {"fields": ("event", "order", "kind", "asset", "file", "caption", "credit")}),
        PUBLICATION_FIELDSET,
    )


@admin.register(ForumDocument)
class ForumDocumentAdmin(OrderedPublishableAdmin):
    list_display = ("title", "event", "order", "status", "publish_at")
    search_fields = ("title", "description")
    fieldsets = ((None, {"fields": ("event", "order", "title", "file", "description")}), PUBLICATION_FIELDSET)


@admin.register(ForumIntervention)
class ForumInterventionAdmin(OrderedPublishableAdmin):
    list_display = ("title", "event", "speaker", "order", "status")
    search_fields = ("title", "abstract")
    autocomplete_fields = ("speaker", "document")
    fieldsets = (
        (None, {"fields": ("event", "order", "title", "speaker", "abstract", "document")}),
        PUBLICATION_FIELDSET,
    )


@admin.register(ForumAgreement)
class ForumAgreementAdmin(OrderedPublishableAdmin):
    list_display = ("title", "event", "kind", "parties", "signed_on", "status")
    list_filter = ("event", "kind", "status")
    search_fields = ("title", "parties", "summary")
    autocomplete_fields = ("document",)
    fieldsets = (
        (None, {"fields": ("event", "order", "kind", "title", "parties", "signed_on", "summary", "document")}),
        PUBLICATION_FIELDSET,
    )


@admin.register(ForumOutcome)
class ForumOutcomeAdmin(OrderedPublishableAdmin):
    list_display = ("title", "event", "order", "status")
    search_fields = ("title", "text")
    fieldsets = ((None, {"fields": ("event", "order", "title", "text")}), PUBLICATION_FIELDSET)


@admin.register(ForumNextEvent)
class ForumNextEventAdmin(OrderedPublishableAdmin):
    list_display = ("title", "event", "date", "place", "status")
    search_fields = ("title", "place", "description")
    ordering = ("date", "order")
    fieldsets = (
        (None, {"fields": ("event", "order", "title", "date", "place", "description", "url")}),
        PUBLICATION_FIELDSET,
    )


# The authenticated governance module registers its own ModelAdmins. Django auto-discovers
# ``<app>.admin`` and nothing else, so the module is imported here — and it is a separate file
# because it is a separate product: this one edits a public page, that one edits a workspace.
from forum import governance_admin  # noqa: E402,F401 — registers the governance back-office
