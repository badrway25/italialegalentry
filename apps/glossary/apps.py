from django.apps import AppConfig


class GlossaryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "glossary"
    verbose_name = "Glossaire — termes italiens expliqués"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from glossary import registry
        from glossary.sitemaps import GlossarySitemap

        register("glossary", GlossarySitemap)
        paths = ["glossaire/"] + [f"glossaire/{key}/" for key in registry.keys()]  # noqa: SIM118 - function, not a dict
        register_public_paths("glossary", paths, requires_gate="phase3_public", tags=("phase3",))
