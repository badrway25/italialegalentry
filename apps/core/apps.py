from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core / Gate"

    def ready(self):
        from core import signals  # noqa: F401
        from core.public_routes import register_public_paths

        register_public_paths("core", [""])
