from django.apps import AppConfig


class LegalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "legal"
    verbose_name = "Pagine legali"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from legal.sitemaps import LegalSitemap

        register("legal", LegalSitemap)
        register_public_paths(
            "legal",
            ["privacy-policy/", "cookie-policy/", "note-legali/", "condizioni-di-utilizzo/", "avvertenze/"],
        )
