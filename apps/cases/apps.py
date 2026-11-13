from django.apps import AppConfig


class CasesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cases"
    verbose_name = "Fascicoli digitali"

    def ready(self):
        # Every case route requires an authenticated account, so nothing is registered in
        # core.public_routes (the registry of pages that must answer 200 to anonymous crawlers).
        import cases.policies  # noqa: F401 — registers the object-level policies (deny by default)
