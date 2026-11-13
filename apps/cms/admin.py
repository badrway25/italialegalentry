from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cms.models import HomeHero, MediaAsset, MenuItem, Redirect, SiteBanner
from core.admin_base import BaseModelAdmin

PUBLICATION_FIELDSET = (
    _("Pubblicazione"),
    {
        "fields": (
            "status",
            "publish_at",
            "unpublish_at",
            "published_at",
            "last_reviewed_at",
            "version",
            "author",
            "reviewer",
            "editorial_note",
        )
    },
)
PUBLICATION_READONLY = ("published_at", "version")


class PublishableAdminMixin:
    list_filter = ("status",)
    readonly_fields = PUBLICATION_READONLY

    def save_model(self, request, obj, form, change):
        if not change and hasattr(obj, "author") and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(MenuItem)
class MenuItemAdmin(BaseModelAdmin):
    list_display = ("label_fr", "location", "parent", "order", "url_name", "requires_gate", "is_visible")
    list_filter = ("location", "is_visible")
    list_editable = ("order", "is_visible")
    search_fields = ("label_fr", "label_it", "label_en", "url_name", "url")
    ordering = ("location", "parent__id", "order")


@admin.register(SiteBanner)
class SiteBannerAdmin(PublishableAdminMixin, BaseModelAdmin):
    list_display = ("key", "status", "publish_at", "unpublish_at", "requires_flag", "version")
    readonly_fields = PUBLICATION_READONLY + ("locked_key",)
    fieldsets = (
        (None, {"fields": ("key", "locked_key", "requires_flag")}),
        (
            _("Testi (solo se non bloccati)"),
            {"fields": ("title_fr", "meta_fr", "quote_fr", "button_label_fr", "url_name", "url")},
        ),
        PUBLICATION_FIELDSET,
    )


@admin.register(HomeHero)
class HomeHeroAdmin(PublishableAdminMixin, BaseModelAdmin):
    list_display = ("variant", "status", "title_fr", "version", "updated_at")
    fieldsets = (
        (None, {"fields": ("variant", "image")}),
        (
            _("Testi (variante interim; la variante Fase 3 usa i testi bloccati)"),
            {"fields": ("eyebrow_fr", "title_fr", "subtitle_fr", "body_fr")},
        ),
        (
            _("Call to action"),
            {
                "fields": (
                    "primary_cta_label_fr",
                    "primary_cta_url_name",
                    "secondary_cta_label_fr",
                    "secondary_cta_url_name",
                )
            },
        ),
        PUBLICATION_FIELDSET,
    )


@admin.register(MediaAsset)
class MediaAssetAdmin(BaseModelAdmin):
    list_display = ("title", "license", "author", "width", "height", "stereotype_checked", "created_at")
    list_filter = ("license", "stereotype_checked")
    search_fields = ("title", "author", "source_url", "alt_fr")
    readonly_fields = ("width", "height")


@admin.register(Redirect)
class RedirectAdmin(BaseModelAdmin):
    list_display = ("old_path", "new_path", "permanent")
    search_fields = ("old_path", "new_path")
