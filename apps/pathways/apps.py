from django.apps import AppConfig


class PathwaysConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pathways"
    verbose_name = "Espace Personnes — parcours"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from pathways.models import PATHWAY_KEYS
        from pathways.sitemaps import PathwaysSitemap

        register("pathways", PathwaysSitemap)
        # The Espace Personnes landing renders an interim page before Phase 3 (always 200).
        register_public_paths("pathways", ["parcours/"])
        # Detail pages, diplomas and training are Phase 3 content: 404 while gate G3 is closed.
        register_public_paths(
            "pathways",
            [f"parcours/{key}/" for key in PATHWAY_KEYS] + ["diplomes-et-titres/", "formation/"],
            requires_gate="phase3_public",
        )
