from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "community"
    verbose_name = "Forum Virtuale"

    def ready(self):
        import community.policies  # noqa: F401 - registers object-level policies
        from core.public_routes import register_public_paths

        register_public_paths("community", ["forum-virtuel/"], requires_gate="virtual_forum")
