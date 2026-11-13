from django.apps import AppConfig


class PortalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "portal"
    verbose_name = "Espace réservé"

    def ready(self):
        # No call to core.public_routes.register_public_paths: EVERY portal route requires an
        # authenticated account (anonymous visitors are redirected to the login page), so none of
        # them belongs to the registry of pages that must answer 200 to anonymous crawlers.
        import portal.policies  # noqa: F401 — registers the object-level policies (deny by default)
        from accounts.services import register_export_section
        from accounts.signals import user_anonymised
        from portal import receivers

        register_export_section("portal")(receivers.portal_export_section)
        user_anonymised.connect(receivers.on_user_anonymised, dispatch_uid="portal.on_user_anonymised")
