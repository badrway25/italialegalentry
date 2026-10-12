from django.apps import AppConfig


class SelectionConfig(AppConfig):
    """
    The selection workflow, assignable only to an authorised actor, who is always
        named and always responsible.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "selection"
    verbose_name = "Selezione autorizzata"

    def ready(self):
        # Nothing is registered in core.public_routes: every selection route requires an
        # authenticated account, and the module must never appear on a public page (CR-03).
        import selection.policies  # noqa: F401 — registers the object-level policies (deny by default)
