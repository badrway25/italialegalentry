from django.apps import AppConfig


class LivingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "living"
    verbose_name = "Vivre en Italie"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from living.sitemaps import LivingSitemap

        register("living", LivingSitemap)
        # V5.12 §8: the index alone is a registered public page. A theme's page exists only once it carries a live,
        # reviewed sheet (living.services.public_topics) — content, not a gate — so it is not registered as a page
        # that must answer 200 when G3 opens.
        register_public_paths("living", ["vivre-en-italie/"], requires_gate="phase3_public")
