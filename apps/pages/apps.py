from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"
    verbose_name = "Pages"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from pages.sitemaps import PagesSitemap
        from pages.urls import GATED_PATHS, PUBLIC_PATHS

        register("pages", PagesSitemap)
        # Homepage and institutional pages: always 200 (their Phase 3 parts are gated inside the page).
        register_public_paths("pages", list(PUBLIC_PATHS.values()))
        # « Attention aux fraudes » is Phase 3 content: 404 while gate G3 is closed.
        register_public_paths("pages", list(GATED_PATHS.values()), requires_gate="phase3_public", tags=("phase3",))
