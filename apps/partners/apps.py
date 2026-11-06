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
        # V5.12 §8: the index exists once one partner is live and authorised in writing (core.gates.partners_public)
        register_public_paths("partners", ["partenaires/"], requires_gate="partners_public")
