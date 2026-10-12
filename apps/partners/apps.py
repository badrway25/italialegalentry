from django.apps import AppConfig


class PartnersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "partners"
    verbose_name = "Partner e istituzioni"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from partners.sitemaps import PartnersSitemap

        register("partners", PartnersSitemap)
        register_public_paths("partners", ["partenaires/"])
