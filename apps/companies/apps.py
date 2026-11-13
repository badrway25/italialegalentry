from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    """
    Company profiles and their skills needs. An impresa expresses a NEED; it never browses people.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "companies"
    verbose_name = "Imprese e fabbisogni"

    def ready(self):
        # Every company route requires an authenticated account, so nothing is registered in
        # core.public_routes (the registry of pages that must answer 200 to anonymous crawlers).
        import companies.policies  # noqa: F401 — registers the object-level policies (deny by default)
        from accounts.services import register_export_section
        from companies import receivers

        register_export_section("companies")(receivers.companies_export_section)
