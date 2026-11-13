from django.apps import AppConfig


class EcosystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ecosystem"
    verbose_name = "Espaces de l’écosystème"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from ecosystem.models import GATE_PHASE3
        from ecosystem.services import gated_paths, ungated_paths
        from ecosystem.sitemaps import EcosystemSitemap

        register("ecosystem", EcosystemSitemap)
        # Espace Entreprises is Phase 1: online now, whatever the state of gate G3.
        register_public_paths("ecosystem", ungated_paths())
        # Institutions, Universités et Formation, Projet Pilote: 404 while gate G3 is closed.
        register_public_paths("ecosystem", gated_paths(), requires_gate=GATE_PHASE3)
