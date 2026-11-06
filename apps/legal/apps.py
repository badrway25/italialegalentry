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
        # V5.14: the privacy notice and the cookie information (A/B) are always public routes; the substantive pages
        # (C/D: official notices, terms, disclaimer) answer 404 to the public until published (Q2; the W2 review's
        # M-2, legal.views.SUBSTANTIVE), so they are registered behind the legal-pages gate — the route suites expect
        # their 404 while it is closed, and core.links hides any link to them meanwhile.
        register_public_paths("legal", ["privacy-policy/", "cookie-policy/"])
        register_public_paths(
            "legal", ["note-legali/", "condizioni-di-utilizzo/", "avvertenze/"], requires_gate="legal_pages"
        )
