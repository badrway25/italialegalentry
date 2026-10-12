from django.apps import AppConfig


class AcademyConfig(AppConfig):
    """
    Training catalogue, enrolment and progression.

    Access never depends on being selected by a company (CONFLICT_REGISTER CR-14, REQ-EDU-04):
    every route needs an authenticated account and nothing else. Nothing is registered in
    ``core.public_routes`` for that reason — no Academy page is served to an anonymous visitor.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "academy"
    verbose_name = "Academy"

    def ready(self):
        import academy.policies  # noqa: F401 — registers the object-level policies (deny by default)
        from academy import receivers
        from accounts.services import register_export_section
        from accounts.signals import user_anonymised

        # A training record is personal data: it belongs in the person's data export (GDPR art. 15)
        # and it must disappear when the account is anonymised (art. 17). Both are wired by calling
        # the accounts API, so no file outside this app has to know the Academy exists.
        register_export_section("academy")(receivers.academy_export_section)
        user_anonymised.connect(receivers.on_user_anonymised, dispatch_uid="academy.on_user_anonymised")
