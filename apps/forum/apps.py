from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "forum"
    verbose_name = "Forum Vénétie–Maroc"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register

        # Both modules register object-level policies at import time (deny by default):
        # ``permissions`` for the public Forum, ``governance_policies`` for the authenticated one.
        from forum import governance_policies, permissions  # noqa: F401
        from forum.sitemaps import ForumSitemap

        register("forum", ForumSitemap)
        register_public_paths("forum", ["forum/", "forum/inscription/", "forum/inscription/confirmation/"])
