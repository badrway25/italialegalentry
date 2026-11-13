from django.apps import AppConfig


class RulesConfig(AppConfig):
    """
    The versioned legal rule engine: rules are data with a source, a validity window,
        a version and a four-eyes approval workflow.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "rules"
    verbose_name = "Regole giuridiche"

    def ready(self) -> None:
        # Importing the module is what registers the object-level policies; without it the registry
        # is empty for these models and ``can()`` answers False for everyone, which would look like
        # a permission bug rather than a missing import.
        from rules import policies  # noqa: F401
