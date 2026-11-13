from django.apps import AppConfig


class FaqConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "faq"
    verbose_name = "FAQ — Questions fréquentes"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from faq.sitemaps import FAQSitemap

        register("faq", FAQSitemap)
        register_public_paths("faq", ["faq/"], requires_gate="phase3_public", tags=("phase3",))
