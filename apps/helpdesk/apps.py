from django.apps import AppConfig


class HelpdeskConfig(AppConfig):
    """
    Escalation from automated orientation to human review, with explicit states and
        an assigned professional.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "helpdesk"
    verbose_name = "Sportello digitale"

    def ready(self):
        # Object-level policies register themselves at import time (deny by default), and the
        # escalation receiver connects the rule engine's REVIEW_REQUIRED outcome to a human.
        from helpdesk import policies, receivers  # noqa: F401
