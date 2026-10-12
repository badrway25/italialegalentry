from django.apps import AppConfig


class EnquiriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "enquiries"
    verbose_name = "Formulaires publics (demandes)"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from enquiries import policies  # noqa: F401 — registers the object-level policy
        from enquiries.sitemaps import EnquiriesSitemap
        from enquiries.urls import PUBLIC_PATHS

        # Public forms are gated by G2 only (never by the Phase 3 date): the pages always render
        # 200 — with the form, or with the "form unavailable" component while G2 is closed.
        register_public_paths("enquiries", list(PUBLIC_PATHS.values()), tags=("forms",))
        register("enquiries", EnquiriesSitemap)
