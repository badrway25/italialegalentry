from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "documents"
    verbose_name = "Documents"

    def ready(self):
        import documents.policies  # noqa: F401 — registers the object-level policy
        from accounts.services import register_export_section
        from accounts.signals import user_anonymised
        from documents import receivers, services

        register_export_section("documents")(services.documents_export_section)
        user_anonymised.connect(receivers.on_user_anonymised, dispatch_uid="documents.on_user_anonymised")
