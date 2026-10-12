from django.apps import AppConfig


class LivingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "living"
    verbose_name = "Vivre en Italie"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from living.catalogue import TOPIC_SLUGS
        from living.sitemaps import LivingSitemap

        register("living", LivingSitemap)
        register_public_paths(
            "living",
            ["vivre-en-italie/"] + [f"vivre-en-italie/{slug}/" for slug in TOPIC_SLUGS],
            requires_gate="phase3_public",
        )
