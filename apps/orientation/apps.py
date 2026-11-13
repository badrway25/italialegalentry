from django.apps import AppConfig


class OrientationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orientation"
    verbose_name = "Orientation"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from orientation import policies  # noqa: F401 - registers object-level policies
        from orientation.sitemaps import OrientationSitemap

        # The wizard is core platform (not Phase 3 gated): open, anonymous, no personal data.
        register_public_paths("orientation", ["orientation/", "orientation/reprendre/"])
        register("orientation", OrientationSitemap)
